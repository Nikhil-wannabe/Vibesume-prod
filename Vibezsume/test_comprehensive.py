#!/usr/bin/env python3
"""
Comprehensive testing script for Vibezsume functionality
"""
import asyncio
import requests
import json
import os
from pathlib import Path

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_DATA_DIR = Path("test_data")
TEST_DATA_DIR.mkdir(exist_ok=True)

class VibezsumeTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        
    def test_health_endpoints(self):
        """Test all health check endpoints"""
        print("🏥 Testing Health Endpoints...")
        
        endpoints = [
            "/health",
            "/api/resume/health",
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                print(f"  ✅ {endpoint}: {response.status_code} - {response.json()}")
            except Exception as e:
                print(f"  ❌ {endpoint}: Error - {e}")
    
    def test_frontend_loading(self):
        """Test if frontend loads correctly"""
        print("\n🌐 Testing Frontend Loading...")
        
        try:
            response = self.session.get(self.base_url)
            if response.status_code == 200 and "Vibezsume" in response.text:
                print("  ✅ Frontend loads successfully")
                print(f"  📄 Page size: {len(response.text)} characters")
            else:
                print(f"  ❌ Frontend failed to load: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Frontend error: {e}")
    
    def create_test_resume_file(self):
        """Create a simple test resume file"""
        test_file = TEST_DATA_DIR / "test_resume.txt"
        
        resume_content = """John Doe
john.doe@email.com
(555) 123-4567
San Francisco, CA

PROFESSIONAL SUMMARY
Experienced software engineer with 5 years of expertise in web development, 
specializing in Python, JavaScript, and cloud technologies.

EXPERIENCE
Software Engineer | Tech Company | 2020-2025
- Developed scalable web applications using Python and React
- Improved system performance by 40%
- Led a team of 3 developers

Junior Developer | Startup Inc | 2018-2020  
- Built responsive web interfaces
- Collaborated with design team on UI/UX improvements

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2018

SKILLS
Python, JavaScript, React, Node.js, AWS, Docker, SQL, Git
"""
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(resume_content)
        
        return test_file
    
    def test_resume_analysis_without_job_description(self):
        """Test resume analysis without job description"""
        print("\n📊 Testing Resume Analysis (No Job Description)...")
        
        test_file = self.create_test_resume_file()
        
        try:
            with open(test_file, 'rb') as f:
                files = {'file': ('test_resume.txt', f, 'text/plain')}
                data = {}
                
                response = self.session.post(
                    f"{self.base_url}/api/resume/analyze", 
                    files=files, 
                    data=data
                )
            
            if response.status_code == 200:
                result = response.json()
                print("  ✅ Analysis completed successfully")
                print(f"  📊 Score: {result.get('score', 'N/A')}")
                print(f"  💪 Strengths: {len(result.get('strengths', []))} items")
                print(f"  📝 Suggestions: {len(result.get('suggestions', []))} items")
                print(f"  😎 Vibe feedback available: {bool(result.get('vibe_feedback'))}")
                return True
            else:
                print(f"  ❌ Analysis failed: {response.status_code}")
                print(f"  📄 Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"  ❌ Analysis error: {e}")
            return False
    
    def test_resume_analysis_with_job_description(self):
        """Test resume analysis with job description"""
        print("\n📊 Testing Resume Analysis (With Job Description)...")
        
        test_file = self.create_test_resume_file()
        job_description = """
        We are looking for a Senior Python Developer with experience in:
        - Python and Django/Flask frameworks
        - JavaScript and React
        - AWS cloud services
        - Docker containerization
        - Agile development methodologies
        - Team leadership experience
        """
        
        try:
            with open(test_file, 'rb') as f:
                files = {'file': ('test_resume.txt', f, 'text/plain')}
                data = {
                    'job_description': job_description,
                    'job_url': 'https://example.com/job/123'
                }
                
                response = self.session.post(
                    f"{self.base_url}/api/resume/analyze", 
                    files=files, 
                    data=data
                )
            
            if response.status_code == 200:
                result = response.json()
                print("  ✅ Analysis with job description completed")
                print(f"  📊 Score: {result.get('score', 'N/A')}")
                print(f"  🎯 Has job description: {result.get('has_job_description', False)}")
                print(f"  📈 Skill gap analysis: {bool(result.get('skill_gap'))}")
                return True
            else:
                print(f"  ❌ Analysis failed: {response.status_code}")
                print(f"  📄 Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"  ❌ Analysis error: {e}")
            return False
    
    def test_resume_builder(self):
        """Test resume builder functionality"""
        print("\n🏗️ Testing Resume Builder...")
        
        try:
            # Test getting available templates
            response = self.session.get(f"{self.base_url}/api/builder/templates")
            if response.status_code == 200:
                templates = response.json()
                print(f"  ✅ Templates available: {templates.get('templates', [])}")
            
            # Test building a resume
            form_data = {
                'full_name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '555-123-4567',
                'location': 'San Francisco, CA',
                'summary': 'Experienced software engineer with 5 years of expertise.',
                'experience_json': json.dumps([{
                    'position': 'Software Engineer',
                    'company': 'Tech Company',
                    'start_date': '2020-01',
                    'end_date': '2025-01',
                    'description': ['Developed scalable web applications'],
                    'technologies': ['Python', 'React']
                }]),
                'education_json': json.dumps([{
                    'degree': 'Bachelor of Science',
                    'field_of_study': 'Computer Science',
                    'institution': 'University of Technology',
                    'graduation_year': '2018'
                }]),
                'skills_json': json.dumps([
                    {'name': 'Python', 'level': 'expert'},
                    {'name': 'JavaScript', 'level': 'advanced'}
                ]),
                'template_style': 'modern',
                'color_scheme': 'blue'
            }
            
            response = self.session.post(
                f"{self.base_url}/api/builder/build-from-form",
                data=form_data
            )
            
            if response.status_code == 200:
                result = response.json()
                print("  ✅ Resume built successfully")
                print(f"  📄 Download URL: {result.get('download_url', 'N/A')}")
                return True
            else:
                print(f"  ❌ Resume builder failed: {response.status_code}")
                print(f"  📄 Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"  ❌ Resume builder error: {e}")
            return False
    
    def test_ats_validator(self):
        """Test ATS validator functionality"""
        print("\n✅ Testing ATS Validator...")
        
        test_file = self.create_test_resume_file()
        
        try:
            with open(test_file, 'rb') as f:
                files = {'file': ('test_resume.txt', f, 'text/plain')}
                data = {'target_keywords': 'python, javascript, react, aws'}
                
                response = self.session.post(
                    f"{self.base_url}/api/ats/validate", 
                    files=files, 
                    data=data
                )
            
            if response.status_code == 200:
                result = response.json()
                print("  ✅ ATS validation completed")
                print(f"  📊 ATS Score: {result.get('ats_score', 'N/A')}")
                return True
            else:
                print(f"  ❌ ATS validation failed: {response.status_code}")
                print(f"  📄 Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"  ❌ ATS validation error: {e}")
            return False
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 Starting Vibezsume Comprehensive Testing")
        print("=" * 50)
        
        results = []
        
        # Run all tests
        self.test_health_endpoints()
        self.test_frontend_loading()
        
        results.append(("Resume Analysis (No Job)", self.test_resume_analysis_without_job_description()))
        results.append(("Resume Analysis (With Job)", self.test_resume_analysis_with_job_description()))
        results.append(("Resume Builder", self.test_resume_builder()))
        results.append(("ATS Validator", self.test_ats_validator()))
        
        # Print summary
        print("\n📋 Test Summary")
        print("=" * 30)
        passed = 0
        total = len(results)
        
        for test_name, passed_test in results:
            status = "✅ PASS" if passed_test else "❌ FAIL"
            print(f"  {status} {test_name}")
            if passed_test:
                passed += 1
        
        print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 All tests passed! Vibezsume is working perfectly!")
        else:
            print("⚠️ Some tests failed. Check the logs above for details.")
        
        return passed == total

if __name__ == "__main__":
    tester = VibezsumeTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)
