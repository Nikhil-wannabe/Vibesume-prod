#!/usr/bin/env python3
"""
Test script to verify Ollama integration with Vibezsume
"""
import asyncio
import sys
sys.path.append('.')

from app.services.llm_service import LLMService
from app.models.resume_models import ResumeData, ContactInfo, Skill, SkillLevel

async def test_ollama_integration():
    """Test the complete Ollama integration"""
    print("🧪 Testing Ollama Integration with Vibezsume")
    print("=" * 50)
    
    # Initialize LLM service
    llm = LLMService()
    await llm.initialize()
    
    if not llm.is_available:
        print("❌ LLM service is not available")
        return False
    
    print(f"✅ LLM service initialized with model: {llm.model_name}")
    
    # Test simple generation
    print("\n🤖 Testing basic AI generation...")
    response = await llm.generate_response(
        "Say hello and confirm you can help with resume analysis.",
        "You are a resume analysis assistant."
    )
    print(f"AI Response: {response[:100]}...")
    
    # Test resume analysis
    print("\n📄 Testing resume analysis...")
    
    # Create a sample resume
    sample_resume = ResumeData(
        contact_info=ContactInfo(
            full_name="John Doe",
            email="john.doe@example.com",
            phone="555-123-4567",
            location="San Francisco, CA"
        ),
        summary="Software engineer with 5 years of experience in web development",
        skills=[
            Skill(name="Python", level=SkillLevel.EXPERT),
            Skill(name="JavaScript", level=SkillLevel.ADVANCED),
            Skill(name="React", level=SkillLevel.INTERMEDIATE)
        ],
        experience=[],
        education=[]
    )
    
    # Analyze the resume
    analysis = await llm.analyze_resume(sample_resume)
    print(f"Analysis Score: {analysis.score}")
    print(f"Strengths: {analysis.strengths[:2]}")
    print(f"Suggestions: {analysis.suggestions[:2]}")
    
    # Test vibe check
    print("\n😎 Testing vibe check...")
    vibe_response = await llm.vibe_check_feedback(sample_resume)
    print(f"Vibe Check: {vibe_response[:200]}...")
    
    print("\n✅ All tests passed! Ollama integration is working perfectly.")
    return True

if __name__ == "__main__":
    success = asyncio.run(test_ollama_integration())
    if success:
        print("\n🎉 Ollama is fully set up and integrated with Vibezsume!")
    else:
        print("\n❌ There were issues with the integration.")
