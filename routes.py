from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user, login_manager
from config import db, login_manager
from models import Recipe, User
from werkzeug.security import check_password_hash

# Create Blueprint instead of creating a new app
routes_bp = Blueprint('routes', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route: Home Page (List Recipes)
@routes_bp.route('/')
def home():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template('index.html', recipes=recipes)

# Route: Sign Up to application
@routes_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('routes.signup'))
        
        new_user = User(email=email, username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('routes.home'))
    
    return render_template('signup.html')

# Route: Login to application
@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('routes.home'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html')

# Route: Logout from application
@routes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.home'))

# Route: Add a New Recipe
@routes_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        image_url = request.form.get('image_url')
        
        new_recipe = Recipe(
            title=title, 
            ingredients=ingredients, 
            instructions=instructions, 
            image_url=image_url,
            user_id=current_user.id  # Associate the recipe with the current user
        )
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('routes.home'))  # Use 'routes.home' because it's a blueprint
    return render_template('add_recipe.html')

# Route: Delete a Recipe
@routes_bp.route('/delete/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash('You do not have permission to delete this recipe.')
        return redirect(url_for('routes.home'))
    
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('routes.home'))

# Route: Get Trending Recipes (Most Viewed and Liked)
@routes_bp.route('/trending')
def trending():
    trending_recipes = Recipe.query.order_by(Recipe.views.desc(), Recipe.likes.desc()).limit(5).all()
    return render_template('trending.html', recipes=trending_recipes)
