from fastapi import FastAPI
from app.routes.characters import router as character_router
from app.database import Base, engine
import app.models
from app.routes.inventory import router as inventory_router
from app.routes.spell_slots import router as spell_slot_router
from app.routes.spells import router as spells_router


app = FastAPI(title="Who are you?")

app.include_router(character_router)
app.include_router(inventory_router)
app.include_router(spell_slot_router)
app.include_router(spells_router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
@app.get("/ping")
def ping():
    return {"ping": "pong!"}

