"""
Resume builder API router
Handles resume building and PDF generation
"""

from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
import logging
from datetime import datetime

from app.services.pdf_builder import PDFResumeBuilder
from app.models.resume_models import ResumeBuilderRequest, ResumeData

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize PDF builder
pdf_builder = PDFResumeBuilder()

# Ensure output directory exists
OUTPUT_DIR = Path("generated_resumes")
OUTPUT_DIR.mkdir(exist_ok=True)

@router.post("/build")
async def build_resume(request: ResumeBuilderRequest):
    """Build a PDF resume from structured data"""
    
    try:
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resume_{timestamp}_{uuid.uuid4().hex[:8]}.pdf"
        output_path = OUTPUT_DIR / filename
        
        # Build the PDF
        pdf_path = await pdf_builder.build_resume(request, str(output_path))
        
        return {
            "filename": filename,
            "download_url": f"/api/builder/download/{filename}",
            "message": "Resume built successfully"
        }
        
    except Exception as e:
        logger.error(f"Error building resume: {e}")
        raise HTTPException(status_code=500, detail=f"Error building resume: {str(e)}")

@router.post("/build-from-form")
async def build_resume_from_form(
    # Contact Information
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    linkedin: str = Form(None),
    github: str = Form(None),
    portfolio: str = Form(None),
    location: str = Form(None),
    
    # Professional Summary
    summary: str = Form(None),
    
    # Experience (JSON strings)
    experience_json: str = Form("[]"),
    education_json: str = Form("[]"),
    skills_json: str = Form("[]"),
    projects_json: str = Form("[]"),
    
    # Template options
    template_style: str = Form("modern"),
    color_scheme: str = Form("blue"),
    sections_order: str = Form("summary,experience,education,skills,projects")
):
    """Build resume from form data"""
    
    try:
        import json
        from app.models.resume_models import ContactInfo, Experience, Education, Skill, Project
        
        # Parse JSON fields
        experience_data = json.loads(experience_json) if experience_json != "[]" else []
        education_data = json.loads(education_json) if education_json != "[]" else []
        skills_data = json.loads(skills_json) if skills_json != "[]" else []
        projects_data = json.loads(projects_json) if projects_json != "[]" else []
        
        # Create contact info
        contact_info = ContactInfo(
            full_name=full_name,
            email=email,
            phone=phone,
            linkedin=linkedin,
            github=github,
            portfolio=portfolio,
            location=location
        )
        
        # Create resume data structure
        resume_data = ResumeData(
            contact_info=contact_info,
            summary=summary,
            experience=[Experience(**exp) for exp in experience_data],
            education=[Education(**edu) for edu in education_data],
            skills=[Skill(**skill) for skill in skills_data],
            projects=[Project(**proj) for proj in projects_data]
        )
        
        # Create builder request
        request = ResumeBuilderRequest(
            resume_data=resume_data,
            template_style=template_style,
            color_scheme=color_scheme,
            sections_order=sections_order.split(',')
        )
        
        # Build the resume
        return await build_resume(request)
        
    except Exception as e:
        logger.error(f"Error building resume from form: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing form data: {str(e)}")

@router.get("/download/{filename}")
async def download_resume(filename: str):
    """Download a generated resume PDF"""
    
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Resume file not found")
    
    return FileResponse(
        path=str(file_path),
        media_type='application/pdf',
        filename=filename
    )

@router.get("/templates")
async def get_available_templates():
    """Get available resume templates"""
    
    return {
        "templates": pdf_builder.get_template_styles(),
        "color_schemes": pdf_builder.get_color_schemes(),
        "default_sections_order": ["summary", "experience", "education", "skills", "projects"]
    }

@router.post("/preview")
async def preview_resume_data(request: ResumeBuilderRequest):
    """Preview resume data without generating PDF"""
    
    try:
        # Return formatted preview of resume sections
        resume_data = request.resume_data
        
        preview = {
            "contact_info": {
                "name": resume_data.contact_info.full_name,
                "email": resume_data.contact_info.email,
                "phone": resume_data.contact_info.phone,
                "location": resume_data.contact_info.location
            },
            "sections": {}
        }
        
        # Add sections based on order
        for section in request.sections_order:
            if section == "summary" and resume_data.summary:
                preview["sections"]["summary"] = resume_data.summary
            elif section == "experience" and resume_data.experience:
                preview["sections"]["experience"] = [
                    {
                        "position": exp.position,
                        "company": exp.company,
                        "duration": f"{exp.start_date} - {exp.end_date or 'Present'}",
                        "description_count": len(exp.description)
                    }
                    for exp in resume_data.experience
                ]
            elif section == "education" and resume_data.education:
                preview["sections"]["education"] = [
                    {
                        "degree": edu.degree,
                        "institution": edu.institution,
                        "year": edu.end_date
                    }
                    for edu in resume_data.education
                ]
            elif section == "skills" and resume_data.skills:
                preview["sections"]["skills"] = [skill.name for skill in resume_data.skills]
            elif section == "projects" and resume_data.projects:
                preview["sections"]["projects"] = [
                    {
                        "name": proj.name,
                        "description": proj.description[:100] + "..." if len(proj.description) > 100 else proj.description
                    }
                    for proj in resume_data.projects
                ]
        
        return {
            "preview": preview,
            "template_style": request.template_style,
            "color_scheme": request.color_scheme
        }
        
    except Exception as e:
        logger.error(f"Error creating preview: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating preview: {str(e)}")

@router.delete("/cleanup")
async def cleanup_old_files():
    """Clean up old generated resume files"""
    
    try:
        import time
        
        deleted_count = 0
        current_time = time.time()
        
        # Delete files older than 24 hours
        for file_path in OUTPUT_DIR.glob("*.pdf"):
            if current_time - file_path.stat().st_mtime > 24 * 3600:  # 24 hours
                file_path.unlink()
                deleted_count += 1
        
        return {
            "deleted_files": deleted_count,
            "message": f"Cleaned up {deleted_count} old resume files"
        }
        
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
        raise HTTPException(status_code=500, detail=f"Error during cleanup: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check for resume builder service"""
    return {
        "status": "healthy",
        "service": "resume_builder",
        "output_directory": str(OUTPUT_DIR),
        "available_templates": pdf_builder.get_template_styles()
    }
