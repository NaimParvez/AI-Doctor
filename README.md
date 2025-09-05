<div align="center">
  <h1>🩺 AI Doctor Jhatka</h1>
  
  <p>
    <strong>Your AI-Powered Medical Consultation Platform</strong>
  </p>
  
  <p>
    <img src="https://img.shields.io/badge/python-v3.8+-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/flask-v3.1.0-green.svg" alt="Flask Version">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome">
    <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="Platform">
  </p>

  <img src="static/images/doctor-avatar.png" alt="AI Doctor Logo" width="150" height="150">
  
  <p>
    A sophisticated Flask-based web application that provides an interactive chat interface for AI-powered medical consultations. 
    Features multimodal interactions including text, image analysis, voice input, and speech synthesis, all wrapped in a modern, responsive UI.
  </p>
  
  <p>
    <a href="#-features">Features</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-installation">Installation</a> •
    <a href="#-usage">Usage</a> •
    <a href="#-api-reference">API</a> •
    <a href="#-contributing">Contributing</a>
  </p>
</div>

## ✨ Features

### 🔐 Authentication & Security

- **Secure User Registration & Login**: Robust authentication system with password hashing
- **Session Management**: Secure session handling with Flask-Login
- **Profile Management**: Comprehensive user profiles with medical history

### 🤖 AI-Powered Medical Consultation

- **Text-Based Conversations**: Natural language processing for medical queries
- **Multimodal Analysis**: Upload and analyze medical images (X-rays, skin conditions, etc.)
- **PDF Document Support**: Process medical reports and documents
- **Local LLM Integration**: Powered by Llava 7B model via Ollama

### 🎙️ Speech & Audio Features

- **Speech-to-Text**: Record voice queries with advanced speech recognition
- **Text-to-Speech**: AI responses converted to natural-sounding speech
- **Multiple Audio Formats**: Support for WAV, MP3, WebM formats

### 📱 Modern User Experience

- **Responsive Design**: Mobile-first approach with modern CSS Grid/Flexbox
- **Real-time Chat Interface**: Smooth, interactive messaging experience
- **File Upload Modal**: Drag-and-drop file uploads with progress indicators
- **Dark/Light Theme**: User preference-based theming
- **Progressive Web App**: Installable PWA capabilities

### 📊 Data Management

- **Conversation History**: Complete chat history with search capabilities
- **Medical Records**: Persistent storage of user medical information
- **File Management**: Organized storage and retrieval of uploaded files
- **Database Migrations**: Seamless database schema updates

### 🛠️ Technical Features

- **Modular Architecture**: Flask Blueprints for scalable code organization
- **RESTful API**: Well-structured API endpoints
- **Error Handling**: Comprehensive error management and logging
- **Environment Configuration**: Flexible deployment configurations

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/NaimParvez/AI-Doctor.git
cd AI-Doctor-Jhatka

# Set up virtual environment
python -m venv env
env\Scripts\activate  # Windows
# source env/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Set up Ollama and download the model
# Install Ollama from https://ollama.ai/
ollama pull llava:7b

# Initialize database
set FLASK_APP=run.py  # Windows
flask db upgrade

# Run the application
python run.py
```

Visit `http://127.0.0.1:5000` to start your AI medical consultation!

## 📋 Prerequisites

## 📋 Prerequisites

### System Requirements

| Component   | Minimum                               | Recommended     |
| ----------- | ------------------------------------- | --------------- |
| **Python**  | 3.8+                                  | 3.10+           |
| **RAM**     | 4GB                                   | 8GB+            |
| **Storage** | 10GB                                  | 20GB+           |
| **OS**      | Windows 10, macOS 10.14, Ubuntu 18.04 | Latest versions |

### Required Software

