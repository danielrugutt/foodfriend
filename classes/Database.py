from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.RecipeModel import RecipeModel
from models.IngredientModel import IngredientModel
from models.RecipeIngredientModel import RecipeIngredientModel
from models.RecipeListModel import RecipeListModel, RecipeListRecipeModel
from models.UserModel import UserModel
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
        os.makedirs("database", exist_ok=True)

        with self.app.app_context():
            from models.RecipeModel import RecipeModel
            from models.IngredientModel import IngredientModel
            from models.RecipeIngredientModel import RecipeIngredientModel
            from models.UserModel import UserModel
            from models.RecipeListModel import RecipeListModel, RecipeListRecipeModel
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

        # this probably has to use the recipe builder later...
        return Recipe(
            title=recipe_model.title,
            ingredients=ingredient_list,
            steps=recipe_model.get_steps(),
            cooking_time=recipe_model.cooking_time,
            nutrition_info=nutrition_info,
            servings=recipe_model.servings,
            cuisine=recipe_model.cuisine,
            diet=recipe_model.get_diet(),
            intolerances=recipe_model.get_intolerances(),
            ID=recipe_model.id,
            img_url=recipe_model
        )

    def check_and_create_user(self, uid, email):
        """ Given a UID and email, checks if the user exists locally - makes them if no """
        with self.app.app_context():
            existing_user = UserModel.query.filter_by(id=uid).first()

            if not existing_user:
                user = UserModel(id=uid, email=email)
                db.session.add(user)
                db.session.commit()





