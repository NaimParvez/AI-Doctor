import os
from flask import Blueprint, render_template, jsonify, redirect, url_for, current_app
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
    conversations = (
        Conversation.query
        .filter_by(user_id=current_user.id)
        .order_by(Conversation.start_time.asc())
        .all()
    )
    return render_template('history.html', conversations=conversations)

@main_bp.route('/delete_conversation/<int:conversation_id>', methods=['DELETE'])
@login_required
def delete_conversation(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)

    if conversation.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']

        # Delete associated media files (image and audio)
        for message in conversation.messages:
            for file_attr in ['image_path', 'audio_path']:
                file_path = getattr(message, file_attr)
                if file_path:
                    absolute_path = os.path.join(upload_folder, os.path.basename(file_path))
                    if os.path.exists(absolute_path):
                        os.remove(absolute_path)

        # Delete the conversation and its messages
        db.session.delete(conversation)
        db.session.commit()
        return jsonify({'message': 'Conversation deleted successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete conversation: {str(e)}'}), 500
