from pydantic import BaseModel
from typing import Optional, List

class ClassLevel(BaseModel):
    name: str
    level: int

class CharacterBase(BaseModel):
    name: str
    classes: list[ClassLevel]
    background: str
    race: str
    xp: int
    proficiency_bonus: int
    armor_class: int
    hit_points: int
    speed: int
    size: str
    passive_perception: int
    quote: str
    max_hit_points: Optional[int] = None
    spell_casting_ability: Optional[str] = None
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    
class Skill(BaseModel):
    name: str
    attribute: str  # força, inteligência, etc
    proficient: bool = False
    value: int = 0  # calculado

class SkillResponse(BaseModel):
    name: str
    attribute: str
    proficient: bool

    class Config:
        from_attributes = True

class CharacterCreate(CharacterBase):
    
    skills: list[Skill] = []
    pass

class CharacterResponse(CharacterBase):
    id: int
    skills: list[SkillResponse]
    
    class Config:
        from_attributes = True

class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    classes: Optional[list[ClassLevel]] = None
    background: Optional[str] = None
    race: Optional[str] = None
    xp: Optional[int] = None
    proficiency_bonus: Optional[int] = None
    armor_class: Optional[int] = None
    hit_points: Optional[int] = None
    speed: Optional[int] = None
    size: Optional[str] = None
    max_hit_points: Optional[int] = None
    passive_perception: Optional[int] = None
    spell_casting_ability: Optional[str] = None

    strength: Optional[int] = None
    dexterity: Optional[int] = None
    constitution: Optional[int] = None
    intelligence: Optional[int] = None
    wisdom: Optional[int] = None
    charisma: Optional[int] = None
        

class AbilityBase(BaseModel):
    name: str
    description: str

class AbilityCreate(AbilityBase):
    pass

class AbilityResponse(AbilityBase):
    id: int

    class Config:
        from_attributes = True