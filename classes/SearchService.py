from flask import Flask, render_template, request
from classes.DietaryPreference import DietaryPreference
from classes.SpoonacularConnection import SpoonacularConnection
from classes.Recipe import *
from classes.Database import Database
import sys


class SearchService:
    database = None

    @classmethod
    def init(cls, app):
        """ Initializes the database and makes it a class variable. Must be initialized before using in app.py """
        cls.database = Database(app)
        cls.database.initialize_database()

    @staticmethod
    def search(user, request):
        user_diet=SearchService.database.get_user_preferences(user)
        search_query = None
        if request.method == 'GET':
            search_query = request.args.get('search_query') # For GET requests
        #read from seach bar, search bar is what directs to /search
        user_search=SpoonacularConnection()
        response=user_search.getSearchResults(search_query,user_diet)

        if 'results' in response:
            for recipe in response['results']:
                print(f"Recipe Name: {recipe["title"]} Recipe ID:{recipe["id"]}",file=sys.stderr)
        else:
            print("No results found!")
        
        return render_template("search_results.html", results=response,search_query=search_query)
    

    @staticmethod
    def search_similar(recipe_id,orig_recipe):
        user_search=SpoonacularConnection()
        response=user_search.getSimilarResults(recipe_id)
        return render_template("similar_results.html", results=response,search_query=orig_recipe)

    @staticmethod
    def settings(user, request_method):
        if request_method=='POST':
            data=request.get_json()
            user_preferences=DietaryPreference(data['excludedCuisines'],data['excludedIngredients'],data['maxSugar'],data['intolerances'],data['diets'])
            SearchService.database.set_user_preferences(user, user_preferences)

        user_preferences=SearchService.database.get_user_preferences(user)

        shown_prefs = { "excludedCuisines": user_preferences.exclude_cuisine,
                    "excludedIngredients": user_preferences.exclude_ingredients,
                    "maxSugar": user_preferences.max_sugar,
                    "intolerances": user_preferences.intolerances,
                    "diets": user_preferences.diets}
        return render_template("settings.html",preferences=shown_prefs)