- **Python 3.8+** - Programming language runtime
- **pip** - Python package manager
- **Git** - Version control system
- **Ollama** - Local LLM runtime ([Download](https://ollama.ai/))
- **Llava 7B Model** - Vision-language model

### Optional Tools

- **Virtual Environment** - Recommended for dependency isolation
- **PostgreSQL** - For production database (SQLite used by default)
- **Redis** - For session storage and caching
- **Docker** - For containerized deployment

## ⚙️ Installation

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/NaimParvez/AI-Doctor.git
cd AI-Doctor-Jhatka
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate
```

### 3. Install Python Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Or install core packages manually
pip install flask flask-sqlalchemy flask-migrate flask-login werkzeug
pip install ollama pyttsx3 SpeechRecognition pillow python-dotenv
```

### 4. Set Up Ollama and AI Model

```bash
# Install Ollama (visit https://ollama.ai/ for installation guide)
# Then download the Llava model
ollama pull llava:7b

# Verify installation
ollama list
```

### 5. Environment Configuration

Create a `.env` file in the project root:

```bash
# .env file
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///app.db
OLLAMA_HOST=http://127.0.0.1:11434
FLASK_ENV=development
```

### 6. Database Setup

```bash
# Set Flask app
set FLASK_APP=run.py  # Windows
export FLASK_APP=run.py  # macOS/Linux

# Initialize database (if migrations folder doesn't exist)
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

### 7. Launch the Application

```bash
# Run development server
python run.py

# Or use Flask's built-in server
flask run --host=0.0.0.0 --port=5000
```

The application will be available at `http://127.0.0.1:5000/`

## 🐳 Docker Installation (Alternative)

```bash
# Build Docker image
docker build -t ai-doctor-jhatka .

# Run container
docker run -p 5000:5000 -v $(pwd)/instance:/app/instance ai-doctor-jhatka
```

## 📖 Usage

### Getting Started

1. **Launch the Application**

   ```bash
   python run.py
   ```

   Navigate to `http://127.0.0.1:5000/`

2. **Create an Account**

   - Click "Register" on the login page
   - Fill in your details: username, email, password, date of birth, and gender
   - Verify your email (if email verification is enabled)

3. **Start Your First Consultation**
   - Log in with your credentials
   - You'll be redirected to the chat interface
   - Type your medical question or concern

### 💬 Chat Interface Features

#### Text Conversations

- Type your medical questions naturally
- Get AI-powered responses based on medical knowledge
- View conversation history in real-time

#### 📷 Image Analysis

- Click the attachment icon (📎)
- Upload medical images (X-rays, skin conditions, symptoms)
- Supported formats: JPG, PNG, GIF, WEBP
- AI analyzes images and provides medical insights

#### 🎤 Voice Interactions

- Click the microphone icon
- Record your voice message
- Speech is automatically transcribed
- AI responds with voice synthesis

#### 📄 Document Processing

- Upload PDF medical reports
- Extract and analyze medical information
- Get insights from lab results and medical documents

### 👤 Profile Management

Navigate to `/auth/profile` to:

- View personal information
- Update medical history
- Manage account settings
- Review consultation statistics

### 📚 Conversation History

Access your medical history at `/history`:

- Browse all past consultations
- Search through conversations
- Download conversation transcripts
- Delete unwanted conversations

### 🔧 Advanced Features

#### Custom Queries

```
Examples of medical queries:
- "I have a persistent cough for 2 weeks"
- "What could this skin rash indicate?"
- "Explain my blood test results"
- "Medication interactions with aspirin"
```

#### Image Upload Tips

- Ensure good lighting for medical photos
- Use high resolution images for better analysis
- Multiple angles for skin conditions
- Include scale references when relevant

## 🏗️ Project Structure

```
AI-Doctor-Jhatka/
├── 📁 app/                          # Main application package
│   ├── __init__.py                  # Flask app factory and configuration
│   ├── models.py                    # SQLAlchemy database models
│   ├── llm_local.py                 # LLM service integration
│   ├── speech.py                    # Speech processing services
│   ├── 📁 routes/                   # Application routes (blueprints)
│   │   ├── __init__.py
│   │   ├── auth.py                  # Authentication routes
│   │   ├── chat.py                  # Chat and messaging routes
│   │   └── main.py                  # Main application routes
│   └── 📁 utils/                    # Utility modules
│       ├── __init__.py
│       ├── image_validator.py       # Image processing utilities
│       ├── llm_local.py            # Local LLM integration
│       └── speech.py               # Speech processing utilities
├── 📁 static/                       # Static assets
│   ├── 📁 css/
│   │   └── style.css               # Application styles
│   ├── 📁 js/
│   │   └── script.js               # Frontend JavaScript
│   ├── 📁 images/
│   │   └── doctor-avatar.png       # UI assets
│   └── 📁 uploads/                 # User uploaded files
├── 📁 templates/                    # Jinja2 HTML templates
│   ├── base.html                   # Base template layout
│   ├── index.html                  # Chat interface
│   ├── history.html                # Conversation history
│   ├── login.html                  # Login page
│   ├── register.html               # Registration page
│   ├── profile.html                # User profile
│   ├── forget_password.html        # Password reset
│   └── logout.html                 # Logout confirmation
├── 📁 migrations/                   # Database migration files
│   ├── alembic.ini                 # Alembic configuration
│   ├── env.py                      # Migration environment
│   └── 📁 versions/                # Migration versions
├── 📁 instance/                     # Instance-specific files
│   └── app.db                      # SQLite database file
├── 📁 models/                       # AI model storage
│   └── 📁 llava-7b/               # Llava model files
├── 📁 env/                         # Virtual environment
├── config.py                       # Application configuration
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── site.db                         # Legacy database file
└── README.md                       # Project documentation
```

### 🔧 Core Components

| Component          | Description                              | Technologies               |
| ------------------ | ---------------------------------------- | -------------------------- |
| **Backend**        | Flask web framework with SQLAlchemy ORM  | Python, Flask, SQLAlchemy  |
| **Database**       | SQLite for development, PostgreSQL ready | SQLite/PostgreSQL          |
| **AI Engine**      | Local LLM via Ollama integration         | Llava 7B, Ollama           |
| **Frontend**       | Responsive web interface                 | HTML5, CSS3, JavaScript    |
| **Authentication** | Secure user management                   | Flask-Login, Werkzeug      |
| **Speech**         | Voice input/output processing            | SpeechRecognition, pyttsx3 |
| **File Upload**    | Image and document processing            | Pillow, PyPDF2             |

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in your project root:

```bash
# Security
SECRET_KEY=your-super-secret-key-change-in-production
FLASK_ENV=development

# Database
DATABASE_URL=sqlite:///app.db
# For PostgreSQL: postgresql://username:password@localhost/dbname

# AI Model Configuration
OLLAMA_HOST=http://127.0.0.1:11434
MODEL_NAME=llava:7b

# File Upload Settings
MAX_CONTENT_LENGTH=16777216  # 16MB in bytes
UPLOAD_FOLDER=static/uploads

# Email Configuration (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Speech Services (optional)
SPEECH_RECOGNITION_TIMEOUT=5
TTS_RATE=150
```

### Configuration Class

The `config.py` file contains the main configuration:

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Security Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # Ollama Configuration
    OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'http://127.0.0.1:11434')

    # SQLite specific settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"check_same_thread": False},
        "poolclass": "StaticPool"
    }

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # Use PostgreSQL in production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

