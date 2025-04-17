from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.RecipeModel import RecipeModel
from models.IngredientModel import IngredientModel
from models.RecipeIngredientModel import RecipeIngredientModel
from models.RecipeListModel import RecipeListModel, RecipeListRecipeModel
from models.UserModel import UserModel
from classes.Recipe import RecipeBuilder
from db import db
import os

class Singleton(type):
    """ A metaclass for making Database a singleton"""
    _instances = {}

    def __call__(database_class, *args, **kwargs):
        if database_class not in database_class._instances:
            database_class._instances[database_class] = super(Singleton, database_class).__call__(*args, **kwargs)
        return database_class._instances[database_class]


class Database(metaclass=Singleton):
    def __init__(self, app):
        self.app = app
        base_dir = os.path.abspath(os.path.dirname(__file__))
        self.database_path = os.path.join(base_dir, "..", "database", "foodfriend.db")
        self.database_uri = "sqlite:///" + self.database_path
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.database_uri
        db.init_app(self.app)


    def initialize_database(self):
        """ Imports all tables and makes the database if it doesn't exist """
        os.makedirs("database", exist_ok=True)

        with self.app.app_context():
            from models.RecipeModel import RecipeModel
            from models.IngredientModel import IngredientModel
            from models.RecipeIngredientModel import RecipeIngredientModel
            from models.UserModel import UserModel
            from models.RecipeListModel import RecipeListModel, RecipeListRecipeModel
            from models.DietaryPreferenceModel import DietaryPreferenceModel
            db.create_all()

        return db

    def insert_recipe(self, recipe_object):
        """ Given a recipe object, inserts into the database """
        recipe_model = self.recipe_to_recipe_model(recipe_object)

        with self.app.app_context():
            db.session.add(recipe_model)
            db.session.commit()

        return recipe_object.ID

    def get_recipe(self, recipe_id):
        """ Grabs a recipe model from the database and converts it to a recipe object """
        recipe_model = RecipeModel.query.get(recipe_id)

        if recipe_model:
            return self.to_recipe_object(recipe_model)
        else:
            return None

    def get_ingredient(self, name, type="OTHER"):
        """ Checks to see if an ingredient exists - if not, makes it. """
        with self.app.app_context():
            existing_ingredient = db.session.query(IngredientModel).filter_by(name=name).first()

            if not existing_ingredient:
                ingredient_model = IngredientModel(name=name, type=type)
                db.session.add(ingredient_model)
                db.session.commit()
                return ingredient_model

        return existing_ingredient


    def recipe_to_recipe_model(self, recipe_object):
        """ Converts an object into a model. Will make ingredients as needed. """
        from models import IngredientModel

        recipe_model = RecipeModel(
            title=recipe_object.title,
            cooking_time=recipe_object.cooking_time,
            servings=recipe_object.servings,
            cuisine=recipe_object.cuisine,
            steps=recipe_object.steps,
            diet=recipe_object.diet,
            intolerances=recipe_object.intolerances
        )

        for ingredient in recipe_object.ingredients:
            found_ingredient = self.get_ingredient(ingredient.name)

            recipe_ingredient_model = RecipeIngredientModel(
                quantity=ingredient.quantity,
                unit=ingredient.unit,
                recipe=recipe_model,
                ingredient=found_ingredient
            )
            recipe_model.ingredients.append(recipe_ingredient_model)

        return recipe_model

    def to_recipe_object(self, recipe_model):
        """ Converts a model into an object. """
        from classes.Recipe import Recipe, RecipeIngredient, Nutrition

        ingredient_list = []
        for bridge in recipe_model.ingredients:
            ingredient = bridge.ingredient
            ingredient_list.append(
                RecipeIngredient(
                    name=ingredient.name,
                    quantity=bridge.quantity,
                    unit=bridge.unit
                )
            )

        nutrition_info = Nutrition(0, 0, 0, 0)  # placeholder, maybe attach later

        recipe = (
            RecipeBuilder(recipe_model.title)
            .set_ingredients(ingredient_list)
            .set_steps(recipe_model.get_steps())
            .set_cooking_time(recipe_model.cooking_time)
            .set_nutrition_info(nutrition_info)
            .set_servings(recipe_model.servings)
            .set_cuisine(recipe_model.cuisine)
            .set_diet(recipe_model.get_diet())
            .set_intolerances(recipe_model.get_intolerances())
            .set_ID(recipe_model.id)
            # .set_img_url(recipe_model)
            .build()
        )

        return recipe


    def check_and_create_user(self, uid, email):
        """ Given a UID and email, checks if the user exists locally - makes them if no, setting up the bookmark list too! """
        with self.app.app_context():
            existing_user = UserModel.query.filter_by(id=uid).first()

            if not existing_user:
                user_model = UserModel(id=uid, email=email)
                self.get_default_list(uid)
                db.session.add(user_model)
                db.session.commit()

    def get_default_list(self, uid):
        """ Returns the id of the default list, creating it if it doesn't exist. """
        with self.app.app_context():
            bookmark_list = RecipeListModel.query.filter_by(user_id=uid, name="Bookmarks").first()

            if bookmark_list is None:
                bookmark_list = RecipeListModel(name="Bookmarks", user_id=uid)
                db.session.add(bookmark_list)
                db.session.commit()
                print("added default bookmark list")
                print(bookmark_list.id)

            return bookmark_list.id


    def add_recipe_to_list(self, uid, recipe_id, list_id=None):
        with self.app.app_context():
            user_model = UserModel.query.filter_by(id=uid).first()
            recipe_model = RecipeModel.query.get(recipe_id)

            if list_id is None:
                self.get_default_list(uid)
                recipe_list = RecipeListModel.query.filter_by(user_id=uid, name="Bookmarks").first()
            else:
                recipe_list = RecipeListModel.query.filter_by(id=list_id, user_id=uid).first()

            if not recipe_list:
                print("No matching recipe list, could not add")
                return False

            # checks if the recipe and recipe list are already together - if no, uses the join table to add to the database
            existing_recipe_list_for_recipe = RecipeListRecipeModel.query.filter_by(recipe_id=recipe_id, recipe_list_id=recipe_list.id).first()

            if existing_recipe_list_for_recipe is None:
                join_model = RecipeListRecipeModel(
                    recipe_list=recipe_list,
                    recipe=recipe_model
                )
                db.session.add(join_model)
                db.session.commit()






