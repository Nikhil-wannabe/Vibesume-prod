"""
Resume analysis API router
Handles upload, parsing, and analysis of resume files
"""

from fastapi import APIRouter, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import os
import uuid
from pathlib import Path
import logging

from app.services.resume_parser import ResumeParser
from app.services.llm_service import LLMService
from app.models.resume_models import JobDescription, AnalysisResult

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
resume_parser = ResumeParser()
llm_service = LLMService()

# LLM service will be initialized in main.py startup event

# Ensure upload directory exists
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/upload", response_model=dict)
async def upload_resume(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    job_description: str = Form(None),
    job_url: str = Form(None)
):
    """Upload and analyze a resume file"""
    
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
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_path = UPLOAD_DIR / f"{file_id}{file_ext}"
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Parse resume
        resume_data = await resume_parser.parse_resume(str(file_path))
        
        # Initialize LLM service if not already done
        if not llm_service.is_available:
            await llm_service.initialize()
        
        # Prepare job description for analysis if provided
        job_desc = None
        if job_description:
            job_desc = JobDescription(
                title="Target Position",
                description=job_description,
                required_skills=[],  # Could be extracted from description
                url=job_url if job_url else None
            )
        
        # Analyze resume
        analysis = await llm_service.analyze_resume(resume_data, job_desc)
        
        # Get skill gap analysis if job description provided
        skill_gap = None
        if job_desc:
            skill_gap = await llm_service.get_skill_gap_analysis(resume_data, job_desc)
        
        # Get vibe check feedback
        vibe_feedback = await llm_service.vibe_check_feedback(resume_data, job_url)
        
        # Schedule file cleanup
        background_tasks.add_task(cleanup_file, file_path)
        
        return {
            "file_id": file_id,
            "resume_data": resume_data.model_dump(),
            "analysis": analysis.model_dump(),
            "skill_gap": skill_gap,
            "vibe_feedback": vibe_feedback,
            "message": "Resume analyzed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error processing resume: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

@router.post("/analyze", response_model=dict)
async def analyze_resume_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    job_description: str = Form(None),
    job_url: str = Form(None)
):
    """Analyze a resume file - main endpoint called by frontend"""
    
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
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_path = UPLOAD_DIR / f"{file_id}{file_ext}"
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Parse resume
        resume_data = await resume_parser.parse_resume(str(file_path))
        
        # Initialize LLM service if not already done
        if not llm_service.is_available:
            await llm_service.initialize()
        
        # Prepare job description for analysis if provided
        job_desc = None
        if job_description and job_description.strip():
            # Extract skills from job description (simple keyword extraction)
            common_skills = ['python', 'javascript', 'react', 'node.js', 'sql', 'aws', 'docker', 'kubernetes', 'git', 'agile']
            description_lower = job_description.lower()
            found_skills = [skill for skill in common_skills if skill in description_lower]
            
            job_desc = JobDescription(
                title="Target Position",
                company="Target Company",
                description=job_description.strip(),
                required_skills=found_skills[:5],  # Top 5 found skills
                preferred_skills=found_skills[5:],  # Additional skills
                url=job_url.strip() if job_url and job_url.strip() else None
            )
        
        # Analyze resume (works with or without job description)
        analysis = await llm_service.analyze_resume(resume_data, job_desc)
        
        # Get skill gap analysis if job description provided
        skill_gap = None
        if job_desc:
            skill_gap = await llm_service.get_skill_gap_analysis(resume_data, job_desc)
        
        # Get vibe check feedback
        vibe_feedback = await llm_service.vibe_check_feedback(resume_data, job_url)
        
        # Schedule file cleanup
        background_tasks.add_task(cleanup_file, file_path)
        
        return {
            "success": True,
            "file_id": file_id,
            "score": analysis.score,
            "strengths": analysis.strengths,
            "weaknesses": analysis.weaknesses,
            "suggestions": analysis.suggestions,
            "missing_skills": analysis.missing_skills,
            "keyword_matches": analysis.keyword_matches,
            "skill_gap": skill_gap,
            "vibe_feedback": vibe_feedback,
            "has_job_description": job_desc is not None,
            "message": "Resume analyzed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error processing resume: {e}")
        # Clean up file if it was created
        if 'file_path' in locals() and file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

