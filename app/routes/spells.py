from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.spell import Spell
from app.schemas.spell import SpellCreate, SpellUpdate, SpellResponse

router = APIRouter(
    prefix="/characters/{character_id}/spells",
    tags=["spells"]
)

@router.get("/", response_model=list[SpellResponse])
def list_spells(character_id: int, db: Session = Depends(get_db)):
    return db.query(Spell).filter(
        Spell.character_id == character_id
    ).all()

@router.post("/", response_model=SpellResponse)
def add_spell(
    character_id: int,
    spell: SpellCreate,
    db: Session = Depends(get_db)
):
    db_spell = Spell(**spell.dict(), character_id=character_id)
    db.add(db_spell)
    db.commit()
    db.refresh(db_spell)
    return db_spell

@router.patch("/{spell_id}", response_model=SpellResponse)
def prepare_spell(
    character_id: int,
    spell_id: int,
    payload: SpellUpdate,
    db: Session = Depends(get_db)
):
    spell = db.query(Spell).filter(
        Spell.id == spell_id,
        Spell.character_id == character_id
    ).first()

    if not spell:
        raise HTTPException(status_code=404, detail="Spell not found")

    for k, v in payload.dict(exclude_unset=True).items():
        setattr(spell, k, v)

    db.commit()
    db.refresh(spell)
    return spell

@router.delete("/{spell_id}", response_model=dict)
def delete_spell(
    character_id: int,
    spell_id: int,
    db: Session = Depends(get_db)
):
    # Buscamos a magia garantindo que pertença ao personagem
    spell = db.query(Spell).filter(
        Spell.id == spell_id,
        Spell.character_id == character_id
    ).first()

    if not spell:
        raise HTTPException(status_code=404, detail="Magia não encontrada")

    db.delete(spell)
    db.commit()
    
    return {"detail": "Magia deletada com sucesso"}