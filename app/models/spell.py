from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Spell(Base):
    __tablename__ = "spells"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    level = Column(Integer, nullable=False)  # 0 = cantrip
    school = Column(String, nullable=True)
    prepared = Column(Boolean, default=False)

    character_id = Column(Integer, ForeignKey("characters.id"))
    character = relationship("Character", back_populates="spells")