### Deployment Configurations

#### Development

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py
```

#### Production

```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

#### Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## 🔧 API Reference

### Authentication Endpoints

#### POST `/auth/register`

Register a new user account.

**Request Body:**

```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "date_of_birth": "YYYY-MM-DD",
  "gender": "male|female|other"
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Account created successfully",
  "user_id": "integer"
}
```

#### POST `/auth/login`

Authenticate user login.

**Request Body:**

```json
{
  "username": "string",
  "password": "string"
}
```

#### GET `/auth/profile`

Get user profile information.

**Response:**

```json
{
  "username": "string",
  "email": "string",
  "age": "integer",
  "gender": "string",
  "join_date": "ISO 8601 datetime"
}
```

### Chat Endpoints

#### POST `/chat/send_message`

Send a message to the AI doctor.

**Request Body:**

```json
{
  "message": "string",
  "image_path": "string (optional)",
  "conversation_id": "integer (optional)"
}
```

**Response:**

```json
{
  "status": "success",
  "response": "AI generated response",
  "conversation_id": "integer",
  "message_id": "integer"
}
```

#### POST `/chat/upload_file`

Upload a file for analysis.

**Form Data:**

- `file`: File object (image or PDF)

**Response:**

```json
{
  "status": "success",
  "filename": "string",
  "file_path": "string"
}
```

#### POST `/chat/speech_to_text`

