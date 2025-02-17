from flask import Blueprint, render_template, request, redirect, url_for, jsonify
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
def add_recipe():
    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        image_url = request.form.get('image_url')
        
        new_recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, image_url=image_url)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('routes.home'))  # Use 'routes.home' because it's a blueprint
    return render_template('add_recipe.html')

# Route: Get Trending Recipes (Most Liked)
@routes_bp.route('/trending')
def trending():
    trending_recipes = Recipe.query.order_by(Recipe.likes.desc()).limit(5).all()
    return jsonify([recipe.to_dict() for recipe in trending_recipes])
