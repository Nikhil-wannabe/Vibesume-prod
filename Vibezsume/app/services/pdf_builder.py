"""
PDF resume builder service
Creates ATS-friendly PDF resumes from structured data
"""

import logging
from typing import Dict, Any, List
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.colors import black, darkblue, gray
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime

from app.models.resume_models import ResumeData, ResumeBuilderRequest

logger = logging.getLogger(__name__)

class PDFResumeBuilder:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom styles for different resume templates"""
        
        # Header styles
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=18,
            spaceAfter=6,
            textColor=darkblue,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=12,
            textColor=darkblue,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=darkblue,
            borderPadding=2
        ))
        
        # Experience item style
        self.styles.add(ParagraphStyle(
            name='ExperienceHeader',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=3,
            fontName='Helvetica-Bold'
        ))
        
        # Description style
        self.styles.add(ParagraphStyle(
            name='Description',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leftIndent=20,
            bulletIndent=10
        ))
        
        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=12
        ))

    async def build_resume(self, request: ResumeBuilderRequest, output_path: str) -> str:
        """Build PDF resume from structured data"""
        
        try:
            # Create the PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build the content based on template style
            if request.template_style == "modern":
                story = self._build_modern_template(request.resume_data, request)
            elif request.template_style == "classic":
                story = self._build_classic_template(request.resume_data, request)
            elif request.template_style == "creative":
                story = self._build_creative_template(request.resume_data, request)
            else:
                story = self._build_modern_template(request.resume_data, request)
            
            # Build the PDF
            doc.build(story)
            
            logger.info(f"Resume PDF created successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error building PDF resume: {e}")
            raise

    def _build_modern_template(self, resume_data: ResumeData, request: ResumeBuilderRequest) -> List[Any]:
        """Build modern template layout"""
        story = []
        
        # Header with name and contact info
        story.extend(self._build_header(resume_data.contact_info))
        
        # Build sections in specified order
        for section in request.sections_order:
            if section == "summary" and resume_data.summary:
                story.extend(self._build_summary_section(resume_data.summary))
            elif section == "experience" and resume_data.experience:
                story.extend(self._build_experience_section(resume_data.experience))
            elif section == "education" and resume_data.education:
                story.extend(self._build_education_section(resume_data.education))
            elif section == "skills" and resume_data.skills:
                story.extend(self._build_skills_section(resume_data.skills))
            elif section == "projects" and resume_data.projects:
                story.extend(self._build_projects_section(resume_data.projects))
        
        # Add certifications if available
        if resume_data.certifications:
            story.extend(self._build_certifications_section(resume_data.certifications))
        
        return story

    def _build_classic_template(self, resume_data: ResumeData, request: ResumeBuilderRequest) -> List[Any]:
        """Build classic template layout"""
        # Similar to modern but with more traditional styling
        return self._build_modern_template(resume_data, request)

    def _build_creative_template(self, resume_data: ResumeData, request: ResumeBuilderRequest) -> List[Any]:
        """Build creative template layout"""
        # More visual elements, but still ATS-friendly
        return self._build_modern_template(resume_data, request)

    def _build_header(self, contact_info) -> List[Any]:
        """Build the header section with contact information"""
        elements = []
        
        # Name
        name_para = Paragraph(contact_info.full_name, self.styles['CustomTitle'])
        elements.append(name_para)
        
        # Contact information
        contact_parts = [contact_info.email]
        if contact_info.phone:
            contact_parts.append(contact_info.phone)
        if contact_info.location:
            contact_parts.append(contact_info.location)
        
        contact_text = " | ".join(contact_parts)
        contact_para = Paragraph(contact_text, self.styles['ContactInfo'])
        elements.append(contact_para)
        
        # Links
        links = []
        if contact_info.linkedin:
            links.append(f'<a href="{contact_info.linkedin}">LinkedIn</a>')
        if contact_info.github:
            links.append(f'<a href="{contact_info.github}">GitHub</a>')
        if contact_info.portfolio:
            links.append(f'<a href="{contact_info.portfolio}">Portfolio</a>')
        
        if links:
            links_text = " | ".join(links)
            links_para = Paragraph(links_text, self.styles['ContactInfo'])
            elements.append(links_para)
        
        elements.append(Spacer(1, 12))
        return elements

    def _build_summary_section(self, summary: str) -> List[Any]:
        """Build professional summary section"""
        elements = []
        
        # Section header
        header = Paragraph("PROFESSIONAL SUMMARY", self.styles['SectionHeader'])
        elements.append(header)
        
        # Summary content
        summary_para = Paragraph(summary, self.styles['Normal'])
        elements.append(summary_para)
        elements.append(Spacer(1, 12))
        
        return elements

    def _build_experience_section(self, experience_list) -> List[Any]:
        """Build work experience section"""
        elements = []
        
        # Section header
        header = Paragraph("PROFESSIONAL EXPERIENCE", self.styles['SectionHeader'])
        elements.append(header)
        
        for exp in experience_list:
            # Job title and company
            end_date = exp.end_date or "Present"
            job_header = f"<b>{exp.position}</b> | {exp.company} | {exp.start_date} - {end_date}"
            if exp.location:
                job_header += f" | {exp.location}"
            
            job_para = Paragraph(job_header, self.styles['ExperienceHeader'])
            elements.append(job_para)
            
            # Job description
            for desc in exp.description:
                desc_text = f"• {desc}"
                desc_para = Paragraph(desc_text, self.styles['Description'])
                elements.append(desc_para)
            
            # Technologies used
            if exp.technologies:
                tech_text = f"<i>Technologies: {', '.join(exp.technologies)}</i>"
                tech_para = Paragraph(tech_text, self.styles['Description'])
                elements.append(tech_para)
            
            elements.append(Spacer(1, 8))
        
        return elements

    def _build_education_section(self, education_list) -> List[Any]:
        """Build education section"""
        elements = []
        
        # Section header
        header = Paragraph("EDUCATION", self.styles['SectionHeader'])
        elements.append(header)
        
        for edu in education_list:
            # Degree and institution
            edu_text = f"<b>{edu.degree}</b>"
            if edu.field_of_study:
                edu_text += f" in {edu.field_of_study}"
            edu_text += f" | {edu.institution}"
            
            if edu.end_date:
                edu_text += f" | {edu.end_date}"
            
            if edu.gpa and edu.gpa >= 3.5:
                edu_text += f" | GPA: {edu.gpa}"
            
            edu_para = Paragraph(edu_text, self.styles['ExperienceHeader'])
            elements.append(edu_para)
            
            # Honors
            if edu.honors:
                honors_text = f"<i>Honors: {', '.join(edu.honors)}</i>"
                honors_para = Paragraph(honors_text, self.styles['Description'])
                elements.append(honors_para)
            
            elements.append(Spacer(1, 6))
        
        return elements

    def _build_skills_section(self, skills_list) -> List[Any]:
        """Build skills section"""
        elements = []
        
        # Section header
        header = Paragraph("TECHNICAL SKILLS", self.styles['SectionHeader'])
        elements.append(header)
        
        # Group skills by category
        categorized_skills = {}
        for skill in skills_list:
            category = skill.category or "Technical"
            if category not in categorized_skills:
                categorized_skills[category] = []
            categorized_skills[category].append(skill.name)
        
        # Display skills by category
        for category, skill_names in categorized_skills.items():
            skills_text = f"<b>{category}:</b> {', '.join(skill_names)}"
            skills_para = Paragraph(skills_text, self.styles['Normal'])
            elements.append(skills_para)
            elements.append(Spacer(1, 4))
        
        return elements

    def _build_projects_section(self, projects_list) -> List[Any]:
        """Build projects section"""
        elements = []
        
        # Section header
        header = Paragraph("PROJECTS", self.styles['SectionHeader'])
        elements.append(header)
        
        for project in projects_list:
            # Project name and description
            project_header = f"<b>{project.name}</b>"
            if project.url:
                project_header += f' | <a href="{project.url}">Live Demo</a>'
            if project.github_url:
                project_header += f' | <a href="{project.github_url}">GitHub</a>'
            
            project_para = Paragraph(project_header, self.styles['ExperienceHeader'])
            elements.append(project_para)
            
            # Project description
            desc_para = Paragraph(f"• {project.description}", self.styles['Description'])
            elements.append(desc_para)
            
            # Technologies
            if project.technologies:
                tech_text = f"<i>Technologies: {', '.join(project.technologies)}</i>"
                tech_para = Paragraph(tech_text, self.styles['Description'])
                elements.append(tech_para)
            
            elements.append(Spacer(1, 6))
        
        return elements

    def _build_certifications_section(self, certifications_list) -> List[Any]:
        """Build certifications section"""
        elements = []
        
        # Section header
        header = Paragraph("CERTIFICATIONS", self.styles['SectionHeader'])
        elements.append(header)
        
        for cert in certifications_list:
            cert_text = f"<b>{cert.name}</b> | {cert.issuer}"
            if cert.issue_date:
                cert_text += f" | {cert.issue_date}"
            if cert.credential_url:
                cert_text += f' | <a href="{cert.credential_url}">Verify</a>'
            
            cert_para = Paragraph(cert_text, self.styles['Normal'])
            elements.append(cert_para)
            elements.append(Spacer(1, 4))
        
        return elements

    def get_template_styles(self) -> List[str]:
        """Get available template styles"""
        return ["modern", "classic", "creative"]

    def get_color_schemes(self) -> List[str]:
        """Get available color schemes"""
        return ["blue", "green", "purple", "black", "gray"]
