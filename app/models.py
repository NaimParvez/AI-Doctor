from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    medical_history = db.Column(db.Text, default='[]')  # Store as JSON string
    conversations = db.relationship('Conversation', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def age(self):
        if self.date_of_birth:
            today = datetime.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    def get_medical_history(self):
        try:
            return json.loads(self.medical_history)
        except json.JSONDecodeError:
            return []
    
    def set_medical_history(self, history_list):
        self.medical_history = json.dumps(history_list)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    messages = db.relationship('Message', backref='conversation', lazy='dynamic', cascade='all, delete-orphan', order_by='Message.timestamp.asc()')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'start_time': self.start_time.isoformat(),
            'last_updated': self.last_updated.isoformat(),
            'messages': [message.to_dict() for message in self.messages]
        }

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    sender = db.Column(db.String(20), nullable=False)  # 'user' or 'doctor'
    text_content = db.Column(db.Text)
    image_path = db.Column(db.String(255))
    audio_path = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'text_content': self.text_content,
            'image_path': self.image_path,
            'audio_path': self.audio_path,
            'timestamp': self.timestamp.isoformat()
        }

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))