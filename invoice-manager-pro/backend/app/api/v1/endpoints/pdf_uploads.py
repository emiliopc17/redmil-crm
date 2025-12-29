from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import PDFUpload
from app.services.docling_service import docling_service
from app.core.config import settings
import os
import uuid

router = APIRouter()

async def process_pdf_task(upload_id: uuid.UUID, file_path: str, db_session: Session):
    upload = db_session.query(PDFUpload).filter(PDFUpload.id == upload_id).first()
    try:
        upload.processing_status = "processing"
        db_session.commit()
        
        # Usar Docling para extraer datos
        extracted_data = await docling_service.extract_price_list(file_path)
        
        upload.extracted_data = extracted_data
        upload.processing_status = "completed"
    except Exception as e:
        upload.processing_status = "failed"
        upload.error_message = str(e)
    
    db_session.commit()

@router.post("/")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    upload_type: str = "price_list",
    db: Session = Depends(get_db)
):
    file_id = uuid.uuid4()
    file_ext = os.path.splitext(file.filename)[1]
    file_name = f"{file_id}{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, file_name)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    db_upload = PDFUpload(
        id=file_id,
        filename=file.filename,
        file_path=file_path,
        upload_type=upload_type,
        processing_status="pending"
    )
    db.add(db_upload)
    db.commit()
    
    background_tasks.add_task(process_pdf_task, file_id, file_path, db)
    
    return {"id": file_id, "status": "pending"}
