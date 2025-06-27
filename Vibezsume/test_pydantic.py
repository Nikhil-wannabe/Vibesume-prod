"""
Minimal test for Pydantic compatibility
"""

print("Testing Pydantic compatibility...")

try:
    from pydantic import BaseModel, Field
    from typing import Optional
    
    print("✅ Pydantic imports successful")
    
    # Test basic model creation
    class TestModel(BaseModel):
        name: str
        email: Optional[str] = None
    
    # Test model instantiation
    test_obj = TestModel(name="test", email="test@example.com")
    print("✅ Pydantic model creation successful")
    
    # Test dict conversion (Pydantic v1 style)
    data = test_obj.dict()
    print("✅ Pydantic .dict() method works")
    print(f"Model data: {data}")
    
except Exception as e:
    print(f"❌ Pydantic test failed: {e}")
    import traceback
    traceback.print_exc()

print("Pydantic test completed.")
