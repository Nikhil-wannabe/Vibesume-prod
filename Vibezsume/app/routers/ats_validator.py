"""
ATS Validator API router
Handles ATS compatibility validation of resumes
"""

from fastapi import APIRouter, File, UploadFile, Form, HTTPException, BackgroundTasks
from pathlib import Path
import uuid
import logging

from app.services.ats_validator import ATSValidator
from app.services.resume_parser import ResumeParser

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
ats_validator = ATSValidator()
resume_parser = ResumeParser()

# Upload settings
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/validate")
async def validate_resume_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """Validate ATS compatibility of uploaded resume file"""
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size: 10MB")
    
    try:
        # Save uploaded file temporarily
        file_id = str(uuid.uuid4())
        file_path = UPLOAD_DIR / f"{file_id}{file_ext}"
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Extract text for analysis
        resume_text = await resume_parser._extract_text_from_file(str(file_path))
        
        if not resume_text:
            raise HTTPException(status_code=400, detail="Could not extract text from file")
        
        # Perform ATS validation
        validation_result = await ats_validator.validate_resume(str(file_path), resume_text)
        
        # Schedule file cleanup
        background_tasks.add_task(cleanup_file, file_path)
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "validation_result": validation_result.dict(),
            "message": "ATS validation completed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error validating resume: {e}")
        raise HTTPException(status_code=500, detail=f"Error validating resume: {str(e)}")

@router.post("/validate-text")
async def validate_resume_text(
    resume_text: str = Form(...),
    filename: str = Form("resume.txt")
):
    """Validate ATS compatibility of resume text"""
    
    try:
        # Create a temporary text file for validation
        file_id = str(uuid.uuid4())
        file_path = UPLOAD_DIR / f"{file_id}.txt"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(resume_text)
        
        # Perform ATS validation
        validation_result = await ats_validator.validate_resume(str(file_path), resume_text)
        
        # Clean up temp file
        file_path.unlink()
        
        return {
            "filename": filename,
            "validation_result": validation_result.dict(),
            "message": "Text validation completed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error validating text: {e}")
        raise HTTPException(status_code=500, detail=f"Error validating text: {str(e)}")

