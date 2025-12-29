-- Invoice Manager Pro Database Schema
-- Based on Crater Invoice Management System

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Companies/Organizations Table
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    logo VARCHAR(500),
    address_line_1 VARCHAR(255),
    address_line_2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    zip_code VARCHAR(20),
    phone VARCHAR(50),
    email VARCHAR(255),
    website VARCHAR(255),
    currency VARCHAR(10) DEFAULT 'USD',
    fiscal_year VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user', -- admin, user, viewer
    avatar VARCHAR(500),
    phone VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers/Clients Table
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    website VARCHAR(255),
    billing_address_line_1 VARCHAR(255),
    billing_address_line_2 VARCHAR(255),
    billing_city VARCHAR(100),
    billing_state VARCHAR(100),
    billing_country VARCHAR(100),
    billing_zip_code VARCHAR(20),
    shipping_address_line_1 VARCHAR(255),
    shipping_address_line_2 VARCHAR(255),
    shipping_city VARCHAR(100),
    shipping_state VARCHAR(100),
    shipping_country VARCHAR(100),
    shipping_zip_code VARCHAR(20),
    currency VARCHAR(10) DEFAULT 'USD',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tax Types Table
CREATE TABLE tax_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    percent DECIMAL(5, 2) NOT NULL,
    compound_tax BOOLEAN DEFAULT FALSE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Items/Products Table
