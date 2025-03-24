# AI Doctor with Vision and Voice

A Flask-based AI medical assistant ("Dr. Cleopetra") with vision and voice capabilities.

## Features
- Local LLaVA-7B model via Ollama for text and image analysis
- Whisper model for speech-to-text (English/Bangla)
- gTTS for text-to-speech
- User authentication and conversation history
- Responsive chatbot frontend

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Install Ollama: Follow instructions at https://ollama.ai/, then `ollama pull llava:7b`
3. Run Ollama: `ollama serve` (runs on http://localhost:11434)
4. Set up `.env` with `SECRET_KEY=your-secret-key` and optionally `OLLAMA_HOST`
5. Run migrations: `flask db init`, `flask db migrate`, `flask db upgrade`
6. Start the app: `python run.py`

## Usage
- Register/login to access the chatbot
- Use text, voice, or images to interact
- View conversation history at `/history`