from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Item
from app.schemas.schemas import ItemCreate, Item as ItemSchema
from uuid import UUID

router = APIRouter()

@router.get("/", response_model=List[ItemSchema])
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

@router.post("/", response_model=ItemSchema)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
