from flask import render_template, request, redirect, url_for, jsonify
from config import app, db
from models import Recipe

# Route: Home Page (List Recipes)
@app.route('/')
def home():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template('index.html', recipes=recipes)

# Route: Add a New Recipe
@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        image_url = request.form.get('image_url')
        
        new_recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, image_url=image_url)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_recipe.html')

# Route: Get Trending Recipes (Most Liked)
@app.route('/trending')
def trending():
    trending_recipes = Recipe.query.order_by(Recipe.likes.desc()).limit(5).all()
    return jsonify([recipe.to_dict() for recipe in trending_recipes])
