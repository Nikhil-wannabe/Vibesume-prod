"""
LLM Service for local language model integration
Supports Ollama and other local LLM solutions
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
import httpx
from app.models.resume_models import ResumeData, JobDescription, AnalysisResult

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
                        logger.info(f"✅ LLM service initialized with model: {self.model_name}")
                    else:
                        logger.warning(f"⚠️ Model {self.model_name} not found. Available models: {available_models}")
                        if available_models:
                            self.model_name = available_models[0]
                            self.is_available = True
                            logger.info(f"Using alternative model: {self.model_name}")
                else:
                    logger.error(f"❌ Ollama server not responding: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Could not connect to Ollama: {e}")
            logger.info("💡 To use AI features, install Ollama from https://ollama.ai and run 'ollama pull llama3.2:3b'")

    async def generate_response(self, prompt: str, system_prompt: str = None) -> str:
        """Generate response from the local LLM"""
        if not self.is_available:
            return self._fallback_response()

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
                    return self._fallback_response()
                    
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return self._fallback_response()

    def _fallback_response(self) -> str:
        """Fallback response when LLM is not available"""
        return "AI analysis unavailable. Please check if Ollama is running and the model is installed."

    async def analyze_resume(self, resume_data: ResumeData, job_description: Optional[JobDescription] = None) -> AnalysisResult:
        """Analyze resume content and provide feedback"""
        
        # Create prompt for resume analysis
        resume_text = self._format_resume_for_analysis(resume_data)
        
        system_prompt = """You are an expert resume reviewer and career coach. Analyze the provided resume and give constructive feedback. Focus on:
1. Overall structure and organization
2. Content quality and relevance
3. Skills alignment with industry standards
4. Areas for improvement
5. Missing critical information

Provide your response in a structured format with specific, actionable recommendations."""

        if job_description:
            prompt = f"""
Analyze this resume against the following job description:

JOB DESCRIPTION:
Title: {job_description.title}
Company: {job_description.company or 'Not specified'}
Description: {job_description.description}
Required Skills: {', '.join(job_description.required_skills)}
Preferred Skills: {', '.join(job_description.preferred_skills)}

RESUME:
{resume_text}

Please provide:
1. Match percentage (0-100)
2. Key strengths that align with the job
3. Missing skills or qualifications
4. Specific suggestions to improve match
5. Keywords that should be added

Format your response as structured feedback.
"""
        else:
            prompt = f"""
Analyze this resume and provide comprehensive feedback:

RESUME:
{resume_text}

Please provide:
1. Overall quality score (0-100)
2. Strengths of the resume
3. Areas that need improvement
4. Specific suggestions for enhancement
5. Missing sections or information

Format your response as structured feedback.
"""

        # Get AI analysis
        ai_response = await self.generate_response(prompt, system_prompt)
        
        # Parse AI response and create structured result
        return self._parse_analysis_response(ai_response, job_description)

    async def get_skill_gap_analysis(self, resume_data: ResumeData, job_description: JobDescription) -> Dict[str, Any]:
        """Analyze skill gaps between resume and job requirements"""
        
        current_skills = [skill.name.lower() for skill in resume_data.skills]
        required_skills = [skill.lower() for skill in job_description.required_skills]
        preferred_skills = [skill.lower() for skill in job_description.preferred_skills]
        
        # Identify missing skills
        missing_required = [skill for skill in required_skills if skill not in current_skills]
        missing_preferred = [skill for skill in preferred_skills if skill not in current_skills]
        
        # Get AI recommendations for skill development
        prompt = f"""
Based on this skill gap analysis:

Current Skills: {', '.join([skill.name for skill in resume_data.skills])}
Missing Required Skills: {', '.join(missing_required)}
Missing Preferred Skills: {', '.join(missing_preferred)}
Job Title: {job_description.title}

Provide specific recommendations for:
1. Priority skills to learn first
2. Learning resources or paths
3. How to gain experience in these skills
4. Timeline for skill development
5. Alternative skills that could compensate

