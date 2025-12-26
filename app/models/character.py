from sqlalchemy import Column, Integer, String
from sqlalchemy.types import JSON
from app.database import Base
from sqlalchemy.orm import relationship

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, nullable=False)
    classes = Column(JSON, nullable=False)  # lista de {"name": ..., "level": ...}
    background = Column(String, nullable=False)
    race = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    xp = Column(Integer, default=0)
    proficiency_bonus = Column(Integer, nullable=False)
    armor_class = Column(Integer, nullable=False)
    hit_points = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    size = Column(String, nullable=False)
    passive_perception = Column(Integer, nullable=False)
    quote = Column(String, default="")

    strength = Column(Integer, nullable=False)
    dexterity = Column(Integer, nullable=False)
    constitution = Column(Integer, nullable=False)
    intelligence = Column(Integer, nullable=False)
    wisdom = Column(Integer, nullable=False)
    charisma = Column(Integer, nullable=False)

    proficiency_bonus = Column(Integer)

    
    skills = relationship(
        "Skill",
        back_populates="character",
        cascade="all, delete"
    )
    
    abilities = relationship(
        "Ability",
        back_populates="character",
        cascade="all, delete-orphan"
    )
    
    inventory = relationship(
    "Item",
    back_populates="character",
    cascade="all, delete-orphan"
    )
    
    spells = relationship(
    "Spell",
    back_populates="character",
    cascade="all, delete-orphan"
    )
    
    spell_slots = relationship(
    "SpellSlot",
    back_populates="character",
    cascade="all, delete-orphan"
    )

