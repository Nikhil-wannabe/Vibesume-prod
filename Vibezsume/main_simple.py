"""
Vibezsume - Simple Resume Analysis API
Simplified version for production deployment
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import tempfile
import PyPDF2
from io import BytesIO
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Vibezsume",
    description="AI-Powered Resume Analysis Platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple LLM service class
class SimpleLLMService:
    def __init__(self):
        self.is_available = True

    def extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_file = BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            return ""

    def analyze_resume(self, text: str) -> dict:
        """Analyze resume text and return structured data"""
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        # Extract phone
        phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phones = re.findall(phone_pattern, text)
        
        # Extract name (first line that looks like a name)
        lines = text.split('\n')
        name = ""
        for line in lines[:5]:
            line = line.strip()
            if line and '@' not in line and len(line.split()) <= 3 and len(line) > 2:
                name = line
                break
        
        # Simple keyword extraction for skills
        tech_keywords = [
            'python', 'javascript', 'java', 'react', 'node.js', 'sql', 'aws', 'docker',
            'git', 'html', 'css', 'mongodb', 'postgresql', 'kubernetes', 'jenkins',
            'machine learning', 'data science', 'api', 'rest', 'microservices'
        ]
        
        text_lower = text.lower()
        found_skills = [skill for skill in tech_keywords if skill in text_lower]
        
        # Extract experience years
        experience_years = 0
        exp_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'experience.*?(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*in'
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                try:
                    experience_years = max(experience_years, int(matches[0]))
                except:
                    pass
        
        # Determine career level
        if experience_years >= 8:
            career_level = "Senior"
        elif experience_years >= 3:
            career_level = "Mid-level"
        elif experience_years >= 1:
            career_level = "Junior"
        else:
            career_level = "Entry-level"
        
        return {
            "name": name or "Not specified",
            "email": emails[0] if emails else "Not specified",
            "phone": f"({phones[0][1]}) {phones[0][2]}-{phones[0][3]}" if phones else "Not specified",
            "experience_years": experience_years,
            "career_level": career_level,
            "skills": found_skills[:10],
            "strengths": [
                "Clear technical background",
                "Relevant industry experience",
                "Good skill diversity"
            ],
            "recommendations": [
                "Add quantifiable achievements",
                "Include project descriptions",
                "Optimize for ATS keywords",
                "Consider adding certifications"
            ],
            "summary": f"Experienced {career_level.lower()} professional with {experience_years} years in the field.",
            "mode": "Demo mode - Enhanced analysis available with full AI integration"
        }

    def validate_ats(self, text: str) -> dict:
        """Validate resume for ATS compatibility"""
        issues = []
        score = 85
        
        if len(text) < 200:
            issues.append("Resume content is too short")
            score -= 15
            
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            issues.append("No email address found")
            score -= 10
            
        structure_keywords = ['experience', 'education', 'skills', 'summary']
        found_sections = sum(1 for keyword in structure_keywords if keyword.lower() in text.lower())
        
        if found_sections < 3:
            issues.append("Missing key resume sections")
            score -= 10
        
        return {
            "ats_score": max(score, 0),
            "issues": issues,
            "recommendations": [
                "Use standard section headings",
                "Include relevant keywords",
                "Use simple formatting",
                "Save as both PDF and plain text"
            ],
            "keyword_density": "Moderate",
            "formatting_score": 90
        }

    def analyze_job_fit(self, resume_text: str, job_text: str) -> dict:
        """Analyze job fit"""
        resume_words = set(resume_text.lower().split())
        job_words = set(job_text.lower().split())
        
        common_words = resume_words.intersection(job_words)
        match_percentage = min(len(common_words) / len(job_words) * 100, 95) if job_words else 0
        
        return {
            "match_percentage": round(match_percentage),
            "matched_keywords": list(common_words)[:15],
            "missing_keywords": list(job_words - resume_words)[:10],
            "recommendations": [
                "Include more job-specific keywords",
                "Highlight relevant experience",
                "Tailor skills section to job requirements"
            ],
            "vibe_check": f"{'Strong' if match_percentage > 70 else 'Moderate' if match_percentage > 40 else 'Weak'} alignment with job requirements"
        }

# Initialize service
llm_service = SimpleLLMService()

@app.get("/")
async def read_root():
    """Root endpoint"""
    return {"message": "Vibezsume API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Health check endpoint for Render"""
    return {
        "status": "healthy",
        "message": "Vibezsume API is running",
        "llm_available": llm_service.is_available,
        "features": ["resume_analysis", "ats_validation", "job_analysis", "resume_comparison"]
    }

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and analyze resume"""
    if not file.filename.lower().endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")
    
    try:
        contents = await file.read()
        
        # Extract text
        if file.filename.lower().endswith('.pdf'):
            text = llm_service.extract_text_from_pdf(contents)
        else:
            text = contents.decode('utf-8')
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from file")
        
        # Analyze resume
        analysis = llm_service.analyze_resume(text)
        
        return {
            "filename": file.filename,
            "extracted_text": text[:500] + "..." if len(text) > 500 else text,
            "analysis": analysis,
            "message": "Resume analyzed successfully"
        }
        
    except Exception as e:
        logger.error(f"Resume analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/validate_ats")
async def validate_ats(file: UploadFile = File(...)):
    """Validate resume for ATS compatibility"""
    if not file.filename.lower().endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")
    
    try:
        contents = await file.read()
        
        if file.filename.lower().endswith('.pdf'):
            text = llm_service.extract_text_from_pdf(contents)
        else:
            text = contents.decode('utf-8')
        
        validation = llm_service.validate_ats(text)
        
        return {
            "filename": file.filename,
            "validation": validation,
            "message": "ATS validation completed"
        }
        
    except Exception as e:
        logger.error(f"ATS validation error: {e}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@app.post("/compare_resume_job")
async def compare_resume_job(
    resume_file: UploadFile = File(...),
    job_title: str = Form(...),
    job_description: str = Form(...)
):
    """Compare resume against job description"""
    try:
        contents = await resume_file.read()
        
        if resume_file.filename.lower().endswith('.pdf'):
            resume_text = llm_service.extract_text_from_pdf(contents)
        else:
            resume_text = contents.decode('utf-8')
        
        job_text = f"{job_title} {job_description}"
        comparison = llm_service.analyze_job_fit(resume_text, job_text)
        
        return {
            "resume_filename": resume_file.filename,
            "job_title": job_title,
            "comparison": comparison,
            "message": "Comparison completed"
        }
        
    except Exception as e:
        logger.error(f"Comparison error: {e}")
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

@app.post("/analyze_job_skills")
async def analyze_job_skills(
    job_title: str = Form(...),
    job_description: str = Form(...)
):
    """Analyze job requirements and extract skills"""
    try:
        job_text = f"{job_title} {job_description}".lower()
        
        # Extract common tech skills from job description
        tech_keywords = [
            'python', 'javascript', 'java', 'react', 'node.js', 'sql', 'aws', 'docker',
            'git', 'html', 'css', 'mongodb', 'postgresql', 'kubernetes', 'jenkins',
            'machine learning', 'data science', 'api', 'rest', 'microservices'
        ]
        
        found_skills = [skill for skill in tech_keywords if skill in job_text]
        
        # Extract experience requirements
        exp_match = re.search(r'(\d+)\+?\s*years?\s*(?:of\s*)?experience', job_text)
        required_experience = int(exp_match.group(1)) if exp_match else 0
        
        return {
            "job_title": job_title,
            "analysis": {
                "required_skills": found_skills,
                "experience_required": required_experience,
                "key_responsibilities": [
                    "Develop and maintain applications",
                    "Collaborate with team members",
                    "Write clean, efficient code",
                    "Participate in code reviews"
                ],
                "recommendations": [
                    "Highlight relevant experience",
                    "Include matching keywords",
                    "Quantify achievements",
                    "Show impact of your work"
                ]
            },
            "message": "Job analysis completed"
        }
        
    except Exception as e:
        logger.error(f"Job analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
