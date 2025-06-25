"""
Resume parsing service for extracting data from uploaded files
"""

import logging
import re
from typing import Dict, Any, List, Optional
import PyPDF2
import docx
from pathlib import Path
import spacy
import nltk
from app.models.resume_models import ResumeData, ContactInfo, Experience, Education, Skill, SkillLevel

logger = logging.getLogger(__name__)

class ResumeParser:
    def __init__(self):
        self.nlp = None
        self._initialize_nlp()

    def _initialize_nlp(self):
        """Initialize NLP models for text processing"""
        try:
            # Try to load spaCy model
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None

        try:
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
        except:
            logger.warning("Could not download NLTK data")

    async def parse_resume(self, file_path: str) -> ResumeData:
        """Parse resume file and extract structured data"""
        
        # Extract text from file
        text = await self._extract_text_from_file(file_path)
        
        if not text:
            raise ValueError("Could not extract text from resume file")

        # Parse different sections
        contact_info = self._extract_contact_info(text)
        summary = self._extract_summary(text)
        experience = self._extract_experience(text)
        education = self._extract_education(text)
        skills = self._extract_skills(text)
        
        return ResumeData(
            contact_info=contact_info,
            summary=summary,
            experience=experience,
            education=education,            skills=skills,
            projects=[],  # Can be enhanced later
            certifications=[],
            languages=[],
            awards=[]
        )

    async def _extract_text_from_file(self, file_path: str) -> str:
        """Extract text content from PDF, DOCX, or TXT file"""
        file_path = Path(file_path)
        
        if file_path.suffix.lower() == '.pdf':
            return self._extract_from_pdf(file_path)
        elif file_path.suffix.lower() in ['.docx', '.doc']:
            return self._extract_from_docx(file_path)
        elif file_path.suffix.lower() == '.txt':
            return self._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

    def _extract_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return ""

    def _extract_from_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {e}")
            return ""

    def _extract_from_txt(self, file_path: Path) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error extracting text from TXT: {e}")
            return ""

    def _extract_contact_info(self, text: str) -> ContactInfo:
        """Extract contact information from resume text"""
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        email = email_match.group() if email_match else "email@example.com"
        
        # Extract phone number
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phone_match = re.search(phone_pattern, text)
        phone = phone_match.group() if phone_match else None
        
        # Extract name (usually in the first few lines)
        lines = text.split('\n')
        name = "Full Name"
        for line in lines[:5]:
            line = line.strip()
            if line and not any(char in line for char in ['@', 'http', '+']) and len(line.split()) <= 4:
                if not re.search(r'\d', line):  # No numbers in name
                    name = line
                    break
        
        # Extract LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, text)
        linkedin = f"https://{linkedin_match.group()}" if linkedin_match else None
        
        # Extract GitHub
        github_pattern = r'github\.com/[\w-]+'
        github_match = re.search(github_pattern, text)
        github = f"https://{github_match.group()}" if github_match else None
        
        return ContactInfo(
            full_name=name,
            email=email,
            phone=phone,
            linkedin=linkedin,
            github=github
        )

    def _extract_summary(self, text: str) -> Optional[str]:
        """Extract professional summary or objective"""
        
        # Look for common summary section headers
        summary_patterns = [
            r'(?:SUMMARY|PROFESSIONAL SUMMARY|OBJECTIVE|PROFILE).*?\n(.*?)(?=\n[A-Z]|\n\n|\Z)',
            r'(?:Summary|Professional Summary|Objective|Profile).*?\n(.*?)(?=\n[A-Z]|\n\n|\Z)'
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                summary = match.group(1).strip()
                # Clean up the summary
                summary = re.sub(r'\n+', ' ', summary)
                if len(summary) > 50:  # Reasonable length for a summary
                    return summary
        
        return None

    def _extract_experience(self, text: str) -> List[Experience]:
        """Extract work experience from resume"""
        
        experiences = []
        
        # Find experience section
        exp_pattern = r'(?:EXPERIENCE|WORK EXPERIENCE|EMPLOYMENT|PROFESSIONAL EXPERIENCE)(.*?)(?=\n(?:EDUCATION|SKILLS|PROJECTS|CERTIFICATIONS|\Z))'
        exp_match = re.search(exp_pattern, text, re.DOTALL | re.IGNORECASE)
        
        if not exp_match:
            return experiences
        
        exp_section = exp_match.group(1)
        
        # Split into individual jobs (look for patterns like company names, dates)
        job_patterns = r'([A-Z][^,\n]*(?:Inc|LLC|Corp|Company|Ltd)?.*?\n.*?\d{4}.*?(?=\n[A-Z][^,\n]*(?:Inc|LLC|Corp|Company|Ltd)?|\Z))'
        jobs = re.findall(job_patterns, exp_section, re.DOTALL)
        
        for job in jobs:
            # Extract company, position, dates, and description
            lines = [line.strip() for line in job.split('\n') if line.strip()]
            
            if len(lines) >= 2:
                # First line often contains company/position
                company = lines[0]
                position = lines[1] if len(lines) > 1 else "Position"
                
                # Look for dates
                date_pattern = r'(\d{1,2}/\d{4}|\d{4})'
                dates = re.findall(date_pattern, job)
                start_date = dates[0] if dates else "2020"
                end_date = dates[1] if len(dates) > 1 else None
                
                # Extract description points
                description = []
                for line in lines[2:]:
                    if line and not re.search(r'\d{4}', line):
                        description.append(line.lstrip('•-* '))
                
                experiences.append(Experience(
                    company=company,
                    position=position,
                    start_date=start_date,
                    end_date=end_date,
                    description=description[:5],  # Limit to 5 points
                    technologies=[]
                ))
        
        return experiences

    def _extract_education(self, text: str) -> List[Education]:
        """Extract education information"""
        
        education_list = []
        
        # Find education section
        edu_pattern = r'(?:EDUCATION|ACADEMIC BACKGROUND)(.*?)(?=\n(?:EXPERIENCE|SKILLS|PROJECTS|CERTIFICATIONS|\Z))'
        edu_match = re.search(edu_pattern, text, re.DOTALL | re.IGNORECASE)
        
        if not edu_match:
            return education_list
        
        edu_section = edu_match.group(1)
        
        # Look for degree patterns
        degree_patterns = [
            r'(Bachelor|Master|PhD|B\.S\.|M\.S\.|B\.A\.|M\.A\.|MBA).*?(?=\n\n|\Z)',
            r'([A-Z][^,\n]*(?:University|College|Institute).*?\d{4})'
        ]
        
        for pattern in degree_patterns:
            matches = re.findall(pattern, edu_section, re.DOTALL | re.IGNORECASE)
            for match in matches:
                # Parse degree information
                lines = [line.strip() for line in match.split('\n') if line.strip()]
                
                if lines:
                    institution = "Institution"
                    degree = lines[0]
                    
                    # Look for university/college name
                    for line in lines:
                        if any(word in line.lower() for word in ['university', 'college', 'institute']):
                            institution = line
                            break
                    
                    # Extract graduation year
                    year_pattern = r'\d{4}'
                    year_match = re.search(year_pattern, match)
                    year = year_match.group() if year_match else None
                    
                    education_list.append(Education(
                        institution=institution,
                        degree=degree,
                        end_date=year
                    ))
        
        return education_list

    def _extract_skills(self, text: str) -> List[Skill]:
        """Extract skills from resume"""
        
        skills = []
        
        # Find skills section
        skills_pattern = r'(?:SKILLS|TECHNICAL SKILLS|CORE COMPETENCIES)(.*?)(?=\n(?:EXPERIENCE|EDUCATION|PROJECTS|CERTIFICATIONS|\Z))'
        skills_match = re.search(skills_pattern, text, re.DOTALL | re.IGNORECASE)
        
        if skills_match:
            skills_section = skills_match.group(1)
        else:
            # Look for skills throughout the document
            skills_section = text
        
        # Common technical skills to look for
        tech_skills = [
            'Python', 'Java', 'JavaScript', 'React', 'Node.js', 'SQL', 'MongoDB',
            'AWS', 'Docker', 'Kubernetes', 'Git', 'HTML', 'CSS', 'TypeScript',
            'Angular', 'Vue.js', 'Django', 'Flask', 'FastAPI', 'PostgreSQL',
            'Redis', 'Elasticsearch', 'Jenkins', 'CI/CD', 'Machine Learning',
            'Data Science', 'TensorFlow', 'PyTorch', 'Pandas', 'NumPy',
            'C++', 'C#', '.NET', 'Spring Boot', 'Microservices', 'REST API',
            'GraphQL', 'Terraform', 'Ansible', 'Linux', 'Bash', 'PowerShell'
        ]
        
        # Find mentioned skills
        found_skills = []
        for skill in tech_skills:
            if skill.lower() in skills_section.lower():
                found_skills.append(Skill(
                    name=skill,
                    level=SkillLevel.INTERMEDIATE  # Default level
                ))
        
        # Also extract skills from comma-separated lists
        lines = skills_section.split('\n')
        for line in lines:
            if ',' in line and len(line.split(',')) > 2:
                skill_names = [s.strip() for s in line.split(',')]
                for skill_name in skill_names:
                    if skill_name and len(skill_name) < 30:  # Reasonable skill name length
                        found_skills.append(Skill(
                            name=skill_name,
                            level=SkillLevel.INTERMEDIATE
                        ))
        
        # Remove duplicates
        unique_skills = []
        seen_skills = set()
        for skill in found_skills:
            if skill.name.lower() not in seen_skills:
                unique_skills.append(skill)
                seen_skills.add(skill.name.lower())
        
        return unique_skills[:20]  # Limit to 20 skills
