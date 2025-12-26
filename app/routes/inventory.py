from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter(
    prefix="/characters/{character_id}/inventory",
    tags=["inventory"]
)

@router.get("/", response_model=list[ItemResponse])
def list_inventory(character_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Item)
        .filter(Item.character_id == character_id)
        .all()
    )

@router.post("/", response_model=ItemResponse)
def add_item(
    character_id: int,
    item: ItemCreate,
    db: Session = Depends(get_db)
):
    db_item = Item(
        **item.dict(),
        character_id=character_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(
    character_id: int,
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db)
):
    db_item = (
        db.query(Item)
        .filter(
            Item.id == item_id,
            Item.character_id == character_id
        )
        .first()
    )

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_item(
    character_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):
    db_item = (
        db.query(Item)
        .filter(
            Item.id == item_id,
            Item.character_id == character_id
        )
        .first()
    )

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"detail": "Item removed"}
