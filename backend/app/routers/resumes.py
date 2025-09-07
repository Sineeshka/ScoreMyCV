from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi import UploadFile, File
from app import models, schemas, database
from app.routers.auth import get_current_user

router = APIRouter(
    prefix= "/resumes",
    tags=["Resumes"]
)

# @router.post("/", response_model=schemas.ResumeOut, status_code=status.HTTP_201_CREATED)
# def create_resume(resume: schemas.ResumeCreate,
#                   db: Session = Depends(database.get_db),
#                   current_user: models.User = Depends(get_current_user)):
#     new_resume = models.Resume(
#         filename=resume.filename,
#         raw_text=resume.raw_text,
#         parsed_json =resume.parsed_json,
#         user_id=current_user.id
#     )
#     db.add(new_resume)
#     db.commit()
#     db.refresh(new_resume)
#     return new_resume

@router.get("/",response_model=List[schemas.ResumeOut])
def get_resumes(db: Session = Depends(database.get_db),
                current_user: models.User = Depends(get_current_user)):
    resumes= db.query(models.Resume).filter(models.Resume.user_id == current_user.id).all()
    return resumes

@router.post("/upload", response_model=schemas.ResumeOut)
def upload_resume(file: UploadFile = File(...),
                  db: Session = Depends(database.get_db),
                  current_user: models.User = Depends(get_current_user)):
    #only accepts pdfs
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    from PyPDF2 import PdfReader
    import io

    #read file into memory
    pdf_bytes = io.BytesIO(file.file.read())
    reader = PdfReader(pdf_bytes)

    #extract text
    raw_text = ""
    for page in reader.pages:
        raw_text += page.extract_text() or ""
    
    #save to db
    new_resume = models.Resume(
        filename=file.filename,
        raw_text=raw_text,
        parsed_json=None,
        user_id=current_user.id
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return new_resume