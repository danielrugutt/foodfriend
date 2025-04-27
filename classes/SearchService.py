from flask import Flask, render_template, request
from classes.DietaryPreference import DietaryPreference
from classes.SpoonacularConnection import SpoonacularConnection
from classes.Recipe import *
import sys


class SearchService:
        
    @staticmethod
    def search(user, request):
        search_query = None
        if request.method == 'GET':
            search_query = request.args.get('search_query') # For GET requests
        #read from seach bar, search bar is what directs to /search
        user_diet=user
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
        user_preferences = { "excludedCuisines": user.exclude_cuisine,
                            "excludedIngredients": user.exclude_ingredients,
                            "maxSugar": user.max_sugar,
                            "intolerances": user.intolerances,
                            "diets": user.diets}
        if request_method=='POST':
            data=request.get_json()
            new_pref=DietaryPreference(data['excludedCuisines'],data['excludedIngredients'],data['maxSugar'],data['intolerances'],data['diets'])
            user.update_preferences(new_pref)

        return render_template("settings.html",preferences=user_preferences)