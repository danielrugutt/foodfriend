from flask import Flask, redirect, render_template, request, make_response, session, abort, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from firebase_admin import credentials, firestore, auth
from datetime import timedelta
from dotenv import load_dotenv
from typing import List
from classes.DietaryPreference import DietaryPreference
from classes.Search import Search
from classes.SpoonacularRecipeAdapter import SpoonacularRecipeAdapter
from classes.Recipe import *
from classes.Exporter import *
from classes.Database import Database
import secrets
import os
import sys
import firebase_admin
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configure session cookie settings
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Adjust session expiration as needed
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Can be 'Strict', 'Lax', or 'None'

# Firebase Admin SDK setup
cred = credentials.Certificate("firebase-auth.json")
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()

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

""" AUTHENTICATION ROUTES """

# Add this to any request needing authentication
def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        
        else:
            return f(*args, **kwargs)
        
    return decorated_function


@app.route('/auth', methods=['POST'])
def authorize():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return "Unauthorized", 401

    token = token[7:]  # Strip off 'Bearer ' to get the actual token
    print(f"Received token: {token}")

    try:
        decoded_token = auth.verify_id_token(token, check_revoked=True, clock_skew_seconds=60) # Validate token here
        session['user'] = decoded_token # Add user to session
        return redirect(url_for('dashboard'))
    
    except:
        return "Unauthorized", 401


""" GUEST ROUTES """
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    #for testing between setting and searching
    global test_user
    search_query = None
    if request.method == 'GET':
         search_query = request.args.get('search_query') # For GET requests
    #read from seach bar, search bar is what directs to /search
    user_diet=test_user
    user_search=Search(user_diet)
    response=user_search.search(search_query)

    if 'results' in response:
        for recipe in response['results']:
            print(f"Recipe Name: {recipe["title"]} Recipe ID:{recipe["id"]}",file=sys.stderr)
    else:
        print("No results found!")

    return render_template("search_results.html", results=response,search_query=search_query)


@app.route('/settings', methods=['POST','GET'])
def settings():
    #TESTING ONLY
    global test_user
    user_preferences = { "excludedCuisines": test_user.exclude_cuisine,
                        "excludedIngredients": test_user.exclude_ingredients,
                        "maxSugar": test_user.max_sugar,
                        "intolerances": test_user.intolerances,
                        "diets": test_user.diets}
    if request.method=='POST':
        data=request.get_json()
        test_user=DietaryPreference(data['excludedCuisines'],data['excludedIngredients'],data['maxSugar'],data['intolerances'],data['diets'])
        print(data)
    return render_template("settings.html",preferences=user_preferences) 

 
@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    recipe = database.get_recipe(recipe_id)

    if recipe is None:
        recipe=SpoonacularRecipeAdapter(recipe_id)
        recipe=recipe.standardizeRecipe()
        #return "Recipe not found", 404

    return render_template("recipe.html", recipe=recipe)

@app.route('/recipe/<int:recipe_id>/export', methods=['GET'])
def export_recipe(recipe_id):
    recipe = database.get_recipe(recipe_id)
    if recipe is None:
        recipe=SpoonacularRecipeAdapter(recipe_id)
        recipe=recipe.standardizeRecipe()

    export_type = request.args.get('type')
    exporter = FactoryMethod.create_exporter(recipe, export_type)

    return exporter.exportRecipe()

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
def logout():
    session.pop('user', None)  # Remove the user from session
    response = make_response(redirect(url_for('login')))
    response.set_cookie('session', '', expires=0)  # Optionally clear the session cookie
    return response

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')


""" LOGGED IN USER ROUTES """
@app.route('/dashboard')
@auth_required
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=8080)