Convert speech to text.

**Form Data:**

- `audio`: Audio file object

**Response:**

```json
{
  "status": "success",
  "transcription": "string"
}
```

### History Endpoints

#### GET `/history`

Get conversation history for the current user.

**Response:**

```json
{
  "conversations": [
    {
      "id": "integer",
      "created_at": "ISO 8601 datetime",
      "message_count": "integer",
      "last_message": "string"
    }
  ]
}
```

#### DELETE `/delete_conversation/<int:conversation_id>`

Delete a specific conversation.

**Response:**

```json
{
  "status": "success",
  "message": "Conversation deleted successfully"
}
```

### WebSocket Events

The application supports real-time communication via WebSocket:

```javascript
// Connect to WebSocket
const socket = io();

// Send message
socket.emit("send_message", {
  message: "Hello AI Doctor",
  conversation_id: 123,
});

// Receive response
socket.on("ai_response", (data) => {
  console.log(data.response);
});
```

## 🔨 Development & Extension

## 🔨 Development & Extension

### Setting Up Development Environment

1. **Install Development Dependencies**

```bash
pip install -r requirements-dev.txt  # If available
pip install pytest flask-testing coverage black flake8
```

2. **Run in Development Mode**

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py
```

3. **Database Development**

```bash
# Create new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Downgrade if needed
flask db downgrade
```

### Implementing Custom LLM Service

Replace the placeholder in `app/utils/llm_local.py`:

```python
import ollama
from typing import Optional, Dict, Any

class LLMService:
    def __init__(self, model_name: str = "llava:7b"):
        self.model_name = model_name
        self.client = ollama.Client()

    def process_text_only(self, text: str, user_info: Dict[str, Any]) -> str:
        """Process text-only medical queries"""
        try:
            prompt = self._build_medical_prompt(text, user_info)
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': 0.1,
                    'top_p': 0.9,
                    'max_tokens': 500
                }
            )
            return response['response']
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties: {str(e)}"

    def process_image_query(self, image_path: str, text: str, user_info: Dict[str, Any]) -> str:
        """Process image + text medical queries"""
        try:
            with open(image_path, 'rb') as image_file:
                response = self.client.generate(
                    model=self.model_name,
                    prompt=self._build_image_prompt(text, user_info),
                    images=[image_file.read()],
                    options={
                        'temperature': 0.1,
                        'top_p': 0.9
                    }
                )
            return response['response']
        except Exception as e:
            return f"Unable to analyze the image: {str(e)}"

    def _build_medical_prompt(self, query: str, user_info: Dict) -> str:
        """Build medical consultation prompt"""
        return f"""
        You are a knowledgeable medical AI assistant. A {user_info.get('age', 'N/A')} year old
        {user_info.get('gender', 'person')} is asking: {query}

        Please provide helpful medical information while emphasizing that this is not a
        substitute for professional medical advice. Always recommend consulting with a
        healthcare provider for proper diagnosis and treatment.
        """

    def _build_image_prompt(self, query: str, user_info: Dict) -> str:
        """Build image analysis prompt"""
        return f"""
        Analyze this medical image. The patient asks: {query}

        Please describe what you observe and provide relevant medical insights.
        Remember to recommend professional medical evaluation for accurate diagnosis.
        """

# Global instance
llm_service = LLMService()
```

### Implementing Speech Services

Enhance `app/utils/speech.py`:

```python
import speech_recognition as sr
import pyttsx3
import os
from pydub import AudioSegment
from pydub.utils import which

