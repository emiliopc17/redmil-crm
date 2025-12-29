from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Customer
from app.schemas.schemas import CustomerCreate, Customer as CustomerSchema
from uuid import UUID

router = APIRouter()

@router.get("/", response_model=List[CustomerSchema])
def get_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()

@router.post("/", response_model=CustomerSchema)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/{customer_id}", response_model=CustomerSchema)
def get_customer(customer_id: UUID, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return customer
