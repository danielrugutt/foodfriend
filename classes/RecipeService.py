from flask import Flask, redirect, render_template, request, make_response, session, abort, jsonify, url_for
from models.RecipeListModel import RecipeListModel
from classes.SpoonacularConnection import SpoonacularConnection
from classes.Database import Database
from classes.Exporter import *

class RecipeService:
    database = None

    @classmethod
    def init(cls, app):
        """ Initializes the database and makes it a class variable. Must be initialized before using in app.py """
        cls.database = Database(app)
        cls.database.initialize_database()

    @staticmethod
    def get_recipe_from_database(recipe_id):
        """ Grabs the recipe from the database or from Spoonacular. Used in multiple other methods """
        recipe = RecipeService.database.get_recipe(recipe_id)

        if recipe is None:
            spoon = SpoonacularConnection()
            recipe = spoon.getRecipe(recipe_id)
            RecipeService.database.insert_recipe(recipe)

        return recipe

    @staticmethod
    def format_recipe_page(recipe_id, session):
        """ Returns the recipe page given an ID, including lists if logged in """
        recipe = RecipeService.get_recipe_from_database(recipe_id)

        if recipe is None:
            return "Recipe not found", 404

        uid = session.get("uid")
        user_lists = []

        if uid:
            user_lists = RecipeListModel.query.filter_by(user_id=uid).all()

        return render_template("recipe.html", recipe=recipe, user_lists=user_lists, uid=uid)

    @staticmethod
    def export_recipe(recipe_id):
        """ Exports the given recipe in either an email or PDF format """
        recipe = RecipeService.get_recipe_from_database(recipe_id)

        if recipe is None:
            return "Recipe not found", 404

        export_type = request.args.get('type')
        exporter = FactoryMethod.create_exporter(recipe, export_type)

        return exporter.exportRecipe()

    @staticmethod
    def bookmark_recipe(recipe_id, session):
        """ Bookmarks the recipe to whatever list the user chooses on the template page """
        uid = session.get("uid")
        list_id = request.form.get("list_id")
        new_list_name = request.form.get("new_list_name")

        recipe = RecipeService.get_recipe_from_database(recipe_id)
        if recipe is None:
            return "Recipe not found", 404

        if list_id == "new" and new_list_name:
            list_id = RecipeService.database.create_named_list(uid, new_list_name)

        RecipeService.database.add_recipe_to_list(uid, recipe_id, list_id)
        return f"Saved recipe {recipe_id} to list {list_id}"

    @staticmethod
    def get_lists(session):
        """ Gets all lists the user has and displays them """
        uid = session.get("uid")
        user_lists = RecipeListModel.query.filter_by(user_id=uid).all()
        return render_template("lists.html", lists=user_lists)