CREATE TABLE items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    unit VARCHAR(50), -- piece, hour, kg, etc.
    price DECIMAL(15, 2) NOT NULL,
    sku VARCHAR(100),
    category VARCHAR(100),
    tax_id UUID REFERENCES tax_types(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Invoices Table
CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    invoice_number VARCHAR(100) UNIQUE NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'draft', -- draft, sent, viewed, overdue, paid
    subtotal DECIMAL(15, 2) DEFAULT 0.00,
    discount DECIMAL(15, 2) DEFAULT 0.00,
    discount_type VARCHAR(20) DEFAULT 'fixed', -- fixed, percentage
    tax DECIMAL(15, 2) DEFAULT 0.00,
    total DECIMAL(15, 2) DEFAULT 0.00,
    notes TEXT,
    terms TEXT,
    paid_status VARCHAR(50) DEFAULT 'unpaid', -- unpaid, partial, paid
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Invoice Items Table
CREATE TABLE invoice_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_id UUID REFERENCES invoices(id) ON DELETE CASCADE,
    item_id UUID REFERENCES items(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    quantity DECIMAL(10, 2) NOT NULL,
    price DECIMAL(15, 2) NOT NULL,
    discount DECIMAL(15, 2) DEFAULT 0.00,
    discount_type VARCHAR(20) DEFAULT 'fixed',
    tax DECIMAL(15, 2) DEFAULT 0.00,
    total DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payments Table
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    invoice_id UUID REFERENCES invoices(id) ON DELETE CASCADE,
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    payment_number VARCHAR(100) UNIQUE NOT NULL,
    payment_date DATE NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    payment_method VARCHAR(50), -- cash, check, credit_card, bank_transfer
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Estimates/Quotes Table
CREATE TABLE estimates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    estimate_number VARCHAR(100) UNIQUE NOT NULL,
    estimate_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'draft', -- draft, sent, viewed, expired, accepted, rejected
    subtotal DECIMAL(15, 2) DEFAULT 0.00,
    discount DECIMAL(15, 2) DEFAULT 0.00,
    discount_type VARCHAR(20) DEFAULT 'fixed',
    tax DECIMAL(15, 2) DEFAULT 0.00,
    total DECIMAL(15, 2) DEFAULT 0.00,
    notes TEXT,
    terms TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Estimate Items Table
CREATE TABLE estimate_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estimate_id UUID REFERENCES estimates(id) ON DELETE CASCADE,
    item_id UUID REFERENCES items(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    quantity DECIMAL(10, 2) NOT NULL,
    price DECIMAL(15, 2) NOT NULL,
    discount DECIMAL(15, 2) DEFAULT 0.00,
    discount_type VARCHAR(20) DEFAULT 'fixed',
    tax DECIMAL(15, 2) DEFAULT 0.00,
    total DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PDF Uploads Table (for Docling processing)
CREATE TABLE pdf_uploads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    upload_type VARCHAR(50), -- price_list, invoice, receipt, etc.
    processing_status VARCHAR(50) DEFAULT 'pending', -- pending, processing, completed, failed
    extracted_data JSONB,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Currency Exchange Rates Table
CREATE TABLE exchange_rates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    from_currency VARCHAR(10) NOT NULL,
    to_currency VARCHAR(10) NOT NULL,
    rate DECIMAL(15, 6) NOT NULL,
    effective_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Settings/Preferences Table
CREATE TABLE settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    key VARCHAR(100) NOT NULL,
    value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, key)
);

-- Indexes for performance
CREATE INDEX idx_invoices_customer ON invoices(customer_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_date ON invoices(invoice_date);
CREATE INDEX idx_payments_invoice ON payments(invoice_id);
CREATE INDEX idx_customers_company ON customers(company_id);
CREATE INDEX idx_items_company ON items(company_id);
CREATE INDEX idx_pdf_uploads_company ON pdf_uploads(company_id);
-- --- CRM MODULE TABLES ---

-- Customer Tags Table
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(20) DEFAULT '#1DB954', -- Spotify Green por defecto
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customer-Tag Mapping
CREATE TABLE customer_tags (
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (customer_id, tag_id)
);

-- Customer Notes (Seguimiento)
CREATE TABLE customer_notes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customer Reminders / Tasks
CREATE TABLE customer_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- pending, completed, cancelled
    priority VARCHAR(20) DEFAULT 'medium', -- low, medium, high
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pipeline Stages (For Kanban)
ALTER TABLE estimates ADD COLUMN IF NOT EXISTS pipeline_stage VARCHAR(50) DEFAULT 'prospecting';
-- Stages: prospecting, proposal_sent, negotiation, won, lost

-- Notification Webhooks (For n8n)
CREATE TABLE webhooks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    event_type VARCHAR(100) NOT NULL, -- estimate.won, invoice.paid, etc.
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample Tags
INSERT INTO tags (company_id, name, color)
SELECT id, 'VIP', '#FFD700' FROM companies WHERE email = 'admin@redmil.hn';
INSERT INTO tags (company_id, name, color)
SELECT id, 'Corporativo', '#1DB954' FROM companies WHERE email = 'admin@redmil.hn';
INSERT INTO tags (company_id, name, color)
SELECT id, 'Nuevo', '#2E9AFE' FROM companies WHERE email = 'admin@redmil.hn';

-- Insert default admin user (password: admin123)
INSERT INTO users (company_id, first_name, last_name, email, password_hash, role)
SELECT id, 'Admin', 'User', 'admin@invoice.pro', 
       '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYXqK3J5xCi', 'admin'
FROM companies WHERE email = 'admin@redmil.hn';

-- Insert sample tax types
INSERT INTO tax_types (company_id, name, percent)
SELECT id, 'ISV (15%)', 15.00 FROM companies WHERE email = 'admin@redmil.hn';

INSERT INTO tax_types (company_id, name, percent)
SELECT id, 'IVA (16%)', 16.00 FROM companies WHERE email = 'admin@redmil.hn';

-- Insert sample items
INSERT INTO items (company_id, name, description, unit, price)
SELECT id, 'Consultoría de Software', 'Servicio de consultoría técnica', 'hora', 50.00
FROM companies WHERE email = 'admin@redmil.hn';

INSERT INTO items (company_id, name, description, unit, price)
SELECT id, 'Desarrollo Web', 'Desarrollo de aplicación web personalizada', 'proyecto', 5000.00
FROM companies WHERE email = 'admin@redmil.hn';
