
# AI-Doctor-Jhatka

![AI Doctor Logo](static/images/doctor-avatar.png)

**AI-Doctor-Jhatka** is a Flask-based web application that provides an interactive chat interface for users to consult with an AI-powered doctor. The application supports text-based conversations, image and PDF uploads, speech-to-text transcription, and text-to-speech responses. It includes user authentication, conversation history, and the ability to delete conversations, all wrapped in a modern and responsive UI.

## Features

- **User Authentication**: Register, login, and logout functionality with secure password hashing.
- **Interactive Chat**: Engage in conversations with an AI doctor, powered by a local LLM (placeholder implementation).
- **File Uploads**: Attach images and PDFs to your messages, with a user-friendly modal for file selection and recent files history.
- **Speech Integration**: Use the microphone to record speech, which is transcribed and sent as a message, with AI responses converted to speech.
- **Conversation History**: View past conversations and delete them, with associated files removed from the server.
- **Profile Page**: View user details such as username, email, age, gender, and join date.
- **Modern UI**: Gradient backgrounds, animations, and a responsive design for an enhanced user experience.
- **Database Support**: SQLite database with Flask-SQLAlchemy for storing users, conversations, and messages.
- **Flask Blueprints**: Modular code structure for better organization and scalability.


## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.8+**
- **pip** (Python package manager)
- **Virtualenv** (optional but recommended)
- **Git** (to clone the repository)
- **OLLAMA** (for running local model)
- **Llava:7b** (``` ollama run llava:7b``` to download model)

## Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/NaimParvez/AI-Doctor.git
   cd AI-Doctor
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv env
   env\Scripts\activate  # On Windows
   # source env/bin/activate  # On macOS/Linux
   ```

3. **Install Dependencies**:
   ```bash
   pip install flask flask-sqlalchemy flask-migrate flask-login werkzeug
   ```

4. **Set Up the Database**:
   Initialize the database and apply migrations:
   ```bash
   set FLASK_APP=run.py  # On Windows
   # export FLASK_APP=run.py  # On macOS/Linux
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. **Run the Application**:
   Start the Flask development server:
   ```bash
   python run.py
   ```
   The application will be available at `http://127.0.0.1:5000/`.

## Usage

1. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:5000/`. If you’re not logged in, you’ll be redirected to the login page.

2. **Register and Login**:
   - Register a new account at `/auth/register` by providing a username, email, password, date of birth, and gender.
   - Log in at `/auth/login` using your username and password.

3. **Chat with the AI Doctor**:
   - After logging in, you’ll be redirected to `/chat/`.
   - Type a message in the input field and press Enter or click the send icon to chat.
   - Use the attach icon to upload images or PDFs via the modal.
   - Use the microphone icon to record speech, which will be transcribed and sent as a message.

4. **View Conversation History**:
   - Go to `/history` to view past conversations.
   - Click the "Delete" button to remove a conversation, which also deletes associated files.

5. **View Profile**:
   - Go to `/auth/profile` to view your user details, including username, email, age, gender, and join date.

6. **Logout**:
   - Click the "Logout" link in the header to log out and return to the login page.

## Project Structure

```
AI-Doctor/
├── app/
│   ├── __init__.py              # Flask app setup and blueprint registration
│   ├── models.py                # Database models (User, Conversation, Message)
│   ├── routes/
│   │   ├── __init__.py          # Empty file for package
│   │   ├── auth.py              # Authentication routes (login, register, logout, profile)
│   │   ├── chat.py              # Chat routes (chat page, file upload, message sending)
│   │   └── main.py              # Main routes (root, history, delete conversation)
│   └── utils/
│       ├── __init__.py          # Empty file for package
│       ├── llm_local.py         # Placeholder for LLM service
│       └── speech.py            # Placeholder for speech-to-text and text-to-speech
├── static/
│   ├── css/
│   │   └── style.css            # Styles for the application
│   ├── js/
│   │   └── script.js            # JavaScript for chat interactions
│   ├── uploads/                 # Directory for uploaded files
│   └── images/
│       └── doctor-avatar.png    # Doctor avatar image
├── templates/
│   ├── base.html                # Base template
│   ├── index.html               # Chat page template
│   ├── history.html             # History page template
│   ├── login.html               # Login page template
│   ├── register.html            # Registration page template
│   └── profile.html             # Profile page template
├── config.py                    # Configuration settings
├── run.py                       # Entry point to run the application
└── README.md                    # This file
```

## Configuration

The application uses a `config.py` file for configuration. You can modify the following settings:

- **SECRET_KEY**: Used for session security. Set a secure key in production.
- **SQLALCHEMY_DATABASE_URI**: Database URI (defaults to SQLite `site.db`).
- **UPLOAD_FOLDER**: Directory for storing uploaded files (defaults to `static/uploads`).

Example `config.py`:
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
```

## Extending the Application

### Implementing the LLM Service
The `app/utils/llm_local.py` file contains a placeholder for the LLM service. Replace the placeholder with your actual LLM implementation:

```python
class LLMService:
    def process_text_only(self, text, user_info):
        # Implement your LLM logic here
        return "This is a placeholder response to your text: " + text

    def process_image_query(self, image_path, text, user_info):
        # Implement your image + text LLM logic here
        return "This is a placeholder response to your image query: " + text

llm_service = LLMService()
```

### Implementing Speech Services
The `app/utils/speech.py` file contains placeholders for speech-to-text and text-to-speech services. Replace them with your actual implementations:

```python
class SpeechService:
    def speech_to_text(self, file_path, language="en-US"):
        # Implement your speech-to-text logic here
        return "This is a placeholder transcription"

    def text_to_speech(self, text, output_path):
        # Implement your text-to-speech logic here
        # This should generate an audio file at output_path
        pass

speech_service = SpeechService()
```

## Contributing

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
