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
from classes.CalendarService import CalendarService
import secrets
import os
import sys
import firebase_admin
import json
from auth_service import authorize, auth_required, delete_account, logout, init_auth_service, delete_account

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

RecipeService.init(app)
SearchService.init(app)
CalendarService.init(app)

# Configure session cookie settings
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Adjust session expiration as needed
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Can be 'Strict', 'Lax', or 'None'
CORS(app, supports_credentials=True) # Secure cross origin requests support

# Firebase Admin SDK setup
cred = credentials.Certificate("firebase-auth.json")
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()
database = Database(app)
init_auth_service(database)
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
    return authorize()


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
    return logout()

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
    return CalendarService.add_meal(session)

@app.route('/planned-meals')
@auth_required
def get_planned_meals():
    return CalendarService.get_planned_meals()


@app.route('/all-recipes')
@auth_required
def get_all_recipes():
    return CalendarService.get_all_recipes()

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
    return delete_account()

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=8080)
