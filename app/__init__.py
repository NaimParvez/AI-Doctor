from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Register blueprints after extensions are initialized
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.chat import chat_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    
    return app