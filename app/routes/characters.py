from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.character import Character
from app.models.skill import Skill
from app.models.ability import Ability

from app.schemas.character import CharacterCreate, CharacterResponse, CharacterUpdate
from app.schemas.ability import AbilityCreate, AbilityResponse

from app.services.skills import generate_skills, generate_saving_throws
from app.services.level import calculate_level
from app.services.proeficiency import calculate_proficiency_bonus
from app.models.saving_throw import SavingThrow

router = APIRouter(prefix="/characters", tags=["characters"])

@router.post("/", response_model=CharacterResponse)
def create_character(character: CharacterCreate, db: Session = Depends(get_db)):
    # gera todas as skills automaticamente
    skills_schema = generate_skills(character)
    saves_schema = generate_saving_throws(character) # Sua função do services/skills.py
    # converte schema -> model ORM
    skills = [
        Skill(
            name=skill.name,
            attribute=skill.attribute,
            proficient=skill.proficient
        )
        for skill in skills_schema
    ]
    # ADICIONE ISSO:
    from app.models.saving_throw import SavingThrow # Importe o novo model
    saving_throws = [
        SavingThrow(name=s.name, attribute=s.attribute, proficient=s.proficient) 
        for s in saves_schema
    ]
    # soma o nível total baseado nas classes
    total_level = sum(cls.level for cls in character.classes)

    # calcula o bônus de proficiência
    proficiency_bonus = calculate_proficiency_bonus(total_level)

    db_character = Character(
    name=character.name,
    race=character.race,
    classes=[cls.dict() for cls in character.classes],
    quote=character.quote,
    #saving_throws=[st.dict() for st in character.saving_throws],
    spell_casting_ability=character.spell_casting_ability,
    background=character.background,
    level=total_level,
    xp=character.xp,
    proficiency_bonus=proficiency_bonus,
    armor_class=character.armor_class,
    hit_points=character.hit_points,
    speed=character.speed,
    size=character.size,
    passive_perception=character.passive_perception,
    strength=character.strength,
    dexterity=character.dexterity,
    constitution=character.constitution,
    intelligence=character.intelligence,
    wisdom=character.wisdom,
    charisma=character.charisma,
    max_hit_points=character.max_hit_points,
    skills=skills,
    saving_throws=saving_throws
    )


    db.add(db_character)
    db.commit()
    db.refresh(db_character)

    return db_character

# GET /characters
@router.get("/", response_model=list[CharacterResponse])
def list_characters(db: Session = Depends(get_db)):
    return db.query(Character).all()

# GET /characters/{id}
@router.get("/{character_id}", response_model=CharacterResponse)
def get_character(character_id: int, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    # Se o personagem antigo não tem o campo gravado no banco
    if not character.saving_throws:
        saves_schema = generate_saving_throws(character)
        character.saving_throws = [
            SavingThrow(name=s.name, attribute=s.attribute, proficient=s.proficient) 
            for s in saves_schema
        ]
        db.commit() # Salva eles permanentemente no banco
        db.refresh(character)
        
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@router.patch("/{character_id}", response_model=CharacterResponse)
def update_character(character_id: int, payload: CharacterUpdate, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    data = payload.model_dump(exclude_unset=True)

    for key, value in data.items():
        if key != "skills":
            setattr(character, key, value)

    if "xp" in data:
        character.level = calculate_level(character.xp)
        character.proficiency_bonus = calculate_proficiency_bonus(character.level)

    db.commit()
    db.refresh(character)
    return character


# DELETE /characters/{id}
@router.delete("/{character_id}", response_model=dict)
def delete_character(character_id: int, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    db.delete(character)
    db.commit()
    return {"detail": "Character deleted"}

# PATCH /characters/{id}/skills/{skill_name}
@router.patch("/{character_id}/skills/{skill_name}", response_model=CharacterResponse)
def update_skill(character_id: int, skill_name: str, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    skill = next((s for s in character.skills if s.name == skill_name), None)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    skill.proficient = not skill.proficient
    db.commit()
    db.refresh(character)

    return character


@router.post("/{character_id}/abilities", response_model=AbilityResponse)
def add_ability(
    character_id: int,
    ability: AbilityCreate,
    db: Session = Depends(get_db)
):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    db_ability = Ability(
        name=ability.name,
        description=ability.description,
        character=character
    )

    db.add(db_ability)
    db.commit()
    db.refresh(db_ability)

    return db_ability

@router.get(
    "/{character_id}/abilities",
    response_model=list[AbilityResponse]
)
def get_abilities(character_id: int, db: Session = Depends(get_db)):
    abilities = (
        db.query(Ability)
        .filter(Ability.character_id == character_id)
        .all()
    )
    return abilities

@router.delete("/{character_id}/abilities/{ability_id}", response_model=dict)
def delete_ability(
    character_id: int,
    ability_id: int,
    db: Session = Depends(get_db)
):
    # Busca a habilidade vinculada ao personagem específico
    ability = db.query(Ability).filter(
        Ability.id == ability_id,
        Ability.character_id == character_id
    ).first()

    if not ability:
        raise HTTPException(status_code=404, detail="Habilidade não encontrada")

    db.delete(ability)
    db.commit()
    
    return {"detail": "Habilidade deletada com sucesso"}
@router.patch("/{character_id}/saving-throws/{save_name}", response_model=CharacterResponse)
def update_saving_throw(character_id: int, save_name: str, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # Busca o save específico na lista do personagem
    save = next((s for s in character.saving_throws if s.name == save_name), None)
    if not save:
        raise HTTPException(status_code=404, detail="Saving Throw not found")

    save.proficient = not save.proficient # Inverte o estado
    db.commit()
    db.refresh(character)

    return character