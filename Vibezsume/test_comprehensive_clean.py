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
        print("Testing Health Endpoints...")
        
        endpoints = [
            "/health",
            "/api/resume/health",
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                print(f"  PASS {endpoint}: {response.status_code} - {response.json()}")
            except Exception as e:
                print(f"  FAIL {endpoint}: Error - {e}")
    
    def test_frontend_loading(self):
        """Test if frontend loads correctly"""
        print("\nTesting Frontend Loading...")
        
        try:
            response = self.session.get(self.base_url)
            if response.status_code == 200 and "Vibezsume" in response.text:
                print("  PASS Frontend loads successfully")
                print(f"  INFO Page size: {len(response.text)} characters")
            else:
                print(f"  FAIL Frontend failed to load: {response.status_code}")
        except Exception as e:
            print(f"  FAIL Frontend error: {e}")
    
    def create_test_resume(self):
        """Create test resume file"""
        test_resume_content = """John Doe
Software Engineer
Email: john.doe@example.com  
Phone: (555) 123-4567
LinkedIn: linkedin.com/in/johndoe
GitHub: github.com/johndoe
Location: San Francisco, CA

PROFESSIONAL SUMMARY
Experienced software engineer with 5+ years in full-stack web development. 
Proficient in Python, JavaScript, and modern frameworks. Strong background 
in building scalable applications and working with cross-functional teams.

EXPERIENCE
Senior Software Engineer | Tech Corp | 2021 - Present
• Developed and maintained web applications using Python Flask and React
• Implemented RESTful APIs serving 10,000+ daily active users
• Collaborated with product team to define technical requirements
• Mentored junior developers and conducted code reviews

Software Engineer | StartupXYZ | 2019 - 2021  
• Built responsive web interfaces using JavaScript and CSS frameworks
• Integrated third-party APIs and payment processing systems
• Participated in agile development process and sprint planning
• Optimized application performance resulting in 30% faster load times

EDUCATION
Bachelor of Science in Computer Science | University of California | 2019
• Relevant Coursework: Data Structures, Algorithms, Database Systems
• GPA: 3.7/4.0

SKILLS
Programming Languages: Python, JavaScript, TypeScript, Java, SQL
Frameworks & Libraries: React, Flask, FastAPI, Node.js, Express
Databases: PostgreSQL, MongoDB, Redis, MySQL
Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD, Git
Tools: VS Code, JIRA, Slack, Figma

PROJECTS
E-commerce Platform | 2022
• Built full-stack e-commerce application with payment integration
• Technologies: React, Python Flask, PostgreSQL, Stripe API

Task Management App | 2021
• Developed collaborative task management tool for teams
• Technologies: Vue.js, Node.js, MongoDB, Socket.io"""
        
        test_file = TEST_DATA_DIR / "test_resume.txt"
        test_file.write_text(test_resume_content)
        return test_file
    
    def test_resume_analysis_no_job(self):
        """Test resume analysis without job description"""
        print("\nTesting Resume Analysis (No Job Description)...")
        
        try:
            test_file = self.create_test_resume()
            
            with open(test_file, 'rb') as f:
                files = {'file': ('test_resume.txt', f, 'text/plain')}
                response = self.session.post(f"{self.base_url}/api/resume/analyze", files=files)
            
            if response.status_code == 200:
                result = response.json()
                print("  PASS Analysis completed successfully")
                print(f"  INFO Score: {result.get('score', 'N/A')}")
                print(f"  INFO Strengths: {len(result.get('strengths', []))} items")
                print(f"  INFO Suggestions: {len(result.get('suggestions', []))} items")
                print(f"  INFO Vibe feedback available: {result.get('vibe_feedback') is not None}")
                return True
            else:
                print(f"  FAIL Analysis failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"  FAIL Analysis error: {e}")
            return False
    
    def test_resume_analysis_with_job(self):
        """Test resume analysis with job description"""
        print("\nTesting Resume Analysis (With Job Description)...")
        
        try:
            test_file = self.create_test_resume()
            job_description = """We are seeking a Senior Full-Stack Developer to join our team.
            
Required Skills:
- 5+ years of experience in web development
- Proficiency in Python and JavaScript
- Experience with React and modern front-end frameworks  
- Knowledge of RESTful API design and implementation
- Experience with cloud platforms (AWS, Azure, or GCP)
- Strong understanding of database design (SQL and NoSQL)
- Experience with version control (Git) and CI/CD pipelines

Preferred Skills:
- Experience with FastAPI or Flask
- Knowledge of Docker and Kubernetes
- Experience with microservices architecture
- Background in agile development methodologies"""
            
            with open(test_file, 'rb') as f:
                files = {'file': ('test_resume.txt', f, 'text/plain')}
                data = {'job_description': job_description}
                response = self.session.post(f"{self.base_url}/api/resume/analyze", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print("  PASS Analysis with job description completed")
                print(f"  INFO Score: {result.get('score', 'N/A')}")
                print(f"  INFO Has job description: {result.get('has_job_description', False)}")
                print(f"  INFO Skill gap analysis: {result.get('skill_gap') is not None}")
                return True
            else:
                print(f"  FAIL Analysis failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"  FAIL Analysis error: {e}")
            return False
    
    def test_resume_builder(self):
        """Test resume builder functionality"""
        print("\nTesting Resume Builder...")
        
        try:
            # Test templates endpoint
            response = self.session.get(f"{self.base_url}/api/builder/templates")
            if response.status_code == 200:
                templates = response.json()
                print(f"  PASS Templates available: {templates.get('templates', [])}")
            else:
                print(f"  FAIL Templates endpoint failed: {response.status_code}")
                return False
            
            # Test resume building
            form_data = {
                'full_name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '(555) 123-4567',
                'location': 'San Francisco, CA',
                'summary': 'Experienced software engineer with expertise in web development.',
                'experience_json': json.dumps([
                    {
                        'title': 'Senior Software Engineer',
                        'company': 'Tech Corp',
                        'start_date': '2021-01',
                        'end_date': 'Present',
                        'description': 'Developed web applications using Python and React'
                    }
                ]),
                'education_json': json.dumps([
                    {
                        'degree': 'Bachelor of Science',
                        'field': 'Computer Science',
                        'institution': 'University of California',
                        'graduation_date': '2019-05'
                    }
                ]),
                'skills_json': json.dumps([
                    {'name': 'Python', 'level': 'expert'},
                    {'name': 'JavaScript', 'level': 'advanced'},
                    {'name': 'React', 'level': 'advanced'}
                ]),
                'template_style': 'modern',
                'color_scheme': 'blue'
            }
            
            response = self.session.post(f"{self.base_url}/api/builder/build-from-form", data=form_data)
            if response.status_code == 200:
                result = response.json()
                print("  PASS Resume built successfully")
                print(f"  INFO Download URL: {result.get('download_url', 'N/A')}")
                return True
            else:
                print(f"  FAIL Resume building failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"  FAIL Resume builder error: {e}")
            return False
    
    def test_ats_validator(self):
        """Test ATS validator functionality"""
        print("\nTesting ATS Validator...")
        
        try:
            test_file = self.create_test_resume()
            
            with open(test_file, 'rb') as f:
                files = {'file': ('test_resume.txt', f, 'text/plain')}
                response = self.session.post(f"{self.base_url}/api/ats/validate", files=files)
            
            if response.status_code == 200:
                result = response.json()
                validation = result.get('validation_result', {})
                print("  PASS ATS validation completed")
                print(f"  INFO ATS Score: {validation.get('ats_score', 'N/A')}")
                return True
            else:
                print(f"  FAIL ATS validation failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"  FAIL ATS validator error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests and provide summary"""
        print("Starting Vibezsume Comprehensive Testing")
        print("=" * 50)
        
        # Health and frontend tests
        self.test_health_endpoints()
        self.test_frontend_loading()
        
        # Main functionality tests
        tests = [
            ("Resume Analysis (No Job)", self.test_resume_analysis_no_job),
            ("Resume Analysis (With Job)", self.test_resume_analysis_with_job),
            ("Resume Builder", self.test_resume_builder),
            ("ATS Validator", self.test_ats_validator)
        ]
        
        passed = 0
        total = len(tests)
        results = []
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    results.append(f"  PASS {test_name}")
                    passed += 1
                else:
                    results.append(f"  FAIL {test_name}")
            except Exception as e:
                results.append(f"  FAIL {test_name}: {e}")
        
        # Print summary
        print("\nTest Summary")
        print("=" * 30)
        for result in results:
            print(result)
        
        success_rate = (passed / total) * 100
        print(f"Overall: {passed}/{total} tests passed ({success_rate:.1f}%)")
        
        if passed == total:
            print("All tests passed! Vibezsume is working perfectly!")
        else:
            print("Some tests failed. Please check the errors above.")

def main():
    """Main test execution"""
    tester = VibezsumeTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
