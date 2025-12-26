from pydantic import BaseModel

class SpellSlotBase(BaseModel):
    level: int
    total: int
    used: int = 0

class SpellSlotCreate(SpellSlotBase):
    pass

class SpellSlotUpdate(BaseModel):
    total: int | None = None
    used: int | None = None

class SpellSlotResponse(SpellSlotBase):
    id: int

    class Config:
        from_attributes = True
        
class SpellSlotDelta(BaseModel):
    delta: int