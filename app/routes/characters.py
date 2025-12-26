from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.character import Character
from app.models.skill import Skill
from app.models.ability import Ability

from app.schemas.character import CharacterCreate, CharacterResponse, CharacterUpdate
from app.schemas.ability import AbilityCreate, AbilityResponse

from app.services.skills import generate_skills
from app.services.level import calculate_level
from app.services.proeficiency import calculate_proficiency_bonus


router = APIRouter(prefix="/characters", tags=["characters"])

@router.post("/", response_model=CharacterResponse)
def create_character(character: CharacterCreate, db: Session = Depends(get_db)):
    # gera todas as skills automaticamente
    skills_schema = generate_skills(character)

    # converte schema -> model ORM
    skills = [
        Skill(
            name=skill.name,
            attribute=skill.attribute,
            proficient=skill.proficient
        )
        for skill in skills_schema
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
    skills=skills
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