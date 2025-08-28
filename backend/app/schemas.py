from pydantic import BaseModel, EmailStr
from typing import Optional,List
from datetime import datetime

#user schemas

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

#  Auth Schemas 

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None

#resume schemas

class ResumeCreate(BaseModel):
    filename: str
    raw_text: str
    parsed_json: Optional[str]

class ResumeOut(ResumeCreate):
    id: int
    score: int
    created_at: datetime

    class Config:
        from_attributes  = True

#job schemas

class JobCreate(BaseModel):
    title: str
    company: str
    jd_text: str

class JobOut(JobCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes  = True

#score schemas

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
        from_attributes  = True