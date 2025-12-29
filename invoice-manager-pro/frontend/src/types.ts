export interface Company {
    id: string;
    name: string;
}

export interface Customer {
    id: string;
    name: string;
    email?: string;
    phone?: string;
    currency: string;
    billing_address_line_1?: string;
}

export interface Item {
    id: string;
    name: string;
    description?: string;
    price: number;
    unit?: string;
}

export interface InvoiceItem {
    id?: string;
    item_id?: string;
    name: string;
    description?: string;
    quantity: number;
    price: number;
    tax: number;
    total: number;
}

export interface Invoice {
    id: string;
    invoice_number: string;
    invoice_date: string;
    due_date: string;
    status: string;
    subtotal: number;
    tax: number;
    total: number;
    customer_id: string;
    customer?: Customer;
    items?: InvoiceItem[];
    currency?: string;
    paid_status?: string;
}

export interface Estimate {
    id: string;
    pipeline_stage: 'opportunity' | 'proposal' | 'negotiation' | 'won' | 'lost';
    total: number;
    customer?: Customer;
}
