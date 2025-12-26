from pydantic import BaseModel
from typing import Optional

class SpellBase(BaseModel):
    name: str
    description: Optional[str]
    level: int
    school: Optional[str]
    prepared: bool = False

class SpellCreate(SpellBase):
    pass

class SpellUpdate(BaseModel):
    prepared: bool | None = None

class SpellResponse(SpellBase):
    id: int

    class Config:
        from_attributes = True