Be practical and actionable in your advice.
"""

        system_prompt = "You are a career development expert specializing in skill gap analysis and professional development planning."
        
        ai_response = await self.generate_response(prompt, system_prompt)
        
        return {
            "missing_required_skills": missing_required,
            "missing_preferred_skills": missing_preferred,
            "skill_match_percentage": self._calculate_skill_match(current_skills, required_skills + preferred_skills),
            "ai_recommendations": ai_response,
            "learning_priority": missing_required[:5]  # Top 5 priority skills
        }

    async def vibe_check_feedback(self, resume_data: ResumeData, job_url: Optional[str] = None) -> str:
        """Provide 'vibe check' feedback in a casual, honest manner"""
        
        resume_text = self._format_resume_for_analysis(resume_data)
        
        system_prompt = """You are a friendly but brutally honest career coach who gives "vibe check" feedback. 
Be conversational, use some casual language, but provide genuinely helpful insights. 
Point out both the good stuff and what needs work, but do it in an encouraging way.
Think of yourself as that friend who tells you the truth but has your back."""

        if job_url:
            prompt = f"""
Give me a vibe check on this resume. Someone's trying to land a job and wants to know if their resume is giving the right energy.

Job URL: {job_url}

RESUME:
{resume_text}

Keep it real - what's working, what's not, and what would make this resume actually stand out? 
Be specific about improvements but keep the tone supportive and motivating.
"""
        else:
            prompt = f"""
Time for a resume vibe check! Give me the real talk on this resume:

RESUME:
{resume_text}

What's the energy this resume is giving off? Is it "hire me now" or "maybe consider me"? 
What would make this resume absolutely slap? Keep it honest but encouraging.
"""

        return await self.generate_response(prompt, system_prompt)

    def _format_resume_for_analysis(self, resume_data: ResumeData) -> str:
        """Format resume data into readable text for LLM analysis"""
        sections = []
        
        # Contact info
        contact = resume_data.contact_info
        sections.append(f"Name: {contact.full_name}")
        sections.append(f"Email: {contact.email}")
        if contact.phone:
            sections.append(f"Phone: {contact.phone}")
        if contact.location:
            sections.append(f"Location: {contact.location}")
        
        # Summary
        if resume_data.summary:
            sections.append(f"\nSUMMARY:\n{resume_data.summary}")
        
        # Experience
        if resume_data.experience:
            sections.append("\nEXPERIENCE:")
            for exp in resume_data.experience:
                end_date = exp.end_date or "Present"
                sections.append(f"\n{exp.position} at {exp.company} ({exp.start_date} - {end_date})")
                for desc in exp.description:
                    sections.append(f"• {desc}")
                if exp.technologies:
                    sections.append(f"Technologies: {', '.join(exp.technologies)}")
        
        # Education
        if resume_data.education:
            sections.append("\nEDUCATION:")
            for edu in resume_data.education:
                sections.append(f"{edu.degree} in {edu.field_of_study or 'N/A'} - {edu.institution}")
        
        # Skills
        if resume_data.skills:
            sections.append(f"\nSKILLS:\n{', '.join([skill.name for skill in resume_data.skills])}")
        
        return "\n".join(sections)

    def _parse_analysis_response(self, ai_response: str, job_description: Optional[JobDescription] = None) -> AnalysisResult:
        """Parse AI response into structured AnalysisResult"""
        
        # Extract score from response (look for percentage or score)
        score = 75.0  # Default fallback
        try:
            import re
            score_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:%|/100|score)', ai_response.lower())
            if score_match:
                score = float(score_match.group(1))
                if score > 100:
                    score = score / 10  # Handle cases where it might be out of 1000
        except:
            pass
        
        # Parse sections from AI response
        strengths = self._extract_list_from_response(ai_response, ["strength", "positive", "good"])
        weaknesses = self._extract_list_from_response(ai_response, ["weakness", "improvement", "issue"])
        suggestions = self._extract_list_from_response(ai_response, ["suggest", "recommend", "should"])
        missing_skills = self._extract_list_from_response(ai_response, ["missing", "lack", "need"])
        
        return AnalysisResult(
            score=score,
            strengths=strengths[:5],  # Limit to top 5
            weaknesses=weaknesses[:5],
            suggestions=suggestions[:7],
            missing_skills=missing_skills[:10],
            keyword_matches={}  # Could be enhanced with keyword analysis
        )

    def _extract_list_from_response(self, response: str, keywords: List[str]) -> List[str]:
        """Extract bullet points or lists from AI response based on keywords"""
        lines = response.split('\n')
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
