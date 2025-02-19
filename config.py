import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Load environment variables
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "your_secret_key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()
login_manager = LoginManager()  # Initialize Flask-Login

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)  # Initialize login manager

    # Set login view (redirects unauthorized users)
    login_manager.login_view = "routes.login"

    # Import and register blueprints
    from routes import routes_bp
    app.register_blueprint(routes_bp)

    return app
