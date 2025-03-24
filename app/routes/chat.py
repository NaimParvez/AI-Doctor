import os
import time
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Conversation, Message
from app.utils.llm_local import llm_service
from app.utils.speech import speech_service

chat_bp = Blueprint('chat', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'webm', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_info():
    if not current_user.is_authenticated:
        return None
    user_info = {
        'username': current_user.username,
        'email': current_user.email,
        'medical_history': current_user.get_medical_history()
    }
    if current_user.age:
        user_info['age'] = current_user.age
    if current_user.gender:
        user_info['gender'] = current_user.gender
    return user_info

@chat_bp.route('/')
@login_required
def chat_page():
    conversations = Conversation.query.filter_by(user_id=current_user.id).order_by(Conversation.start_time.asc()).all()
    return render_template('index.html', username=current_user.username, conversations=conversations)

@chat_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{int(time.time())}_{file.filename}")
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        relative_path = f"/static/uploads/{filename}"
        
        if filename.lower().endswith(('.mp3', '.wav', '.webm')):
            transcription = speech_service.speech_to_text(file_path, language="en-US")
            return jsonify({
                'file_path': relative_path,
                'transcription': transcription,
                'file_type': 'audio',
                'detected_language': 'en'
            })
        elif filename.lower().endswith('.pdf'):
            return jsonify({'file_path': relative_path, 'file_type': 'pdf'})
        else:
            return jsonify({'file_path': relative_path, 'file_type': 'image'})
    
    return jsonify({'error': 'File type not allowed'}), 400

@chat_bp.route('/message', methods=['POST'])
@login_required
def send_message():
    data = request.json
    text_content = data.get('text', '')
    file_path = data.get('image_path')
    audio_path = data.get('audio_path')
    conversation_id = data.get('conversation_id')
    
    if conversation_id:
        conversation = Conversation.query.get(conversation_id)
        if not conversation or conversation.user_id != current_user.id:
            return jsonify({'error': 'Conversation not found'}), 404
    else:
        conversation = Conversation(user_id=current_user.id)
        db.session.add(conversation)
        db.session.commit()
    
    user_message = Message(
        conversation_id=conversation.id,
        sender='user',
        text_content=text_content,
        image_path=file_path,
        audio_path=audio_path
    )
    db.session.add(user_message)
    conversation.last_updated = datetime.utcnow()
    db.session.commit()
    
    user_info = get_user_info()
    if file_path:
        abs_file_path = os.path.join(current_app.root_path, '..', file_path.lstrip('/'))
        response_text = llm_service.process_image_query(abs_file_path, text_content, user_info)
    else:
        response_text = llm_service.process_text_only(text_content, user_info)
    
    speech_filename = f"response_{int(time.time())}.mp3"
    speech_path = os.path.join(current_app.config['UPLOAD_FOLDER'], speech_filename)
    speech_service.text_to_speech(response_text, speech_path)
    
    doctor_message = Message(
        conversation_id=conversation.id,
        sender='doctor',
        text_content=response_text,
        audio_path=f"/static/uploads/{speech_filename}"
    )
    db.session.add(doctor_message)
    db.session.commit()
    
    return jsonify({
        'response': response_text,
        'audio': f"/static/uploads/{speech_filename}",
        'conversation_id': conversation.id
    })