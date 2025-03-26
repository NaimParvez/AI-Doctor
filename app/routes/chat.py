import os
import time
import threading
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Conversation, Message
from app.utils.llm_local import llm_service
from app.utils.speech import speech_service
import logging

chat_bp = Blueprint('chat', __name__)

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'webm', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_info(conversation_id=None):
    if not current_user.is_authenticated:
        logger.warning("Attempt to get user info for unauthenticated user")
        return None
    user_info = {
        'username': current_user.username,
        'email': current_user.email
    }
    if current_user.age:
        user_info['age'] = current_user.age
    if current_user.gender:
        user_info['gender'] = current_user.gender
    if current_user.medical_history:
        user_info['medical_history'] = current_user.medical_history
    else:
        user_info['medical_history'] = "No medical history provided."

    # Fetch previous conversation messages if a conversation_id is provided
    if conversation_id:
        conversation = Conversation.query.get(conversation_id)
        if conversation and conversation.user_id == current_user.id:
            # Fetch only the last 5 messages to improve performance
            messages = conversation.messages.order_by(Message.timestamp.asc()).limit(5).all()
            user_info['previous_conversation'] = [
                {
                    'sender': message.sender,
                    'text': message.text_content,
                    'image_path': message.image_path,
                    'timestamp': message.timestamp.isoformat()
                }
                for message in messages
            ]
        else:
            user_info['previous_conversation'] = []
            logger.warning(f"Conversation {conversation_id} not found or does not belong to user {current_user.username}")
    else:
        user_info['previous_conversation'] = []

    return user_info

@chat_bp.route('/')
@login_required
def chat_page():
    conversations = Conversation.query.filter_by(user_id=current_user.id).order_by(Conversation.start_time.asc()).all()
    # If no conversations exist, create one and add the user's medical history as the first message
    if not conversations:
        conversation = Conversation(user_id=current_user.id)
        db.session.add(conversation)
        try:
            db.session.commit()
            logger.info(f"Created new conversation for user {current_user.username}, ID: {conversation.id}")
            # Add medical history as the first message if it exists
            medical_history = current_user.medical_history if current_user.medical_history else "No medical history provided."
            medical_history_message = Message(
                conversation_id=conversation.id,
                sender='user',
                text_content=f"Medical History: {medical_history}"
            )
            db.session.add(medical_history_message)
            db.session.commit()
            conversations = [conversation]
            logger.info(f"Added medical history message to conversation {conversation.id} for user {current_user.username}")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to create conversation for user {current_user.username}: {str(e)}")
            return render_template('index.html', username=current_user.username, conversations=[], error="Failed to initialize conversation")
    return render_template('index.html', username=current_user.username, conversations=conversations)

@chat_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        logger.warning(f"User {current_user.username} attempted to upload a file with no file part")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        logger.warning(f"User {current_user.username} attempted to upload a file with no filename")
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{int(time.time())}_{file.filename}")
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        try:
            file.save(file_path)
            relative_path = f"/static/uploads/{filename}"
            logger.info(f"User {current_user.username} uploaded file: {relative_path}")
            
            if filename.lower().endswith(('.mp3', '.wav', '.webm')):
                try:
                    transcription = speech_service.speech_to_text(file_path, language="en-US")
                    if not transcription:
                        logger.warning(f"Transcription failed for audio file: {file_path}")
                        return jsonify({'error': 'Failed to transcribe audio'}), 500
                    return jsonify({
                        'file_path': relative_path,
                        'transcription': transcription,
                        'file_type': 'audio',
                        'detected_language': 'en'
                    })
                except Exception as e:
                    logger.error(f"Transcription failed for audio file {file_path}: {str(e)}")
                    return jsonify({'error': 'Failed to transcribe audio'}), 500
            elif filename.lower().endswith('.pdf'):
                return jsonify({'file_path': relative_path, 'file_type': 'pdf'})
            else:
                return jsonify({'file_path': relative_path, 'file_type': 'image'})
        except Exception as e:
            logger.error(f"Failed to save uploaded file for user {current_user.username}: {str(e)}")
            return jsonify({'error': 'Failed to save file'}), 500
    
    logger.warning(f"User {current_user.username} attempted to upload an invalid file type: {file.filename}")
    return jsonify({'error': 'File type not allowed'}), 400

