"""
ATS (Applicant Tracking System) validator service
Analyzes resume formatting, spacing, and ATS compatibility
"""

import re
import logging
from typing import Dict, List, Any, Tuple
from pathlib import Path
import PyPDF2
import docx
from app.models.resume_models import ATSValidationResult

logger = logging.getLogger(__name__)

class ATSValidator:
    def __init__(self):
        self.ats_friendly_fonts = [
            'arial', 'calibri', 'times new roman', 'helvetica', 'georgia',
            'verdana', 'tahoma', 'trebuchet ms', 'garamond'
        ]
        
        self.problematic_elements = [
            'text boxes', 'headers', 'footers', 'tables', 'images',
            'graphics', 'columns', 'watermarks'
        ]

    async def validate_resume(self, file_path: str, resume_text: str) -> ATSValidationResult:
        """Comprehensive ATS validation of resume"""
        
        # Perform various validation checks
        formatting_score, formatting_issues = self._check_formatting(file_path, resume_text)
        spacing_score, spacing_issues = self._check_spacing(resume_text)
        font_score, font_issues = self._check_font_compatibility(file_path)
        section_score, section_issues = self._check_section_structure(resume_text)
        keyword_score, keyword_analysis = self._analyze_keyword_optimization(resume_text)
        
        # Calculate overall score
        overall_score = (
            formatting_score * 0.25 +
            spacing_score * 0.20 +
            font_score * 0.15 +
            section_score * 0.25 +
            keyword_score * 0.15
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            formatting_issues, spacing_issues, font_issues, section_issues, keyword_analysis
        )
        
        return ATSValidationResult(
            overall_score=round(overall_score, 1),
            formatting_issues=formatting_issues,
            spacing_issues=spacing_issues,
            font_issues=font_issues,
            section_issues=section_issues,
            keyword_optimization=keyword_analysis,
            recommendations=recommendations
        )

    def _check_formatting(self, file_path: str, text: str) -> Tuple[float, List[str]]:
        """Check for ATS-friendly formatting"""
        issues = []
        score = 100.0
        
        file_path = Path(file_path)
        
        # Check file format
        if file_path.suffix.lower() not in ['.pdf', '.docx', '.doc']:
            issues.append("Use PDF or DOCX format for better ATS compatibility")
            score -= 20
        
        # Check for complex formatting indicators in text
        if re.search(r'[│┌┐└┘├┤┬┴┼]', text):
            issues.append("Contains table borders or complex formatting that may confuse ATS")
            score -= 15
        
        # Check for excessive special characters
        special_chars = len(re.findall(r'[★☆●○◆◇▪▫►▲▼◄]', text))
        if special_chars > 5:
            issues.append("Too many special characters/symbols - use simple bullets (•)")
            score -= 10
        
        # Check for proper bullet points
        if '•' not in text and '-' not in text and '*' not in text:
            issues.append("No bullet points detected - use consistent bullet formatting")
            score -= 10
        
        # Check for mixed bullet styles
        bullet_types = sum([1 for char in ['•', '-', '*'] if char in text])
        if bullet_types > 1:
            issues.append("Inconsistent bullet point styles - stick to one type")
            score -= 5
        
        return max(score, 0), issues

    def _check_spacing(self, text: str) -> Tuple[float, List[str]]:
        """Check spacing and layout issues"""
        issues = []
        score = 100.0
        
        lines = text.split('\n')
        
        # Check for excessive blank lines
        consecutive_blanks = 0
        max_consecutive_blanks = 0
        for line in lines:
            if not line.strip():
                consecutive_blanks += 1
                max_consecutive_blanks = max(max_consecutive_blanks, consecutive_blanks)
            else:
                consecutive_blanks = 0
        
        if max_consecutive_blanks > 2:
            issues.append("Too many consecutive blank lines - limit to 1-2 for section breaks")
            score -= 10
        
        # Check line length consistency
        non_empty_lines = [line for line in lines if line.strip()]
        if non_empty_lines:
            avg_length = sum(len(line) for line in non_empty_lines) / len(non_empty_lines)
            long_lines = sum(1 for line in non_empty_lines if len(line) > avg_length * 2)
            
            if long_lines > len(non_empty_lines) * 0.1:  # More than 10% are unusually long
                issues.append("Inconsistent line lengths may indicate formatting issues")
                score -= 8
        
        # Check for proper section spacing
        section_headers = re.findall(r'\n([A-Z][A-Z\s]+)\n', text)
        if len(section_headers) < 3:
            issues.append("Sections may not be clearly separated - use consistent header formatting")
            score -= 12
        
        # Check for tabs vs spaces (tabs can cause issues)
        if '\t' in text:
            issues.append("Contains tab characters - use spaces for consistent formatting")
            score -= 5
        
        return max(score, 0), issues

    def _check_font_compatibility(self, file_path: str) -> Tuple[float, List[str]]:
        """Check font compatibility with ATS systems"""
        issues = []
        score = 100.0
        
        # For PDF files, we can do basic checks
        if Path(file_path).suffix.lower() == '.pdf':
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    
                    # Check if PDF is text-selectable (indicates proper font embedding)
                    text_extractable = False
                    for page in pdf_reader.pages:
                        if page.extract_text().strip():
                            text_extractable = True
                            break
                    
                    if not text_extractable:
                        issues.append("PDF text is not selectable - may be an image or have font issues")
                        score -= 30
                
            except Exception as e:
                issues.append("Could not analyze PDF font properties")
                score -= 10
        
        # General font recommendations
        issues.append("Use ATS-friendly fonts: Arial, Calibri, Times New Roman, or Helvetica")
        issues.append("Font size should be 10-12pt for body text, 14-16pt for headers")
        
        return max(score, 0), issues

    def _check_section_structure(self, text: str) -> Tuple[float, List[str]]:
        """Check for proper resume section structure"""
        issues = []
        score = 100.0
        
        required_sections = ['experience', 'education', 'skills']
        optional_sections = ['summary', 'objective', 'projects', 'certifications']
        
        text_lower = text.lower()
        
        # Check for required sections
        missing_required = []
        for section in required_sections:
            if section not in text_lower:
                missing_required.append(section)
        
        if missing_required:
            issues.append(f"Missing required sections: {', '.join(missing_required)}")
            score -= 15 * len(missing_required)
        
        # Check section order (contact info should be first)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            first_section = lines[0].lower()
            if 'experience' in first_section or 'education' in first_section:
                issues.append("Contact information should appear before other sections")
                score -= 10
        
        # Check for clear section headers
        potential_headers = re.findall(r'\n([A-Z][A-Z\s]{2,})\n', text)
        if len(potential_headers) < 2:
            issues.append("Section headers should be in ALL CAPS or clearly formatted")
            score -= 12
        
        # Check for contact information
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            issues.append("No email address found - essential for ATS parsing")
            score -= 20
        
        if not re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text):
            issues.append("No phone number detected - include for better ATS compatibility")
            score -= 10
        
        return max(score, 0), issues

    def _analyze_keyword_optimization(self, text: str) -> Tuple[float, Dict[str, Any]]:
        """Analyze keyword density and optimization"""
        
        # Common industry keywords to check for
        tech_keywords = [
            'python', 'java', 'javascript', 'react', 'sql', 'aws', 'docker',
            'kubernetes', 'git', 'agile', 'scrum', 'api', 'database', 'cloud',
            'machine learning', 'data analysis', 'project management', 'leadership',
            'problem solving', 'teamwork', 'communication', 'analytical'
        ]
        
        text_lower = text.lower()
        word_count = len(text.split())
        
        # Count keyword occurrences
        keyword_counts = {}
        total_keywords = 0
        
        for keyword in tech_keywords:
            count = text_lower.count(keyword)
            if count > 0:
                keyword_counts[keyword] = count
                total_keywords += count
        
        # Calculate keyword density
        keyword_density = (total_keywords / word_count) * 100 if word_count > 0 else 0
        
        # Score based on keyword presence and density
        score = 50.0  # Base score
        
        if len(keyword_counts) > 10:
            score += 30  # Good keyword variety
        elif len(keyword_counts) > 5:
            score += 20
        elif len(keyword_counts) > 2:
            score += 10
        
        if 2.0 <= keyword_density <= 5.0:
            score += 20  # Optimal keyword density
        elif 1.0 <= keyword_density < 2.0 or 5.0 < keyword_density <= 7.0:
            score += 10  # Acceptable density
        
        return min(score, 100), {
            'keyword_density': round(keyword_density, 2),
            'found_keywords': keyword_counts,
            'total_keywords': total_keywords,
            'unique_keywords': len(keyword_counts)
        }

    def _generate_recommendations(self, formatting_issues: List[str], spacing_issues: List[str], 
                                font_issues: List[str], section_issues: List[str], 
                                keyword_analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on validation results"""
        
        recommendations = []
        
        # Priority recommendations
        if section_issues:
            recommendations.append("🔧 Fix section structure issues first - these are critical for ATS parsing")
        
        if formatting_issues:
            recommendations.append("📄 Address formatting issues to improve ATS compatibility")
        
        if spacing_issues:
            recommendations.append("📏 Clean up spacing and layout for better readability")
        
        # Keyword optimization
        if keyword_analysis.get('keyword_density', 0) < 2.0:
            recommendations.append("🔍 Include more relevant industry keywords to improve searchability")
        elif keyword_analysis.get('keyword_density', 0) > 5.0:
            recommendations.append("⚖️ Reduce keyword density to avoid appearing keyword-stuffed")
        
        if keyword_analysis.get('unique_keywords', 0) < 5:
            recommendations.append("🎯 Add more diverse technical and soft skills keywords")
        
        # General best practices
        recommendations.extend([
            "✅ Save as PDF to preserve formatting across different systems",
            "📱 Use a simple, clean layout that's mobile-friendly",
            "🔤 Stick to standard fonts like Arial, Calibri, or Times New Roman",
            "📋 Use consistent bullet points throughout the document",
            "🔍 Include a phone number and professional email address",
            "📊 Quantify achievements with specific numbers and percentages"
        ])
        
        return recommendations[:10]  # Limit to most important recommendations
