from pydantic import BaseModel

class AbilityBase(BaseModel):
    name: str
    description: str

class AbilityCreate(AbilityBase):
    pass

class AbilityResponse(AbilityBase):
    id: int

    class Config:
        from_attributes = True
