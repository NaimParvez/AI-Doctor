import os
import time
import logging
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app import db
from app.models import Conversation, Message
from app.utils.llm_local import llm_service
from app.utils.speech import speech_service

chat_bp = Blueprint('chat', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'webm', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_info(conversation_id=None):
    if not current_user.is_authenticated:
        logger.warning("Unauthenticated user attempted to fetch user info")
        return None

    user_info = {
        'username': current_user.username,
        'email': current_user.email,
        'age': current_user.age,
        'gender': current_user.gender,
        'medical_history': current_user.medical_history or "No medical history provided."
    }

    if conversation_id:
        conversation = Conversation.query.get(conversation_id)
        if conversation and conversation.user_id == current_user.id:
            messages = conversation.messages.order_by(Message.timestamp.asc()).limit(5).all()
            user_info['previous_conversation'] = [{
                'sender': m.sender,
                'text': m.text_content,
                'image_path': m.image_path,
                'timestamp': m.timestamp.isoformat()
            } for m in messages]
        else:
            user_info['previous_conversation'] = []
            logger.warning(f"Conversation {conversation_id} not found or unauthorized for user {current_user.username}")
    else:
        user_info['previous_conversation'] = []

    return user_info

@chat_bp.route('/')
@login_required
def chat_page():
    conversations = Conversation.query.filter_by(user_id=current_user.id).order_by(Conversation.start_time.asc()).all()

    if not conversations:
        conversation = Conversation(user_id=current_user.id)
        db.session.add(conversation)
        try:
            db.session.commit()
            logger.info(f"New conversation created for {current_user.username} (ID: {conversation.id})")

            message = Message(
                conversation_id=conversation.id,
                sender='user',
                text_content=f"Medical History: {current_user.medical_history or 'No medical history provided.'}"
            )
            db.session.add(message)
            db.session.commit()
            conversations = [conversation]
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error initializing conversation for {current_user.username}: {e}")
            return render_template('index.html', username=current_user.username, conversations=[], error="Conversation init failed.")

    return render_template('index.html', username=current_user.username, conversations=conversations)

@chat_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    file = request.files.get('file')
    if not file or file.filename == '':
        logger.warning(f"{current_user.username} submitted invalid file upload")
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        logger.warning(f"{current_user.username} attempted to upload unsupported file: {file.filename}")
        return jsonify({'error': 'File type not allowed'}), 400

    filename = secure_filename(f"{int(time.time())}_{file.filename}")
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, filename)
    relative_path = f"/static/uploads/{filename}"

    try:
        file.save(file_path)
        logger.info(f"{current_user.username} uploaded file: {relative_path}")

        if filename.lower().endswith(('.mp3', '.wav', '.webm')):
            try:
                transcription = speech_service.speech_to_text(file_path, language="en-US")
                if not transcription:
                    raise ValueError("Empty transcription")
                return jsonify({
                    'file_path': relative_path,
                    'transcription': transcription,
                    'file_type': 'audio',
                    'detected_language': 'en'
                })
            except Exception as e:
                logger.error(f"Audio transcription failed for {file_path}: {e}")
                return jsonify({'error': 'Failed to transcribe audio'}), 500

        file_type = 'pdf' if filename.endswith('.pdf') else 'image'
        return jsonify({'file_path': relative_path, 'file_type': file_type})

    except Exception as e:
        logger.error(f"Failed to save file from {current_user.username}: {e}")
        return jsonify({'error': 'File save error'}), 500

@chat_bp.route('/message', methods=['POST'])
@login_required
def send_message():
    data = request.json or {}
    text = data.get('text', '')
    image_path = data.get('image_path')
    audio_path = data.get('audio_path')
    conv_id = data.get('conversation_id')

    if not any([text, image_path, audio_path]):
        logger.warning(f"{current_user.username} submitted empty message")
        return jsonify({'error': 'Message or media required'}), 400

    conversation = None
    if conv_id:
        try:
            conv_id = int(conv_id)
            conversation = Conversation.query.get(conv_id)
            if not conversation or conversation.user_id != current_user.id:
                return jsonify({'error': 'Invalid conversation'}), 404
        except (TypeError, ValueError):
            return jsonify({'error': 'Invalid conversation ID'}), 400
    else:
        conversation = Conversation(user_id=current_user.id)
        db.session.add(conversation)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Conversation creation failed'}), 500

    user_msg = Message(
        conversation_id=conversation.id,
        sender='user',
        text_content=text,
        image_path=image_path,
        audio_path=audio_path
    )
    db.session.add(user_msg)
    conversation.last_updated = datetime.utcnow()

    user_info = get_user_info(conversation.id)
    if not user_info:
        return jsonify({'error': 'User info retrieval failed'}), 500

    try:
        if image_path:
            abs_path = os.path.join(current_app.root_path, '..', image_path.lstrip('/'))
            if not os.path.exists(abs_path):
                return jsonify({'error': 'Image file missing'}), 404
            response = llm_service.process_image_query(abs_path, text, user_info)
        else:
            response = llm_service.process_text_only(text, user_info)
    except Exception as e:
        logger.error(f"LLM failed for user {current_user.username}: {e}")
        return jsonify({'error': 'LLM processing failed'}), 500

    audio_filename = f"response_{int(time.time())}.mp3"
    audio_abs_path = os.path.join(current_app.config['UPLOAD_FOLDER'], audio_filename)
    audio_rel_path = f"/static/uploads/{audio_filename}"

    doctor_msg = Message(
        conversation_id=conversation.id,
        sender='doctor',
        text_content=response,
        audio_path=audio_rel_path
    )
    db.session.add(doctor_msg)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Database commit failed'}), 500

    try:
        speech_service.text_to_speech(response, audio_abs_path)
    except Exception as e:
        logger.warning(f"Speech generation failed: {e}")
        audio_rel_path = None

    return jsonify({
        'response': response,
        'audio': audio_rel_path,
        'conversation_id': conversation.id
    })
