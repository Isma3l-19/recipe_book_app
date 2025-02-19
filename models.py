from config import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)  # Renamed for clarity
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to Recipes (cascade delete if user is deleted)
    recipes = db.relationship('Recipe', back_populates='user', lazy=True, cascade="all, delete")

    # Set hashed password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check password against hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Convert user object to dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)

    # Foreign key linking to User model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    # Relationship to User
    user = db.relationship('User', back_populates='recipes')

    # Convert recipe object to dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'image_url': self.image_url,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'likes': self.likes,
            'user': self.user.to_dict() if self.user else None  # Embed user details
        }
