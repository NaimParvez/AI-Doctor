import os
from flask import Blueprint, render_template, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Conversation, Message

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('chat.chat_page'))
    return redirect(url_for('auth.login'))

@main_bp.route('/history')
@login_required
def history():
    conversations = Conversation.query.filter_by(user_id=current_user.id).order_by(Conversation.start_time.asc()).all()
    return render_template('history.html', conversations=conversations)

@main_bp.route('/delete_conversation/<int:conversation_id>', methods=['DELETE'])
@login_required
def delete_conversation(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    if conversation.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    # Delete associated files
    for message in conversation.messages:
        if message.image_path and os.path.exists(os.path.join('static', message.image_path.lstrip('/'))):
            os.remove(os.path.join('static', message.image_path.lstrip('/')))
        if message.audio_path and os.path.exists(os.path.join('static', message.audio_path.lstrip('/'))):
            os.remove(os.path.join('static', message.audio_path.lstrip('/')))

    # Delete the conversation (cascades to messages due to cascade='all, delete-orphan')
    db.session.delete(conversation)
    db.session.commit()
    return jsonify({'message': 'Conversation deleted successfully'})