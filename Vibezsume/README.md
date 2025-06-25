# Vibezsume - AI-Powered Resume Analysis Platform

A modern web application that provides AI-powered resume analysis, ATS validation, and resume building capabilities using local Small Language Models (SLM).

## 🚀 Features

### 📄 Resume Analysis
- **AI-Powered Feedback**: Upload resumes and get intelligent feedback using local LLMs
- **Skill Gap Analysis**: Compare your skills against job descriptions
- **Vibe Check**: Get honest, conversational feedback on your resume quality

### ✅ ATS Validator
- **Formatting Check**: Analyze spacing, fonts, and layout issues
- **Compatibility Score**: Get detailed ATS compatibility ratings
- **Actionable Recommendations**: Receive specific suggestions for improvement

### 🛠️ Resume Builder
- **ATS-Friendly PDFs**: Generate professional, tracking-system optimized resumes
- **Multiple Templates**: Choose from modern, classic, and creative designs
- **Customizable Sections**: Flexible section ordering and content management

### 🧠 Local AI Integration
- **Privacy-First**: All AI processing happens locally using Ollama
- **No Data Sharing**: Your resume data never leaves your system
- **Offline Capable**: Works without internet once set up

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python 3.8+)
- **Frontend**: Modern JavaScript (ES6+) with responsive CSS
- **AI Engine**: Ollama with local language models
- **Document Processing**: PyPDF2, python-docx, ReportLab
- **UI/UX**: Progressive enhancement, mobile-first design

## 📋 Prerequisites

Before running the application, make sure you have:

1. **Python 3.8 or higher**
2. **Ollama** installed and running
3. **Git** (for cloning the repository)

### Install Ollama

1. Download Ollama from [https://ollama.ai](https://ollama.ai)
2. Install and start the Ollama service
3. Pull a language model:
   ```bash
   ollama pull llama3.2:3b
   ```

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Vibezsume
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
# The defaults should work for local development
```

### 4. Download Required NLP Models
```bash
python -m spacy download en_core_web_sm
```

### 5. Start the Application
```bash
# Development mode
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Access the Application
Open your browser and navigate to: `http://localhost:8000`

## 📱 Usage Guide

### Analyzing a Resume
1. Navigate to the "Analyze" section
2. Upload your resume (PDF or DOCX)
3. Optionally paste a job description for targeted analysis
4. Click "Analyze Resume" and wait for AI feedback

### Building a Resume
1. Go to the "Build" section
2. Fill out your information in the form
3. Choose a template style and color scheme
4. Click "Generate PDF Resume" to download

### Validating ATS Compatibility
1. Visit the "Validate" section
2. Upload a resume file or paste text
3. Add target keywords (optional)
4. Get detailed compatibility scoring and recommendations

## 🔧 Configuration

### Environment Variables

Key configuration options in `.env`:

```bash
# Application
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Ollama Configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# File Handling
MAX_FILE_SIZE_MB=10
UPLOAD_DIRECTORY=uploads
OUTPUT_DIRECTORY=generated_resumes
```

### Customizing AI Models

You can use different Ollama models by:

1. Pulling the model: `ollama pull model-name`
2. Updating the `OLLAMA_MODEL` in your `.env` file
3. Restarting the application

Recommended models:
- `llama3.2:3b` (default, good balance)
- `llama3.2:1b` (faster, less detailed)
- `mistral:7b` (alternative option)

## 🚀 Deployment

### For Production Deployment

1. **Update Environment Variables**:
   ```bash
   DEBUG=False
   ALLOWED_ORIGINS=https://yourdomain.com
   SECRET_KEY=your-secure-secret-key
   ```

2. **Use Production ASGI Server**:
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

3. **Set Up Reverse Proxy** (nginx example):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📁 Project Structure

```
Vibezsume/
├── app/
│   ├── models/           # Pydantic models
│   ├── routers/          # API endpoints
│   ├── services/         # Business logic
│   ├── static/           # CSS, JS, images
│   └── templates/        # HTML templates
├── uploads/              # Temporary file storage
├── generated_resumes/    # PDF output directory
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Development

### Adding New Features

1. **API Endpoints**: Add to `app/routers/`
2. **Business Logic**: Implement in `app/services/`
3. **Data Models**: Define in `app/models/`
4. **Frontend**: Update `app/static/` and `app/templates/`

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🛠️ Troubleshooting

### Common Issues

**Ollama Connection Error**:
- Ensure Ollama is running: `ollama serve`
- Check if the model is available: `ollama list`
- Verify OLLAMA_URL in your .env file

**File Upload Issues**:
- Check file size limits (default 10MB)
- Ensure upload directory exists and is writable
- Verify file types are supported (PDF, DOCX)

**Missing NLP Models**:
```bash
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Getting Help

- Check the application logs for detailed error messages
- Ensure all dependencies are properly installed
- Verify environment configuration
- Test Ollama connectivity independently

## 🔮 Future Enhancements

- [ ] User authentication and resume history
- [ ] Multiple language support
- [ ] Integration with job boards
- [ ] Resume templates marketplace
- [ ] Collaborative resume editing
- [ ] Analytics dashboard for recruiters

---

**Built with ❤️ for job seekers everywhere**
