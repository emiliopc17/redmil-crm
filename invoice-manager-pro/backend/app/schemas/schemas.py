from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID

# Shared
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Customer
class CustomerBase(BaseSchema):
    name: str
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    currency: str = "USD"
    billing_address_line_1: Optional[str] = None
    billing_city: Optional[str] = None
    billing_country: Optional[str] = None

class CustomerCreate(CustomerBase):
    company_id: Optional[UUID] = None

class Customer(CustomerBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

# Item/Product
class ItemBase(BaseSchema):
    name: str
    description: Optional[str] = None
    unit: Optional[str] = None
    price: float
    sku: Optional[str] = None
    category: Optional[str] = None

class ItemCreate(ItemBase):
    company_id: Optional[UUID] = None

class Item(ItemBase):
    id: UUID
    created_at: datetime

# Invoice Item
class InvoiceItemBase(BaseSchema):
    name: str
    description: Optional[str] = None
    quantity: float
    price: float
    discount: float = 0.0
    tax: float = 0.0
    total: float

class InvoiceItemCreate(InvoiceItemBase):
    item_id: Optional[UUID] = None

class InvoiceItem(InvoiceItemBase):
    id: UUID
    invoice_id: UUID

# Invoice
class InvoiceBase(BaseSchema):
    invoice_number: str
    invoice_date: date
    due_date: date
    status: str = "draft"
    subtotal: float
    discount: float = 0.0
    tax: float = 0.0
    total: float
    notes: Optional[str] = None
    terms: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    customer_id: UUID
    company_id: Optional[UUID] = None
    items: List[InvoiceItemCreate]

class InvoiceUpdate(BaseModel):
    status: Optional[str] = None
    paid_status: Optional[str] = None

class Invoice(InvoiceBase):
    id: UUID
    customer_id: UUID
    paid_status: str
    items: List[InvoiceItem]
    created_at: datetime

# PDF Upload
class PDFUploadBase(BaseSchema):
    filename: str
    upload_type: str
    processing_status: str

class PDFUpload(PDFUploadBase):
    id: UUID
    extracted_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime

# CRM Notes
class CRMNoteBase(BaseSchema):
    content: str

class CRMNoteCreate(CRMNoteBase):
    customer_id: UUID

class CRMNote(CRMNoteBase):
    id: UUID
    created_at: datetime

# CRM Tasks
class CRMTaskBase(BaseSchema):
    title: str
    description: Optional[str] = None
    due_date: datetime
    status: str = "pending"
    priority: str = "medium"

class CRMTaskCreate(CRMTaskBase):
    customer_id: UUID

class CRMTask(CRMTaskBase):
    id: UUID
    created_at: datetime