class SpeechService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self._configure_tts()

    def _configure_tts(self):
        """Configure text-to-speech settings"""
        voices = self.tts_engine.getProperty('voices')
        # Set female voice if available
        for voice in voices:
            if 'female' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break

        self.tts_engine.setProperty('rate', 150)  # Speaking rate
        self.tts_engine.setProperty('volume', 0.9)  # Volume level

    def speech_to_text(self, file_path: str, language: str = "en-US") -> str:
        """Convert speech to text"""
        try:
            # Convert various audio formats to WAV
            audio_file = self._convert_to_wav(file_path)

            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language=language)
                return text
        except sr.UnknownValueError:
            return "Could not understand the audio"
        except sr.RequestError as e:
            return f"Speech recognition error: {str(e)}"
        except Exception as e:
            return f"Error processing audio: {str(e)}"

    def text_to_speech(self, text: str, output_path: str) -> bool:
        """Convert text to speech"""
        try:
            self.tts_engine.save_to_file(text, output_path)
            self.tts_engine.runAndWait()
            return True
        except Exception as e:
            print(f"TTS Error: {str(e)}")
            return False

    def _convert_to_wav(self, file_path: str) -> str:
        """Convert audio file to WAV format"""
        if file_path.endswith('.wav'):
            return file_path

        try:
            audio = AudioSegment.from_file(file_path)
            wav_path = file_path.rsplit('.', 1)[0] + '.wav'
            audio.export(wav_path, format='wav')
            return wav_path
        except Exception:
            return file_path  # Return original if conversion fails

# Global instance
speech_service = SpeechService()
```

### Adding New Features

#### 1. Medical History Tracking

```python
# In models.py
class MedicalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    condition = db.Column(db.String(200), nullable=False)
    diagnosis_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

#### 2. Appointment Scheduling

```python
# In models.py
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(500))
    status = db.Column(db.String(20), default='scheduled')
```

#### 3. Medication Reminders

```python
# In models.py
class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100))
    frequency = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
```

### Testing

#### Unit Tests

```python
# tests/test_auth.py
import unittest
from app import create_app, db
from app.models import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_registration(self):
        response = self.app.test_client().post('/auth/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
```

#### Integration Tests

```bash
# Run tests
python -m pytest tests/
# With coverage
python -m pytest --cov=app tests/
```

## 🚀 Deployment

### Production Deployment Options

#### 1. Traditional Server Deployment

**Using Gunicorn (Recommended)**

```bash
# Install Gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# With configuration file
gunicorn -c gunicorn.conf.py run:app
```

**Gunicorn Configuration (`gunicorn.conf.py`)**

```python
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

#### 2. Docker Deployment

**Dockerfile**

```dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p static/uploads

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

**Docker Compose (`docker-compose.yml`)**

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./instance:/app/instance
      - ./static/uploads:/app/static/uploads
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:password@db:5432/aidoctor
      - OLLAMA_HOST=http://ollama:11434
    depends_on:
      - db
      - ollama

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=aidoctor
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  postgres_data:
  ollama_data:
```

#### 3. Cloud Platform Deployment

**Heroku**

```bash
# Create Procfile
echo "web: gunicorn run:app" > Procfile

# Deploy to Heroku
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

**AWS EC2**

```bash
# Install dependencies on EC2
sudo yum update -y
sudo yum install python3 python3-pip nginx -y

# Clone repository and setup
git clone https://github.com/NaimParvez/AI-Doctor.git
cd AI-Doctor-Jhatka
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Configure Nginx reverse proxy
sudo nano /etc/nginx/conf.d/aidoctor.conf
```

**Nginx Configuration**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/AI-Doctor-Jhatka/static;
        expires 30d;
    }
}
```

### Environment Setup for Production

```bash
# .env for production
SECRET_KEY=super-secret-production-key-here
FLASK_ENV=production
DATABASE_URL=postgresql://username:password@localhost/aidoctor_prod
OLLAMA_HOST=http://localhost:11434
MAX_CONTENT_LENGTH=52428800  # 50MB

# Security settings
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
PERMANENT_SESSION_LIFETIME=1800  # 30 minutes
```

### Performance Optimization

#### Database Optimization

```python
# In config.py for production
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 20,
    'pool_recycle': 300,
    'pool_pre_ping': True
}
```

#### Caching Setup

```python
# Install Redis
pip install redis flask-caching

# In app/__init__.py
from flask_caching import Cache
cache = Cache()

# Configure caching
cache.init_app(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})
```

#### Monitoring and Logging

```python
# In run.py for production
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/aidoctor.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

## 🧪 Testing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request with a detailed description of your changes.

Please ensure your code follows the project’s coding style and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, please reach out to [Naim Parvez](mailto:parveznaim0@gmail.com),[ Sartaj Alam Pritom](mailto:sartajalam0010@gmail.com),[ Jerin Romijah Tuli](mailto:ramijahtuli786@gmail.com).
