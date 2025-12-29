from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Customer, PDFUpload # I should have CustomerNote and CustomerTask in models
from app.schemas.schemas import CRMNote, CRMNoteCreate, CRMTask, CRMTaskCreate
from uuid import UUID
import httpx
import logging

# Nota: Necesito asegurarme de que los modelos CustomerNote y CustomerTask existan en models.py
# Como no los agregué explícitamente en el paso anterior a models.py (solo a init.sql), los agregaré ahora.

router = APIRouter()
logger = logging.getLogger(__name__)

N8N_WEBHOOK_URL = "http://n8n:5678/webhook/estimate-won"

@router.get("/customers/{customer_id}/notes", response_model=List[CRMNote])
def get_customer_notes(customer_id: UUID, db: Session = Depends(get_db)):
    # Importación tardía para evitar círculos si fuera necesario
    from app.models.models import CRMNote as CRMNoteModel
    return db.query(CRMNoteModel).filter(CRMNoteModel.customer_id == customer_id).all()

@router.post("/customers/{customer_id}/notes", response_model=CRMNote)
def create_customer_note(customer_id: UUID, note: CRMNoteCreate, db: Session = Depends(get_db)):
    from app.models.models import CRMNote as CRMNoteModel
    db_note = CRMNoteModel(**note.dict(), customer_id=customer_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/customers/{customer_id}/tasks", response_model=List[CRMTask])
def get_customer_tasks(customer_id: UUID, db: Session = Depends(get_db)):
    from app.models.models import CRMTask as CRMTaskModel
    return db.query(CRMTaskModel).filter(CRMTaskModel.customer_id == customer_id).all()

@router.post("/customers/{customer_id}/tasks", response_model=CRMTask)
def create_customer_task(customer_id: UUID, task: CRMTaskCreate, db: Session = Depends(get_db)):
    from app.models.models import CRMTask as CRMTaskModel
    db_task = CRMTaskModel(**task.dict(), customer_id=customer_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.patch("/estimates/{estimate_id}/status")
async def update_estimate_status(estimate_id: str, status: str, db: Session = Depends(get_db)):
    # Lógica simplificada para demostración
    if status == "won":
        try:
            async with httpx.AsyncClient() as client:
                await client.post(N8N_WEBHOOK_URL, json={
                    "event": "estimate.won",
                    "estimate_id": estimate_id,
                    "timestamp": "2025-12-23"
                })
                logger.info("Automation triggered in n8n")
        except Exception as e:
            logger.error(f"Failed to trigger n8n: {e}")
            
    return {"status": "updated"}