@router.post("/analyze-text")
async def analyze_resume_text(
    resume_text: str = Form(...),
    job_description: str = Form(None),
    job_url: str = Form(None)
):
    """Analyze resume from plain text input"""
    
    try:
        # For text input, we'll create a minimal resume data structure
        # This is a simplified version - in production you'd want better text parsing
        from app.models.resume_models import ResumeData, ContactInfo
        
        # Extract basic info from text (simplified)
        lines = resume_text.split('\n')
        name = lines[0] if lines else "Resume Candidate"
        
        # Create minimal resume data
        resume_data = ResumeData(
            contact_info=ContactInfo(full_name=name, email="extracted@email.com"),
            summary=resume_text[:500],  # First 500 chars as summary
            experience=[],
            education=[],
            skills=[]
        )
        
        # Prepare job description
        job_desc = None
        if job_description:
            job_desc = JobDescription(
                title="Target Position",
                description=job_description,
                url=job_url if job_url else None
            )
        
        # Analyze
        analysis = await llm_service.analyze_resume(resume_data, job_desc)
        vibe_feedback = await llm_service.vibe_check_feedback(resume_data, job_url)
        
        skill_gap = None
        if job_desc:
            skill_gap = await llm_service.get_skill_gap_analysis(resume_data, job_desc)
        
        return {
            "analysis": analysis.model_dump(),
            "skill_gap": skill_gap,
            "vibe_feedback": vibe_feedback,
            "message": "Text analysis completed"
        }
        
    except Exception as e:
        logger.error(f"Error analyzing text: {e}")
        raise HTTPException(status_code=500, detail=f"Error analyzing text: {str(e)}")

@router.post("/skill-gap")
async def analyze_skill_gap(
    job_description: str = Form(...),
    job_url: str = Form(None),
    current_skills: str = Form(...)
):
    """Analyze skill gap for a specific job description"""
    
    try:
        # Parse current skills
        skills_list = [skill.strip() for skill in current_skills.split(',')]
        
        # Create job description object
        job_desc = JobDescription(
            title="Target Position",
            description=job_description,
            required_skills=skills_list[:5],  # Use first 5 as required
            url=job_url if job_url else None
        )
        
        # Create minimal resume with current skills
        from app.models.resume_models import ResumeData, ContactInfo, Skill
        
        resume_data = ResumeData(
            contact_info=ContactInfo(full_name="User", email="user@example.com"),
            skills=[Skill(name=skill) for skill in skills_list]
        )
        
        # Get skill gap analysis
        skill_gap = await llm_service.get_skill_gap_analysis(resume_data, job_desc)
        
        return {
            "skill_gap": skill_gap,
            "message": "Skill gap analysis completed"
        }
        
    except Exception as e:
        logger.error(f"Error in skill gap analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Error in skill gap analysis: {str(e)}")

@router.get("/vibe-check/{file_id}")
async def get_vibe_check(file_id: str, job_url: str = None):
    """Get vibe check feedback for a previously uploaded resume"""
    
    # In a real application, you'd store the resume data in a database
    # For now, return a sample response
    return {
        "vibe_feedback": "Your resume has good energy! The experience section shows solid progression, but let's amp up those technical skills and add some metrics to really make it pop. Consider adding more specific achievements with numbers - that's what makes recruiters say 'wow!'",
        "message": "Vibe check completed"
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
    """Health check for resume analysis service"""
    # Initialize LLM service if not already done
    if not llm_service.is_available:
        await llm_service.initialize()
    
    return {
        "status": "healthy",
        "service": "resume_analysis",
        "llm_available": llm_service.is_available
    }
