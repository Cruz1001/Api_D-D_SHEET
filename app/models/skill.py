from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    attribute = Column(String, nullable=False) 
    proficient = Column(Boolean, default=False)

    character_id = Column(Integer, ForeignKey("characters.id"))
    character = relationship("Character", back_populates="skills")