@chat_bp.route('/message', methods=['POST'])
@login_required
def send_message():
    data = request.json
    if not data:
        logger.warning(f"User {current_user.username} sent an empty message request")
        return jsonify({'error': 'No data provided'}), 400

    text_content = data.get('text', '')
    file_path = data.get('image_path')
    audio_path = data.get('audio_path')
    conversation_id = data.get('conversation_id')

    # Validate input: at least one of text, image, or audio must be provided
    if not text_content and not file_path and not audio_path:
        logger.warning(f"User {current_user.username} attempted to send an empty message")
        return jsonify({'error': 'Message, image, or audio is required'}), 400

    # Validate conversation_id if provided
    if conversation_id:
        try:
            conversation_id = int(conversation_id)
            conversation = Conversation.query.get(conversation_id)
            if not conversation or conversation.user_id != current_user.id:
                logger.warning(f"User {current_user.username} attempted to access invalid conversation ID: {conversation_id}")
                return jsonify({'error': 'Conversation not found'}), 404
        except (ValueError, TypeError):
            logger.warning(f"User {current_user.username} provided invalid conversation ID: {conversation_id}")
            return jsonify({'error': 'Invalid conversation ID'}), 400
    else:
        conversation = Conversation(user_id=current_user.id)
        db.session.add(conversation)
        try:
            db.session.commit()  # Commit the conversation to assign an ID
            logger.info(f"Created new conversation for user {current_user.username}, ID: {conversation.id}")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to create conversation for user {current_user.username}: {str(e)}")
            return jsonify({'error': 'Failed to create conversation'}), 500

    # Create user message
    user_message = Message(
        conversation_id=conversation.id,
        sender='user',
        text_content=text_content,
        image_path=file_path,
        audio_path=audio_path
    )
    db.session.add(user_message)
    conversation.last_updated = datetime.utcnow()

    # Pass the conversation_id to get_user_info to fetch previous messages
    user_info = get_user_info(conversation_id=conversation.id)
    if not user_info:
        logger.error(f"Failed to get user info for user {current_user.username}")
        return jsonify({'error': 'Failed to retrieve user information'}), 500

    # Process the message with the LLM
    try:
        if file_path:
            abs_file_path = os.path.join(current_app.root_path, '..', file_path.lstrip('/'))
            if not os.path.exists(abs_file_path):
                logger.warning(f"Image file not found for user {current_user.username}: {abs_file_path}")
                return jsonify({'error': 'Image file not found'}), 404
            response_text = llm_service.process_image_query(abs_file_path, text_content, user_info)
        else:
            response_text = llm_service.process_text_only(text_content, user_info)
    except Exception as e:
        logger.error(f"Error processing message for user {current_user.username}: {str(e)}")
        return jsonify({'error': 'Failed to process message with LLM'}), 500

    # Create doctor message
    speech_filename = f"response_{int(time.time())}.mp3"
    speech_path = os.path.join(current_app.config['UPLOAD_FOLDER'], speech_filename)
    speech_relative_path = f"/static/uploads/{speech_filename}"
    
    doctor_message = Message(
        conversation_id=conversation.id,
        sender='doctor',
        text_content=response_text,
        audio_path=speech_relative_path
    )
    db.session.add(doctor_message)

    # Commit all database changes
    try:
        db.session.commit()
        logger.info(f"Messages saved for user {current_user.username} in conversation {conversation.id}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to save messages for user {current_user.username}: {str(e)}")
        return jsonify({'error': 'Failed to save message'}), 500

    # Generate speech synchronously
    try:
        speech_service.text_to_speech(response_text, speech_path)
        logger.info(f"Generated speech for response in conversation {conversation.id}")
    except Exception as e:
        logger.error(f"Failed to generate speech for conversation {conversation.id}: {str(e)}")
        # Set audio path to None if speech generation fails
        speech_relative_path = None

    return jsonify({
        'response': response_text,
        'audio': speech_relative_path,
        'conversation_id': conversation.id
    })