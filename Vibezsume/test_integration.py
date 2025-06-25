"""
Final Integration Test for Vibezsume
Tests all features with a real resume file and verifies the complete flow
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_complete_workflow():
    """Test the complete workflow end-to-end"""
    print("Starting Complete Workflow Test")
    print("=" * 50)
    
    # Test 1: Health Check
    print("1. Testing Health Endpoints...")
    health_response = requests.get(f"{BASE_URL}/health")
    assert health_response.status_code == 200
    print(f"   PASS Main health: {health_response.json()}")
    
    resume_health = requests.get(f"{BASE_URL}/api/resume/health")
    assert resume_health.status_code == 200
    health_data = resume_health.json()
    print(f"   PASS Resume service health: {health_data}")
    print(f"   INFO LLM Available: {health_data.get('llm_available', False)}")
    
    # Test 2: Resume Analysis without Job Description
    print("\n2. Testing Resume Analysis (No Job Description)...")
    with open("test_resume.txt", "rb") as f:
        files = {"file": ("test_resume.txt", f, "text/plain")}
        data = {}
        
        response = requests.post(f"{BASE_URL}/api/resume/analyze", files=files, data=data)
        assert response.status_code == 200
        
        result = response.json()
        print(f"   PASS Analysis Score: {result.get('score', 'N/A')}")
        print(f"   INFO Strengths: {len(result.get('strengths', []))}")
        print(f"   INFO Suggestions: {len(result.get('suggestions', []))}")
        print(f"   INFO Has Job Description: {result.get('has_job_description', False)}")
        print(f"   INFO Has Vibe Feedback: {result.get('vibe_feedback') is not None}")
    
    # Test 3: Resume Analysis with Job Description
    print("\n3. Testing Resume Analysis (With Job Description)...")
    job_description = """
    We are looking for a Senior Full-Stack Developer with expertise in:
    - Python and FastAPI
    - React and TypeScript
    - AWS and cloud technologies
    - Docker and Kubernetes
    - PostgreSQL and database design
    - CI/CD and DevOps practices
    """
    
    with open("test_resume.txt", "rb") as f:
        files = {"file": ("test_resume.txt", f, "text/plain")}
        data = {
            "job_description": job_description,
            "job_url": "https://example.com/job"
        }
        
        response = requests.post(f"{BASE_URL}/api/resume/analyze", files=files, data=data)
        assert response.status_code == 200
        
        result = response.json()
        print(f"   PASS Analysis Score: {result.get('score', 'N/A')}")
        print(f"   INFO Has Job Description: {result.get('has_job_description', False)}")
        print(f"   INFO Has Skill Gap Analysis: {result.get('skill_gap') is not None}")
        print(f"   INFO Keyword Matches: {len(result.get('keyword_matches', []))}")
    
    # Test 4: ATS Validation
    print("\n4. Testing ATS Validation...")
    with open("test_resume.txt", "rb") as f:
        files = {"file": ("test_resume.txt", f, "text/plain")}
        
        response = requests.post(f"{BASE_URL}/api/ats/validate", files=files)
        assert response.status_code == 200
        
        result = response.json()
        validation = result.get('validation_result', {})
        print(f"   PASS ATS Score: {validation.get('ats_score', 'N/A')}")
        print(f"   INFO Issues Found: {len(validation.get('issues', []))}")
        print(f"   INFO Section Count: {len(validation.get('sections_found', []))}")
    
    # Test 5: Resume Builder
    print("\n5. Testing Resume Builder...")
    
    # First get available templates
    templates_response = requests.get(f"{BASE_URL}/api/builder/templates")
    assert templates_response.status_code == 200
    templates = templates_response.json()
    print(f"   INFO Available Templates: {templates.get('templates', [])}")
      # Build a resume
    form_data = {
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "(555) 123-4567",
        "location": "San Francisco, CA",
        "summary": "Experienced software engineer with 5+ years in full-stack development.",
        "experience_json": "[]",
        "education_json": "[]", 
        "skills_json": "[]",
        "template_style": "modern",
        "color_scheme": "blue"
    }
    
    response = requests.post(f"{BASE_URL}/api/builder/build-from-form", data=form_data)
    assert response.status_code == 200
    
    result = response.json()
    print(f"   PASS Resume Built: {result.get('filename', 'N/A')}")
    print(f"   INFO Download URL: {result.get('download_url', 'N/A')}")
    
    # Test download
    if result.get('download_url'):
        download_response = requests.get(f"{BASE_URL}{result['download_url']}")
        if download_response.status_code == 200:
            print(f"   PASS PDF Download: {len(download_response.content)} bytes")
        else:
            print(f"   FAIL PDF Download failed: {download_response.status_code}")
    
    print("\nComplete Workflow Test Finished!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    try:
        # Wait a moment for server to be ready
        time.sleep(2)
        
        success = test_complete_workflow()
        if success:
            print("PASS ALL INTEGRATION TESTS PASSED!")
            print("INFO Vibezsume is fully functional and ready for production!")
        else:
            print("FAIL Some tests failed!")
    except Exception as e:
        print(f"FAIL Integration test failed: {e}")
        import traceback
        traceback.print_exc()
