"""
Pydantic models for resume data structures
"""

from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class ContactInfo(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None
    portfolio: Optional[HttpUrl] = None
    location: Optional[str] = None

class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    honors: Optional[List[str]] = []

class Experience(BaseModel):
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = None  # None for current position
    description: List[str] = []
    technologies: List[str] = []
    location: Optional[str] = None

class Skill(BaseModel):
    name: str
    level: SkillLevel = SkillLevel.INTERMEDIATE
    category: Optional[str] = None  # e.g., "Programming", "Framework", "Tool"

class Project(BaseModel):
    name: str
    description: str
    technologies: List[str] = []
    url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class Certification(BaseModel):
    name: str
    issuer: str
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[HttpUrl] = None

class ResumeData(BaseModel):
    contact_info: ContactInfo
    summary: Optional[str] = None
    education: List[Education] = []
    experience: List[Experience] = []
    skills: List[Skill] = []
    projects: List[Project] = []
    certifications: List[Certification] = []
    languages: List[str] = []
    awards: List[str] = []

class JobDescription(BaseModel):
    title: str
    company: Optional[str] = None
    description: str
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    experience_level: Optional[str] = None
    location: Optional[str] = None
    url: Optional[HttpUrl] = None

class AnalysisResult(BaseModel):
    score: float = Field(..., ge=0.0, le=100.0)
    strengths: List[str] = []
    weaknesses: List[str] = []
    suggestions: List[str] = []
    missing_skills: List[str] = []
    keyword_matches: Dict[str, bool] = {}

class ATSValidationResult(BaseModel):
    overall_score: float = Field(..., ge=0.0, le=100.0)
    formatting_issues: List[str] = []
    spacing_issues: List[str] = []
    font_issues: List[str] = []
    section_issues: List[str] = []
    keyword_optimization: Dict[str, Any] = {}
    recommendations: List[str] = []

class ResumeBuilderRequest(BaseModel):
    resume_data: ResumeData
    template_style: str = "modern"  # modern, classic, creative
    color_scheme: str = "blue"  # blue, green, purple, black
    include_photo: bool = False
    sections_order: List[str] = ["summary", "experience", "education", "skills", "projects"]
