#!/usr/bin/env python3
"""
Test script to validate Vibezsume deployment readiness
"""

import sys
import traceback

def test_imports():
    """Test all critical imports"""
    print("Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
        
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
        
    try:
        import PyPDF2
        print("✅ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"❌ PyPDF2 import failed: {e}")
        return False
        
    try:
        import httpx
        print("✅ httpx imported successfully")
    except ImportError as e:
        print(f"❌ httpx import failed: {e}")
        return False
        
    try:
        import pydantic
        print("✅ Pydantic imported successfully")
    except ImportError as e:
        print(f"❌ Pydantic import failed: {e}")
        return False
        
    return True

def test_app_import():
    """Test main app import"""
    print("\nTesting main app import...")
    
    try:
        import main
        print("✅ Main app imported successfully")
        
        # Check if app is FastAPI instance
        if hasattr(main, 'app'):
            print("✅ FastAPI app instance found")
            return True
        else:
            print("❌ FastAPI app instance not found")
            return False
            
    except Exception as e:
        print(f"❌ Main app import failed: {e}")
        traceback.print_exc()
        return False

def test_health_endpoint():
    """Test if health endpoint is accessible"""
    print("\nTesting health endpoint...")
    
    try:
        import main
        app = main.app
        
        # Check if health endpoint exists
        routes = [route.path for route in app.routes]
        if "/health" in routes:
            print("✅ Health endpoint found")
            return True
        else:
            print("❌ Health endpoint not found")
            return False
            
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Vibezsume Deployment Readiness Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Run tests
    all_tests_passed &= test_imports()
    all_tests_passed &= test_app_import()
    all_tests_passed &= test_health_endpoint()
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! Ready for deployment.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Fix issues before deployment.")
        sys.exit(1)
