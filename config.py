import os
from dotenv import load_dotenv
from sqlalchemy.pool import StaticPool

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max upload size of 16MB
    OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'http://127.0.0.1:11434')
    
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool
    }