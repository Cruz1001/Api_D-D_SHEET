from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SavingThrow(Base):
    __tablename__ = "saving_throws"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    attribute = Column(String)
    proficient = Column(Boolean, default=False)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"))

    character = relationship("Character", back_populates="saving_throws")