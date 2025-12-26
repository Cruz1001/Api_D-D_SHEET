from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.spell_slot import SpellSlot
from app.schemas.spell_slot import (
    SpellSlotCreate,
    SpellSlotUpdate,
    SpellSlotResponse,
    SpellSlotDelta
)

router = APIRouter(
    prefix="/characters/{character_id}/spell-slots",
    tags=["spell-slots"]
)

@router.get("/", response_model=list[SpellSlotResponse])
def list_slots(character_id: int, db: Session = Depends(get_db)):
    return db.query(SpellSlot).filter(
        SpellSlot.character_id == character_id
    ).all()

@router.post("/", response_model=SpellSlotResponse)
def create_slot(
    character_id: int,
    slot: SpellSlotCreate,
    db: Session = Depends(get_db)
):
    db_slot = SpellSlot(**slot.dict(), character_id=character_id)
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot

@router.patch("/{level}", response_model=SpellSlotResponse)
def update_spell_slot(
    character_id: int,
    level: int,
    payload: SpellSlotDelta,
    db: Session = Depends(get_db)
):
    slot = db.query(SpellSlot).filter(
        SpellSlot.character_id == character_id,
        SpellSlot.level == level
    ).first()

    if not slot:
        raise HTTPException(status_code=404, detail="Spell slot not found")

    new_used = slot.used + payload.delta

    if new_used < 0:
        raise HTTPException(
            status_code=400,
            detail="Used slots cannot be negative"
        )

    if new_used > slot.total:
        raise HTTPException(
            status_code=400,
            detail="No spell slots available"
        )

    slot.used = new_used
    db.commit()
    db.refresh(slot)
    return slot

