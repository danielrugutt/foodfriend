from flask import Flask, redirect, render_template, request, session, abort, jsonify, url_for
from flask_cors import CORS
from datetime import datetime,timedelta, time
from dotenv import load_dotenv
from classes.Recipe import *
from classes.Database import Database
from classes.RecipeService import RecipeService
from classes.SearchService import SearchService
from classes.CalendarService import CalendarService
from classes.AuthService import AuthService, auth_required
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Firebase Admin SDK initialization in AuthService
AuthService.init(app)
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

database = Database(app)
db = database.initialize_database()

""" AUTHENTICATION ROUTES """
@app.route('/auth', methods=['POST'])
def auth_route():
    return AuthService.authorize()

""" GUEST ROUTES """
@app.route('/')
@app.route('/login')
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    uid = session.get("uid")
    return SearchService.search(uid,request)

@app.route('/search-similar/<int:recipe_id>/<string:orig_recipe>', methods=['GET', 'POST'])
def search_similar(recipe_id,orig_recipe):
    return SearchService.search_similar(recipe_id,orig_recipe)

@app.route('/settings', methods=['POST','GET'])
def settings():
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
#
# def login():
#     if 'user' in session:
#         return redirect(url_for('dashboard'))
#     else:
#         return render_template('login.html')

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
    return CalendarService.add_meal(session)

@app.route('/update-meal', methods=['POST'])
@auth_required
def update_meal():
    return CalendarService.edit_meal()

@app.route('/delete-meal/<int:meal_id>', methods=['DELETE'])
@auth_required
def delete_meal(meal_id):
    return CalendarService.delete_meal(meal_id)

@app.route('/planned-meals')
@auth_required
def get_planned_meals():
    return CalendarService.get_planned_meals()

@app.route('/all-recipes')
@auth_required
def get_all_recipes():
    return CalendarService.get_all_recipes()

@app.route('/meal_recipe/<int:meal_id>')
@auth_required
def meal(meal_id):
    return CalendarService.format_meal_page(meal_id, session)

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
    return AuthService.change_email(session)

@app.route('/delete-account', methods=['POST'])
@auth_required
def delete_account_route():
    return AuthService.delete_account()

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=8080)
