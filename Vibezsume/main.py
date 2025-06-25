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

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(resume_analysis.router, prefix="/api/resume", tags=["Resume Analysis"])
app.include_router(resume_builder.router, prefix="/api/builder", tags=["Resume Builder"])
app.include_router(ats_validator.router, prefix="/api/ats", tags=["ATS Validator"])

# Initialize LLM service
llm_service = LLMService()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Vibezsume is running"}

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        await llm_service.initialize()
        print("✅ LLM Service initialized successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize LLM service: {e}")
        print("The application will run with limited functionality.")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
