from flask import Flask, redirect, render_template, request, session, abort, jsonify, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from firebase_admin import credentials, firestore
from datetime import datetime,timedelta, time
from dotenv import load_dotenv
from typing import List
from classes.DietaryPreference import DietaryPreference
from classes.SpoonacularConnection import SpoonacularConnection
from classes.SpoonacularRecipeAdapter import SpoonacularRecipeAdapter
from classes.Recipe import *
from classes.Database import Database
from models.UserModel import UserModel
from models.DietaryPreferenceModel import DietaryPreferenceModel
from models.IngredientModel import IngredientModel
from models.PlannedMeal import PlannedMeal
from models.RecipeIngredientModel import RecipeIngredientModel
from models.RecipeModel import RecipeModel
from models.RecipeListModel import RecipeListModel
from classes.RecipeService import RecipeService
from classes.SearchService import SearchService
from classes.AuthService import AuthService, auth_required
import secrets
import os
import sys
import firebase_admin
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Firebase Admin SDK initialization in AuthService
AuthService.init(app)
RecipeService.init(app)
SearchService.init(app)


# Configure session cookie settings
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Adjust session expiration as needed
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Can be 'Strict', 'Lax', or 'None'
CORS(app, supports_credentials=True) # Secure cross origin requests support


database = Database(app)
db = database.initialize_database()

#test user only
test_user=DietaryPreference(["greek"],["paprika"],["200"],["Peanut"],["vegetarian"] )


taratorRecipe = (
    RecipeBuilder("Tarator")
    .set_ingredients([RecipeIngredient("Cucumber", 1,), RecipeIngredient("Walnut", 0.25, "cup"), RecipeIngredient("Yogurt", 0.5, "tub")])
    .set_steps(["Make yogurt broth", "Cut cucumber", "Add walnuts, dill, and salt"])
    .set_cooking_time(15)
    .set_nutrition_info(Nutrition(600, 25, 75, 20))
    .set_servings(4)
    .set_cuisine("Bulgarian")
    .set_diet(["Vegetarian"])
    .set_intolerances(["Dairy"])
    .build()
)

database.insert_recipe(taratorRecipe)

##### TESTING SECTION ENDS HERE #####

def get_current_user():
    uid = session.get("uid")
    if not uid:
        return None
    return UserModel.query.filter_by(id=uid).first()

""" AUTHENTICATION ROUTES """
@app.route('/auth', methods=['POST'])
def auth_route():
    return AuthService.authorize()


""" GUEST ROUTES """
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    uid = session.get("uid")
    return SearchService.search(uid,request)
    

@app.route('/search-similar/<int:recipe_id>/<string:orig_recipe>', methods=['GET', 'POST'])
def search_similar(recipe_id,orig_recipe):
    return SearchService.search_similar(recipe_id,orig_recipe)
    

@app.route('/settings', methods=['POST','GET'])
def settings():
    #TESTING ONLY
    #global test_user
    uid = session.get("uid")
    #if needed saved the changes to dietary pref to DB either here or in the method which ever is easier
    return SearchService.settings(uid, request.method)

@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    return RecipeService.format_recipe_page(recipe_id, session)

@app.route('/recipe/<int:recipe_id>/export', methods=['GET'])
def export_recipe(recipe_id):
    export_type = request.args.get('type')
    return RecipeService.export_recipe(recipe_id, export_type)

@app.route('/login')
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')

@app.route('/signup')
def signup():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('signup.html')


@app.route('/reset-password')
def reset_password():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('forgot_password.html')

@app.route('/logout')
def logout_route():
    return AuthService.logout()

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')


""" LOGGED IN USER ROUTES """
@app.route('/dashboard')
@auth_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/add-meal', methods=["POST"])
@auth_required
def add_meal():
    data = request.get_json()

    title = data.get("title")
    start_time = data.get("startTime")  # e.g., "14:00"
    notes = data.get("notes")
    recipe_id = data.get("recipe_id")
    start_date = data.get("start")      # e.g., "2025-04-29"

    if not all([title, start_time, start_date]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        combined_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({"error": "Invalid date or time format"}), 400

    user_id = session.get("uid")
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    user = db.session.get(UserModel, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    recipe = db.session.get(RecipeModel, recipe_id) if recipe_id else None

    # Optional: check recipe is in user's recipe lists (if needed)
    if recipe:
        user_recipe_ids = {
            entry.recipe.id
            for rl in user.recipe_lists
            for entry in rl.recipes
        }
        if recipe.id not in user_recipe_ids:
            return jsonify({"error": "Recipe not in user's lists"}), 400

    new_meal = PlannedMeal(
        title=title,
        datetime=combined_datetime,
        notes=notes,
        user=user,
        recipe=recipe if recipe else None
    )

    db.session.add(new_meal)
    db.session.commit()

    return jsonify({"message": "Meal added successfully"}), 200


@app.route('/planned-meals')
@auth_required
def get_planned_meals():
    user = get_current_user()
    if not user:
        return jsonify([])

    meals = PlannedMeal.query.filter_by(user_id=user.id).all()

    events = []
    for meal in meals:
        start_dt = meal.datetime
        end_dt = start_dt + timedelta(hours=1)

        events.append({
            "title": f"{meal.title} ({meal.recipe.title})",
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat(),
            "extendedProps": {
                "recipe_id": meal.recipe.id,
                "notes": meal.notes or ""
            }
        })

    return jsonify(events)


@app.route('/all-recipes')
@auth_required
def get_all_recipes():
    test_user_id = session.get("uid")
    if not test_user_id:
        return redirect('/login')

    # Fetch all recipe lists for the user
    recipe_lists = RecipeListModel.query.filter_by(user_id=test_user_id).all()

    grouped_recipes = []
    for recipe_list in recipe_lists:
        # Get recipes for each list
        recipes = recipe_list.recipe_objects()
        grouped_recipes.append({
            'list_name': recipe_list.name,
            'recipes': [{'id': recipe.id, 'name': recipe.title} for recipe in recipes]
        })

    return jsonify(grouped_recipes)

@app.route('/recipe/<int:recipe_id>/bookmark/', methods=["POST"])
@auth_required
def save_to_list(recipe_id):
    return RecipeService.bookmark_recipe(recipe_id, session)

@app.route('/lists')
@auth_required
def lists():
    return RecipeService.get_lists(session)

@app.route('/profile')
@auth_required
def profile():
    return render_template('profile.html')

@app.route('/profile/email-change', methods=["POST"])
@auth_required
def change_email():
    uid = session.get("uid")
    new_user_email = request.form.get("emailChangeInput")
    return

@app.route('/delete-account', methods=['POST'])
@auth_required
def delete_account_route():
    return AuthService.delete_account()

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=8080)
