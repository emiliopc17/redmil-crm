from fastapi import APIRouter
from app.api.v1.endpoints import invoices, customers, items, pdf_uploads, auth, crm

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(invoices.router, prefix="/invoices", tags=["invoices"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(pdf_uploads.router, prefix="/pdf-uploads", tags=["pdf-uploads"])
api_router.include_router(crm.router, prefix="/crm", tags=["crm"])