@router.post("/quick-check")
async def quick_ats_check(
    resume_text: str = Form(...),
    target_keywords: str = Form("")
):
    """Quick ATS compatibility check with keyword analysis"""
    
    try:
        # Perform basic checks without file upload
        issues = []
        score = 100.0
        
        # Basic text analysis
        word_count = len(resume_text.split())
        if word_count < 200:
            issues.append("Resume appears too short (< 200 words)")
            score -= 20
        elif word_count > 1000:
            issues.append("Resume may be too long (> 1000 words)")
            score -= 10
        
        # Check for contact information
        import re
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text):
            issues.append("No email address found")
            score -= 15
        
        if not re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', resume_text):
            issues.append("No phone number detected")
            score -= 10
        
        # Check for section headers
        section_count = len(re.findall(r'\n([A-Z][A-Z\s]{2,})\n', resume_text))
        if section_count < 2:
            issues.append("Sections may not be clearly defined")
            score -= 15
        
        # Keyword analysis
        keyword_analysis = {}
        if target_keywords:
            keywords = [kw.strip().lower() for kw in target_keywords.split(',')]
            text_lower = resume_text.lower()
            
            for keyword in keywords:
                count = text_lower.count(keyword)
                keyword_analysis[keyword] = {
                    "count": count,
                    "found": count > 0
                }
        
        return {
            "quick_score": max(score, 0),
            "word_count": word_count,
            "issues": issues,
            "keyword_analysis": keyword_analysis,
            "recommendations": [
                "Save resume as PDF or DOCX format",
                "Use standard fonts like Arial or Calibri",
                "Include clear section headers in ALL CAPS",
                "Add quantifiable achievements with numbers",
                "Include relevant keywords naturally in context"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error in quick ATS check: {e}")
        raise HTTPException(status_code=500, detail=f"Error in quick check: {str(e)}")

@router.get("/best-practices")
async def get_ats_best_practices():
    """Get ATS best practices and guidelines"""
    
    return {
        "formatting": {
            "file_formats": ["PDF", "DOCX"],
            "fonts": ["Arial", "Calibri", "Times New Roman", "Helvetica"],
            "font_size": "10-12pt for body text, 14-16pt for headers",
            "margins": "0.5-1 inch on all sides"
        },
        "structure": {
            "required_sections": ["Contact Information", "Professional Experience", "Education", "Skills"],
            "optional_sections": ["Summary/Objective", "Projects", "Certifications", "Awards"],
            "section_order": ["Contact", "Summary", "Experience", "Education", "Skills"]
        },
        "content": {
            "use_keywords": "Include relevant job keywords naturally",
            "quantify_achievements": "Use numbers and percentages",
            "action_verbs": "Start bullet points with strong action verbs",
            "avoid": ["Images", "Tables", "Text boxes", "Headers/Footers", "Special characters"]
        },
        "common_mistakes": [
            "Using complex formatting or graphics",
            "Missing contact information",
            "Inconsistent formatting",
            "Too many or too few keywords",
            "Poor section organization",
            "Spelling and grammar errors"
        ],
        "tips": [
            "Keep it simple and clean",
            "Use consistent bullet points",
            "Tailor content to each job application",
            "Proofread carefully",
            "Test with different ATS systems if possible"
        ]
    }

@router.get("/keyword-suggestions")
async def get_keyword_suggestions(industry: str = "technology"):
    """Get keyword suggestions for different industries"""
    
    keyword_database = {
        "technology": [
            "Python", "Java", "JavaScript", "React", "Node.js", "SQL", "AWS", "Docker",
            "Kubernetes", "Git", "Agile", "Scrum", "API", "Database", "Cloud Computing",
            "Machine Learning", "Data Analysis", "DevOps", "CI/CD", "Microservices"
        ],
        "marketing": [
            "Digital Marketing", "SEO", "SEM", "Google Analytics", "Social Media",
            "Content Marketing", "Email Marketing", "PPC", "Brand Management",
            "Marketing Strategy", "Campaign Management", "Lead Generation"
        ],
        "finance": [
            "Financial Analysis", "Excel", "Financial Modeling", "Risk Management",
            "Investment Analysis", "Portfolio Management", "Accounting", "GAAP",
            "Financial Reporting", "Budgeting", "Forecasting", "Compliance"
        ],
        "healthcare": [
            "Patient Care", "Medical Records", "HIPAA", "Clinical Research",
            "Healthcare Administration", "Medical Terminology", "EHR", "Quality Assurance",
            "Healthcare Compliance", "Patient Safety", "Medical Coding"
        ],
        "sales": [
            "Sales Strategy", "Lead Generation", "CRM", "Customer Relationship Management",
            "Sales Forecasting", "Territory Management", "Negotiation", "Closing",
            "Account Management", "Business Development", "Sales Analytics"
        ]
    }
    
    return {
        "industry": industry,
        "keywords": keyword_database.get(industry.lower(), keyword_database["technology"]),
        "usage_tips": [
            "Use keywords naturally in context",
            "Include variations and synonyms",
            "Match job description language",
            "Don't stuff keywords unnaturally",
            "Focus on skills you actually have"
        ]
    }

async def cleanup_file(file_path: Path):
    """Background task to clean up uploaded files"""
    try:
        if file_path.exists():
            file_path.unlink()
            logger.info(f"Cleaned up file: {file_path}")
    except Exception as e:
        logger.error(f"Error cleaning up file {file_path}: {e}")

@router.get("/health")
async def health_check():
    """Health check for ATS validator service"""
    return {
        "status": "healthy",
        "service": "ats_validator",
        "supported_formats": list(ALLOWED_EXTENSIONS)
    }
