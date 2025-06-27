"""
Test Pydantic v2 compatibility for deployment
"""

print("Testing Pydantic v2 compatibility...")

try:
    from pydantic import BaseModel, Field, EmailStr, HttpUrl
    from typing import Optional
    
    print("✅ Pydantic v2 imports successful")
    
    # Test model creation with v2
    class TestModel(BaseModel):
        name: str
        email: Optional[EmailStr] = None
        website: Optional[HttpUrl] = None
    
    # Test model instantiation
    test_obj = TestModel(
        name="test", 
        email="test@example.com",
        website="https://example.com"
    )
    print("✅ Pydantic v2 model creation successful")
    
    # Test model_dump (Pydantic v2 method)
    data = test_obj.model_dump()
    print("✅ Pydantic v2 .model_dump() method works")
    print(f"Model data: {data}")
    
    # Test our resume models
    from app.models.resume_models import ContactInfo, ResumeData
    
    contact = ContactInfo(
        full_name="Test User",
        email="test@example.com",
        phone="123-456-7890"
    )
    print("✅ Resume models work with Pydantic v2")
    print(f"Contact data: {contact.model_dump()}")
    
except Exception as e:
    print(f"❌ Pydantic v2 test failed: {e}")
    import traceback
    traceback.print_exc()

print("Pydantic v2 test completed.")
