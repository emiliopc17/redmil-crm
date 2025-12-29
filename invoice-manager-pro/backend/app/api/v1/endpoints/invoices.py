from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Invoice, InvoiceItem
from app.schemas.schemas import InvoiceCreate, Invoice as InvoiceSchema
from uuid import UUID

router = APIRouter()

@router.get("/", response_model=List[InvoiceSchema])
def get_invoices(db: Session = Depends(get_db)):
    return db.query(Invoice).all()

@router.post("/", response_model=InvoiceSchema)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    invoice_data = invoice.dict(exclude={"items"})
    db_invoice = Invoice(**invoice_data)
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    
    for item in invoice.items:
        db_item = InvoiceItem(**item.dict(), invoice_id=db_invoice.id)
        db.add(db_item)
    
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

@router.get("/{invoice_id}", response_model=InvoiceSchema)
def get_invoice(invoice_id: UUID, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return invoice
