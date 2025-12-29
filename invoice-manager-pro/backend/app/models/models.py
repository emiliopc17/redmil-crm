from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Numeric, Date, Text, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    logo = Column(String(500))
    address_line_1 = Column(String(255))
    address_line_2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    zip_code = Column(String(20))
    phone = Column(String(50))
    email = Column(String(255))
    website = Column(String(255))
    currency = Column(String(10), default='USD')
    fiscal_year = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="company")
    customers = relationship("Customer", back_populates="company")
    invoices = relationship("Invoice", back_populates="company")
    items = relationship("Item", back_populates="company")


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"))
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default='user')
    avatar = Column(String(500))
    phone = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="users")
    invoices = relationship("Invoice", back_populates="user")


class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    contact_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    website = Column(String(255))
    billing_address_line_1 = Column(String(255))
    billing_address_line_2 = Column(String(255))
    billing_city = Column(String(100))
    billing_state = Column(String(100))
    billing_country = Column(String(100))
    billing_zip_code = Column(String(20))
    shipping_address_line_1 = Column(String(255))
    shipping_address_line_2 = Column(String(255))
    shipping_city = Column(String(100))
    shipping_state = Column(String(100))
    shipping_country = Column(String(100))
    shipping_zip_code = Column(String(20))
    currency = Column(String(10), default='USD')
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="customers")
    invoices = relationship("Invoice", back_populates="customer")
    payments = relationship("Payment", back_populates="customer")


class TaxType(Base):
    __tablename__ = "tax_types"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    percent = Column(Numeric(5, 2), nullable=False)
    compound_tax = Column(Boolean, default=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Item(Base):
    __tablename__ = "items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    unit = Column(String(50))
    price = Column(Numeric(15, 2), nullable=False)
    sku = Column(String(100))
    category = Column(String(100))
    tax_id = Column(UUID(as_uuid=True), ForeignKey("tax_types.id", ondelete="SET NULL"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="items")


class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    invoice_number = Column(String(100), unique=True, nullable=False)
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(String(50), default='draft')
    subtotal = Column(Numeric(15, 2), default=0.00)
    discount = Column(Numeric(15, 2), default=0.00)
    discount_type = Column(String(20), default='fixed')
    tax = Column(Numeric(15, 2), default=0.00)
    total = Column(Numeric(15, 2), default=0.00)
    notes = Column(Text)
    terms = Column(Text)
    paid_status = Column(String(50), default='unpaid')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="invoices")
    customer = relationship("Customer", back_populates="invoices")
    user = relationship("User", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="invoice")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"))
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id", ondelete="SET NULL"))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    quantity = Column(Numeric(10, 2), nullable=False)
    price = Column(Numeric(15, 2), nullable=False)
    discount = Column(Numeric(15, 2), default=0.00)
    discount_type = Column(String(20), default='fixed')
    tax = Column(Numeric(15, 2), default=0.00)
    total = Column(Numeric(15, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    invoice = relationship("Invoice", back_populates="items")


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"))
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"))
    payment_number = Column(String(100), unique=True, nullable=False)
    payment_date = Column(Date, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    payment_method = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    invoice = relationship("Invoice", back_populates="payments")
    customer = relationship("Customer", back_populates="payments")


class PDFUpload(Base):
    __tablename__ = "pdf_uploads"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String(100))
    upload_type = Column(String(50))
    processing_status = Column(String(50), default='pending')
    extracted_data = Column(JSON)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMNote(Base):
    __tablename__ = "customer_notes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMTask(Base):
    __tablename__ = "customer_tasks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    due_date = Column(DateTime, nullable=False)
    status = Column(String(50), default='pending')
    priority = Column(String(20), default='medium')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"))
    name = Column(String(50), nullable=False)
    color = Column(String(20), default='#1DB954')
    created_at = Column(DateTime, default=datetime.utcnow)

class Webhook(Base):
    __tablename__ = "webhooks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"))
    url = Column(Text, nullable=False)
    event_type = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
