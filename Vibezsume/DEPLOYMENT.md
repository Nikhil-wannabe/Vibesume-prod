# Vibezsume Deployment Guide

## Free Deployment Options

### Option 1: Render (Recommended)
1. Go to [render.com](https://render.com) and sign up with GitHub
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free
5. Set environment variables:
   - `PYTHON_VERSION`: `3.11.0`
6. Deploy!

**Pros**: Easy setup, good free tier, automatic deployments
**Cons**: Apps sleep after 15 minutes of inactivity

### Option 2: Koyeb
1. Go to [koyeb.com](https://www.koyeb.com)
2. Connect GitHub repository
3. Configure as Python app
4. Deploy

**Pros**: No sleep mode, 512MB RAM
**Cons**: Smaller community

### Option 3: PythonAnywhere
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create free account
3. Upload files or clone from GitHub
4. Configure WSGI file for FastAPI

**Pros**: Always-on, good Python support
**Cons**: More manual setup required

### Option 4: Deta Space
1. Go to [deta.space](https://deta.space)
2. Install Deta CLI
3. Deploy with: `deta deploy`

**Pros**: Completely free, no limits
**Cons**: Newer platform, less documentation

## Important Notes

⚠️ **Ollama Limitation**: Local LLM (Ollama) won't work on these free platforms. The app will fall back to basic analysis without AI features.

✅ **What Will Work**:
- Resume file upload and parsing
- Basic resume analysis (without AI)
- Resume builder and PDF generation
- ATS validation
- Beautiful responsive UI

❌ **What Won't Work**:
- AI-powered resume analysis (requires local Ollama)
- Skill gap analysis with LLM
- Vibe check feedback

## Files Included for Deployment
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification  
- `Procfile` - Process configuration
- `render.yaml` - Render-specific configuration
