from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SpellSlot(Base):
    __tablename__ = "spell_slots"

    id = Column(Integer, primary_key=True)
    level = Column(Integer, nullable=False)  # 1 a 9
    total = Column(Integer, nullable=False)
    used = Column(Integer, default=0)

    character_id = Column(Integer, ForeignKey("characters.id"))
    character = relationship("Character", back_populates="spell_slots")
