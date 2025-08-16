from pydantic import BaseModel, EmailStr
from typing import Optional,List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode= True

class ResumeCreate(BaseModel):
    filename: str
    raw_text: str
    parsed_json: Optional[str]

class ResumeOut(ResumeCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class JobCreate(BaseModel):
    title: str
    company: str
    jd_text: str

class JobOut(JobCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ScoreOut(BaseModel):
    id: int
    total_score: float
    skills_score: float
    experience_score: float
    education_score: float
    semantic_score: float
    matched_keywords: str
    missing_keywords: str
    suggestions: str
    created_at: datetime

    class Config:
        orm_mode = True