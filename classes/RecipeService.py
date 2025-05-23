from flask import Flask, redirect, render_template, request, make_response, session, abort, jsonify, url_for, flash
from models.RecipeListModel import RecipeListModel
from classes.SpoonacularConnection import SpoonacularConnection
from classes.Database import Database
from classes.Exporter import *
from classes.Recipe import RecipeBuilder, Recipe, RecipeIngredient

class RecipeService:
    database = None

    @classmethod
    def init(cls, app):
        """ Initializes the database and makes it a class variable. Must be initialized before using in app.py """
        cls.database = Database(app)
        cls.database.initialize_database()

        # inserting a single local recipe
        # spoonacular has an API limit, so this just makes sure we have something to look at if we hit that limit
        taratorRecipe = (
            RecipeBuilder("Tarator")
            .set_ingredients([RecipeIngredient("Cucumber", 1,), RecipeIngredient("Walnut", 0.25, "cup"), RecipeIngredient("Yogurt", 0.5, "tub")])
            .set_steps(["Make yogurt broth", "Cut cucumber", "Add walnuts, dill, and salt"])
            .set_cooking_time(15)
            .set_servings(4)
            .set_cuisine("Bulgarian")
            .set_diet(["Vegetarian"])
            .set_intolerances(["Dairy"])
            .build()
        )
        cls.database.insert_recipe(taratorRecipe)

    @staticmethod
    def get_recipe_from_database(recipe_id):
        """ Grabs the recipe from the database or from Spoonacular, if not found within local database """
        recipe = RecipeService.database.get_recipe(recipe_id)
        if recipe:
            return recipe

        recipe = SpoonacularConnection().getRecipe(recipe_id)
        if recipe:
            RecipeService.database.insert_recipe(recipe)

        return recipe

    @staticmethod
    def format_recipe_page(recipe_id, session):
        """ Returns the recipe page given an ID, including lists if logged in """
        recipe = RecipeService.get_recipe_from_database(recipe_id)

        if recipe is None:
            return "Recipe not found.", 404

        uid = session.get("uid")
        user_lists = []

        if uid:
            user_lists = RecipeListModel.query.filter_by(user_id=uid).all()

        return render_template("recipe.html", recipe=recipe, user_lists=user_lists, uid=uid)

    @staticmethod
    def export_recipe(recipe_id, export_type):
        """ Exports the given recipe in either an email or PDF format """
        recipe = RecipeService.get_recipe_from_database(recipe_id)

        if recipe is None:
            return "Recipe not found", 404

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
        list_name = RecipeListModel.query.filter_by(id=list_id).first().name
        flash("Recipe saved successfully to " + list_name + "!") # going to be shown in the flask template
        return redirect(url_for("recipe", recipe_id=recipe_id))

    @staticmethod
    def get_lists(session):
        """ Gets all lists the user has and displays them """
        uid = session.get("uid")
        user_lists = RecipeListModel.query.filter_by(user_id=uid).all()
        return render_template("lists.html", lists=user_lists)
