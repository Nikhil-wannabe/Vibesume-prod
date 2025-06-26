"""
LLM Service for local language model integration
Supports Ollama and other local LLM solutions with fallback demo mode
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
import httpx
import re

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, model_name: str = "llama3.2:3b"):
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434"
        self.client = None
        self.is_available = False

    async def initialize(self):
        """Initialize the LLM service and check if Ollama is available"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.ollama_url}/api/tags")
                if response.status_code == 200:
                    models = response.json()
                    available_models = [model["name"] for model in models.get("models", [])]
                    
                    if self.model_name in available_models:
                        self.is_available = True
                        logger.info(f"LLM service initialized with model: {self.model_name}")
                    else:
                        logger.warning(f"Model {self.model_name} not found. Available models: {available_models}")
                        if available_models:
                            self.model_name = available_models[0]
                            self.is_available = True
                            logger.info(f"Using alternative model: {self.model_name}")
                else:
                    logger.error(f"Ollama server not responding: {response.status_code}")
        except Exception as e:
            logger.error(f"Could not connect to Ollama: {e}")
            logger.info("Running in demo mode with enhanced mock analysis")

    async def generate_response(self, prompt: str, system_prompt: str = None) -> str:
        """Generate response from the local LLM with fallback"""
        if not self.is_available:
            return self._fallback_response(prompt)

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                }
                
                if system_prompt:
                    payload["system"] = system_prompt

                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "").strip()
                else:
                    logger.error(f"LLM request failed: {response.status_code}")
                    return self._fallback_response(prompt)
                    
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return self._fallback_response(prompt)

    def _fallback_response(self, prompt: str) -> str:
        """Enhanced fallback response with demo analysis"""
        if "resume" in prompt.lower():
            return self._generate_demo_resume_analysis(prompt)
        elif "job" in prompt.lower():
            return self._generate_demo_job_analysis(prompt)
        else:
            return "Analysis completed in demo mode. For advanced AI insights, run locally with Ollama."

    def _generate_demo_resume_analysis(self, prompt: str) -> str:
        """Generate demo resume analysis"""
        return """
        DEMO ANALYSIS:
        
        Strengths:
        • Professional experience demonstrated
        • Clear technical skills listed
        • Good educational background
        • Relevant industry experience
        
        Areas for Improvement:
        • Add quantifiable achievements
        • Include more specific project details
        • Optimize keywords for ATS systems
        • Consider adding certifications
        
        Overall Score: 78/100
        
        Recommendations:
        • Use action verbs to start bullet points
        • Add metrics to show impact
        • Tailor resume for specific roles
        • Include relevant keywords from job descriptions
        """

    def _generate_demo_job_analysis(self, prompt: str) -> str:
        """Generate demo job analysis"""
        return """
        JOB ANALYSIS:
        
        Key Requirements Identified:
        • Technical skills in programming
        • Experience with relevant frameworks
        • Team collaboration abilities
        • Problem-solving skills
        
        Match Assessment:
        • Good alignment with stated experience
        • Skills match moderately well
        • Consider highlighting relevant projects
        
        Suggestions:
        • Emphasize matching experience
        • Add relevant keywords
        • Quantify achievements
        • Show impact of previous work
        """

    async def analyze_resume(self, text: str) -> Dict[str, Any]:
        """Analyze resume text and return structured data"""
        # Extract basic info
        basic_info = self.extract_basic_info(text)
        
        # Simple keyword extraction for skills
        tech_keywords = [
            'python', 'javascript', 'java', 'react', 'node.js', 'sql', 'aws', 'docker',
            'git', 'html', 'css', 'mongodb', 'postgresql', 'kubernetes', 'jenkins',
            'machine learning', 'data science', 'api', 'rest', 'microservices'
        ]
        
        text_lower = text.lower()
        found_skills = [skill for skill in tech_keywords if skill in text_lower]
        
        # Extract experience years
        experience_years = self._extract_experience_years(text)
        
        # Determine career level
        career_level = self._determine_career_level(experience_years)
        
        return {
            "name": basic_info["name"],
            "email": basic_info["email"],
            "phone": basic_info["phone"],
            "experience_years": experience_years,
            "career_level": career_level,
            "skills": found_skills[:10],
            "strengths": [
                "Clear technical background",
                "Relevant industry experience",
                "Good skill diversity",
                "Professional presentation"
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

    def extract_basic_info(self, text: str) -> Dict[str, Any]:
        """Extract basic information from resume text"""
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        # Extract phone
        phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phones = re.findall(phone_pattern, text)
        
        # Extract name (first non-email line that looks like a name)
        lines = text.split('\n')
        name = ""
        for line in lines[:5]:
            line = line.strip()
            if line and '@' not in line and len(line.split()) <= 3 and len(line) > 2:
                name = line
                break
        
        return {
            "name": name or "Not specified",
            "email": emails[0] if emails else "Not specified",
            "phone": f"({phones[0][1]}) {phones[0][2]}-{phones[0][3]}" if phones else "Not specified"
        }

    def _extract_experience_years(self, text: str) -> int:
        """Extract years of experience from text"""
        experience_years = 0
        exp_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'experience.*?(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*in'
        ]
        
        text_lower = text.lower()
        for pattern in exp_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                try:
                    experience_years = max(experience_years, int(matches[0]))
                except:
                    pass
        
        return experience_years

    def _determine_career_level(self, years: int) -> str:
        """Determine career level based on years of experience"""
        if years >= 8:
            return "Senior"
        elif years >= 3:
            return "Mid-level"
        elif years >= 1:
            return "Junior"
        else:
            return "Entry-level"

    async def validate_ats(self, text: str) -> Dict[str, Any]:
        """Validate resume for ATS compatibility"""
        issues = []
        score = 85  # Base score
        
        # Check for common ATS issues
        if len(text) < 200:
            issues.append("Resume content is too short")
            score -= 15
            
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            issues.append("No email address found")
            score -= 10
            
        # Check for good structure indicators
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

    async def analyze_job_fit(self, resume_text: str, job_text: str) -> Dict[str, Any]:
        """Analyze how well resume matches job description"""
        # Simple keyword matching
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
        relevant_lines = []
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in keywords):
                # Look for bullet points or numbered lists
                if line.startswith(('•', '-', '*')) or (len(line) > 0 and line[0].isdigit()):
                    relevant_lines.append(line.lstrip('•-*0123456789. '))
        
        return relevant_lines if relevant_lines else ["Analysis completed - see full response for details"]

    def _calculate_skill_match(self, current_skills: List[str], required_skills: List[str]) -> float:
        """Calculate percentage match between current and required skills"""
        if not required_skills:
            return 100.0
        
        matches = sum(1 for req_skill in required_skills if any(req_skill in curr_skill for curr_skill in current_skills))
        return (matches / len(required_skills)) * 100.0
