from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat.chat_page'))
    
    if request.method == 'POST':
        from app import db
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('chat.chat_page'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat.chat_page'))
    
    if request.method == 'POST':
        from app import db
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        date_of_birth = request.form.get('date_of_birth')
        gender = request.form.get('gender')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('register.html')
        
        from datetime import datetime
        user = User(
            username=username,
            email=email,
            date_of_birth=datetime.strptime(date_of_birth, '%Y-%m-%d') if date_of_birth else None,
            gender=gender
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('chat.chat_page'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)