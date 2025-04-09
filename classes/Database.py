from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.RecipeModel import RecipeModel
from models.RecipeIngredientModel import RecipeIngredientModel
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
            from models.RecipeIngredientModel import RecipeIngredientModel
            db.create_all()

        return db

    def insert_recipe(self, recipe_object):
        """ Given a recipe object, inserts into the database """
        recipe_model = RecipeModel.recipe_to_recipe_model(recipe_object)

        for ingredient in recipe_object.ingredients:
            ingredient_model = RecipeIngredientModel(
            name=ingredient.name,
            quantity=ingredient.quantity,
            unit=ingredient.unit,
            recipe=recipe_model
        )

        with self.app.app_context():
            db.session.add(recipe_model)
            db.session.commit()
        return recipe_object.ID

    def get_recipe(self, recipe_id):
        """ Grabs a recipe model from the database and converts it to a recipe object """
        recipe_model = RecipeModel.query.get(recipe_id)
        return recipe_model.to_recipe_object() if recipe_model else None


