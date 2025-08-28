from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String, unique=True,index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    resumes = relationship("Resume", back_populates="owner")
    jobs = relationship("Job", back_populates="owner")

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    raw_text = Column(Text)
    parsed_json = Column(Text)
    created_at = Column(DateTime,default=datetime.now(timezone.utc))

    owner = relationship("User", back_populates="resumes")
    scores = relationship("Score", back_populates="resume")

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    company = Column(String)
    jd_text = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    owner = relationship("User", back_populates="jobs")
    scores = relationship("Score", back_populates="job")

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    total_score = Column(Float)
    skills_score = Column(Float)
    experience_score = Column(Float)
    education_score = Column(Float)
    semantic_score = Column(Float)
    matched_keywords = Column(Text)
    missing_keywords = Column(Text)
    suggestions = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    resume = relationship("Resume", back_populates="scores")
    job = relationship("Job", back_populates="scores")