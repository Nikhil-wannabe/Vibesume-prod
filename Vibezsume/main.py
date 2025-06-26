"""
Vibezsume - Modern Resume Analysis Web Application
Entry point for the FastAPI application
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from datetime import datetime
from pathlib import Path

from app.routers import resume_analysis, resume_builder, ats_validator
from app.services.llm_service import LLMService
from app.models.resume_models import ResumeData, JobDescription

# Initialize FastAPI app
app = FastAPI(
    title="Vibezsume",
    description="AI-Powered Resume Analysis and Builder",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for your domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files if directory exists
static_dir = Path("app/static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates_dir = Path("app/templates")
if templates_dir.exists():
    templates = Jinja2Templates(directory="app/templates")
else:
    templates = None

# Include routers
app.include_router(resume_analysis.router, prefix="/api/resume", tags=["Resume Analysis"])
app.include_router(resume_builder.router, prefix="/api/builder", tags=["Resume Builder"])
app.include_router(ats_validator.router, prefix="/api/ats", tags=["ATS Validator"])

# Initialize LLM service
llm_service = LLMService()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Main page"""
    if templates:
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return {"message": "Vibezsume API", "docs": "/docs", "health": "/health"}

@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint for Render"""
    health_status = {
        "status": "healthy",
        "message": "Vibezsume API is running",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "llm_service": llm_service.is_available if llm_service else False,
            "static_files": static_dir.exists(),
            "templates": templates is not None,
        },
        "endpoints": [
            "/api/resume/upload",
            "/api/ats/validate", 
            "/api/builder/generate",
            "/docs"
        ]
    }
    return health_status

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        await llm_service.initialize()
        if llm_service.is_available:
            print("✅ LLM Service initialized successfully")
        else:
            print("ℹ️ Running in basic mode without AI features")
    except Exception as e:
        print(f"ℹ️ LLM service unavailable: {e}")
        print("The application will run with basic functionality.")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
