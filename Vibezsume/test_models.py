"""
Test our actual models
"""

print("Testing our resume models...")

try:
    from app.models.resume_models import ResumeData, ContactInfo, Experience, Education, Skill
    print("✅ All resume models imported successfully")
    
    # Test model creation
    contact = ContactInfo(
        full_name="Test User",
        email="test@example.com",
        phone="123-456-7890"
    )
    print("✅ ContactInfo model created")
    
    # Test dict conversion
    contact_data = contact.dict()
    print("✅ ContactInfo .dict() works")
    print(f"Contact data: {contact_data}")
    
except Exception as e:
    print(f"❌ Resume models test failed: {e}")
    import traceback
    traceback.print_exc()

print("Resume models test completed.")
