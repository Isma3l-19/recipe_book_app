from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user
from config import db
from models import Recipe

# Create Blueprint instead of creating a new app
routes_bp = Blueprint('routes', __name__)

# Route: Home Page (List Recipes)
@routes_bp.route('/')
def home():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template('index.html', recipes=recipes)

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
