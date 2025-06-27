"""
Simple import test for deployment readiness
"""

def test_basic_imports():
    """Test basic imports work"""
    print("Testing basic imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
        
    try:
        import PyPDF2
        print("✅ PyPDF2 imported")
    except ImportError as e:
        print(f"❌ PyPDF2 import failed: {e}")
        return False
        
    try:
        import httpx
        print("✅ httpx imported")
    except ImportError as e:
        print(f"❌ httpx import failed: {e}")
        return False
        
    try:
        from app.models.resume_models import ResumeData
        print("✅ Resume models imported")
    except ImportError as e:
        print(f"❌ Resume models import failed: {e}")
        return False
        
    try:
        from app.services.llm_service import LLMService
        print("✅ LLM service imported")
    except ImportError as e:
        print(f"❌ LLM service import failed: {e}")
        return False
        
    return True

if __name__ == "__main__":
    print("🚀 Vibezsume Basic Import Test")
    print("=" * 40)
    
    success = test_basic_imports()
    
    if success:
        print("\n✅ All basic imports successful!")
        print("The app should be ready for deployment.")
    else:
        print("\n❌ Some imports failed.")
        print("Fix import issues before deployment.")
