import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Conversation, Message
from app import db
import logging

auth_bp = Blueprint('auth', __name__)

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logger.info(f"User {current_user.username} is already authenticated, redirecting to chat page")
        return redirect(url_for('chat.chat_page'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        logger.info(f"Login attempt with username: {username}")

        user = User.query.filter_by(username=username).first()
        
        if user:
            logger.info(f"User found with username: {username}, ID: {user.id}")
            if user.check_password(password):
                logger.info(f"Password matches for user {user.username}")
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                logger.info(f"User {user.username} logged in successfully, redirecting to chat page")
                return redirect(url_for('chat.chat_page'))
            else:
                logger.warning(f"Password does not match for user with username: {username}")
                flash('Invalid username or password', 'error')
        else:
            logger.warning(f"No user found with username: {username}")
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        logger.info(f"User {current_user.username} is already authenticated, redirecting to chat page")
        return redirect(url_for('chat.chat_page'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        date_of_birth = request.form.get('date_of_birth')
        gender = request.form.get('gender')
        medical_history = request.form.get('medical_history')

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            logger.warning(f"Registration failed: Username {username} already exists")
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            logger.warning(f"Registration failed: Email {email} already exists")
            return render_template('register.html')
        
        user = User(
            username=username,
            email=email,
            date_of_birth=datetime.strptime(date_of_birth, '%Y-%m-%d') if date_of_birth else None,
            gender=gender,
            medical_history=medical_history
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user, remember=True)
        flash('Account created successfully!', category='success')
        logger.info(f"User {username} registered and logged in successfully")
        return redirect(url_for('chat.chat_page'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logger.info(f"User {current_user.username} logging out")
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@auth_bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    date_of_birth = request.form.get('date_of_birth')
    gender = request.form.get('gender')
    medical_history = request.form.get('medical_history')

    # Check if the new username or email is already taken by another user
    user_by_username = User.query.filter(User.username == username, User.id != current_user.id).first()
    user_by_email = User.query.filter(User.email == email, User.id != current_user.id).first()

    if user_by_username:
        flash('Username already exists', 'error')
        logger.warning(f"Profile update failed for user {current_user.username}: Username {username} already exists")
        return redirect(url_for('auth.profile'))
    
    if user_by_email:
        flash('Email already exists', 'error')
        logger.warning(f"Profile update failed for user {current_user.username}: Email {email} already exists")
        return redirect(url_for('auth.profile'))

    # Validate password if provided
    if password and len(password) < 6:
        flash('Password must be at least 6 characters', 'error')
        logger.warning(f"Profile update failed for user {current_user.username}: Password too short")
        return redirect(url_for('auth.profile'))

    # Update user details
    current_user.username = username
    current_user.email = email
    if password:
        current_user.set_password(password)
        logger.info(f"User {current_user.username} updated their password")
    current_user.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d') if date_of_birth else None
    current_user.gender = gender if gender else None
    current_user.medical_history = medical_history if medical_history else None

    db.session.commit()
    flash('Profile updated successfully!', category='success')
    logger.info(f"User {current_user.username} updated their profile successfully")
    return redirect(url_for('auth.profile'))

@auth_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    logger.info(f"User {current_user.username} is deleting their account")
    
    # Delete associated files (images and audio)
    conversations = Conversation.query.filter_by(user_id=current_user.id).all()
    for conversation in conversations:
        for message in conversation.messages:
            if message.image_path and os.path.exists(os.path.join('app', 'static', message.image_path.lstrip('/'))):
                os.remove(os.path.join('app', 'static', message.image_path.lstrip('/')))
                logger.info(f"Deleted image file: {message.image_path}")
            if message.audio_path and os.path.exists(os.path.join('app', 'static', message.audio_path.lstrip('/'))):
                os.remove(os.path.join('app', 'static', message.audio_path.lstrip('/')))
                logger.info(f"Deleted audio file: {message.audio_path}")

    # Delete the user (conversations and messages will be deleted automatically due to CASCADE)
    user = User.query.get(current_user.id)
    db.session.delete(user)
    db.session.commit()
    
    logout_user()
    flash('Your account has been deleted successfully.', category='success')
    logger.info(f"User {user.username} deleted their account successfully")
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        logger.info(f"User {current_user.username} is already authenticated, redirecting to chat page")
        return redirect(url_for('chat.chat_page'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        logger.info(f"Forgot password attempt for username: {username}, email: {email}")

        user = User.query.filter_by(username=username, email=email).first()
        
        if user:
            if len(new_password) < 6:
                flash('Password must be at least 6 characters', 'error')
                logger.warning(f"Forgot password failed for user {username}: Password too short")
                return redirect(url_for('auth.forgot_password'))
            
            user.set_password(new_password)
            db.session.commit()
            flash('Password reset successfully! Please log in with your new password.', category='success')
            logger.info(f"User {username} reset their password successfully")
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid username or email', 'error')
            logger.warning(f"Forgot password failed: No user found with username {username} and email {email}")
            return redirect(url_for('auth.forgot_password'))
    
    return render_template('forgot_password.html')