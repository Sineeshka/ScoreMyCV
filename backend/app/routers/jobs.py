from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

@router.post("/", response_model=schemas.JobOut, status_code=status.HTTP_201_CREATED)
def create_job(job: schemas.JobCreate,
               db: Session = Depends(database.get_db),
               current_user: models.User = Depends(get_current_user)):
    new_job = models.Job(
        title=job.title,
        company=job.company,
        jd_text=job.jd_text,
        user_id=current_user.id
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/", response_model=List[schemas.JobOut])
def get_jobs(db: Session = Depends(database.get_db),
             current_user: models.User = Depends(get_current_user)):
    jobs = db.query(models.Job).filter(models.Job.user_id == current_user.id).all()
    return jobs
