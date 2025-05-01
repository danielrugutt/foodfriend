from abc import ABC, ABCMeta, abstractmethod
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.RecipeModel import RecipeModel
from models.IngredientModel import IngredientModel
from models.RecipeIngredientModel import RecipeIngredientModel
from models.RecipeListModel import RecipeListModel, RecipeListRecipeModel
from models.UserModel import UserModel
from models.PlannedMeal import PlannedMeal
from classes.Recipe import RecipeBuilder
from classes.DietaryPreference import DietaryPreference
from models.DietaryPreferenceModel import DietaryPreferenceModel
from db import db
import json
import os

class Singleton(ABCMeta):
    """ A metaclass for making Database a singleton. Inherits from ABCMeta so we can apply both the ABC and Singleton metaclass to the same object """
    _instances = {}

    def __call__(database_class, *args, **kwargs):
        if database_class not in database_class._instances:
            database_class._instances[database_class] = super(Singleton, database_class).__call__(*args, **kwargs)
        return database_class._instances[database_class]

class DatabaseInterface(ABC, metaclass=Singleton):
    @abstractmethod
    def initialize_database(self):
        pass

    @abstractmethod
    def insert_recipe(self, recipe_object):
        pass

    @abstractmethod
    def get_user_preferences(self, uid):
        pass

    @abstractmethod
    def get_recipe(self, recipe_id):
        pass

    @abstractmethod
    def get_user(self, user_id):
        pass

    @abstractmethod
    def set_user_preferences(self, uid, dietary_preference):
        pass

    @abstractmethod
    def get_ingredient(self, name, type):
        pass

    @abstractmethod
    def check_and_create_user(self, uid, email):
        pass

    @abstractmethod
    def get_default_list(self, uid):
        pass

    @abstractmethod
    def add_recipe_to_list(self, uid, recipe_id, list_id):
        pass

    @abstractmethod
    def create_named_list(self, uid, list_name):
        pass

    @abstractmethod
    def insert_planned_meal(self, planned_meal):
        pass


class Database(DatabaseInterface):
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
            from models.PlannedMeal import PlannedMeal
            db.create_all()

        return db

    def insert_recipe(self, recipe_object):
        """ Given a recipe object, inserts into the database """
        with self.app.app_context():

            # checking if recipe exists first!
            existing_recipe = db.session.get(RecipeModel, recipe_object.ID)
            if existing_recipe:
                return existing_recipe.id

            recipe_model = self.recipe_to_recipe_model(recipe_object)
            db.session.add(recipe_model)

            # add ingredients, creating as needed
            for ingredient in recipe_object.ingredients:
                found_ingredient = self.get_ingredient(ingredient.name)

                if found_ingredient is None:
                    found_ingredient = IngredientModel(name=ingredient.name.lower())
                    db.session.add(found_ingredient)

                recipe_ingredient_model = RecipeIngredientModel(
                    quantity=ingredient.quantity,
                    unit=ingredient.unit,
                    recipe=recipe_model,
                    ingredient=found_ingredient
                )

                db.session.add(recipe_ingredient_model)
                recipe_model.ingredients.append(recipe_ingredient_model)

            db.session.commit()

        return recipe_object.ID
    
    def get_user_preferences(self, uid):
        dietary_preference = DietaryPreferenceModel.query.filter_by(user_id=uid).first()
        if dietary_preference is None:
            dietary_preference = DietaryPreferenceModel(user_id=uid, exclude_cuisine="", exclude_ingredients="", max_sugar=999, intolerances="", diets="")
            db.session.add(dietary_preference)
            db.session.commit()
        #print("TESTING",dietary_preference.exclude_cuisine)
        exclude_cuisine = dietary_preference.exclude_cuisine.split(",") if dietary_preference.exclude_cuisine else []
        exclude_ingredients = dietary_preference.exclude_ingredients.split(",") if dietary_preference.exclude_ingredients else []
        max_sugar = dietary_preference.max_sugar
        intolerances = dietary_preference.intolerances.split(",") if dietary_preference.intolerances else []
        diets = dietary_preference.diets.split(",") if dietary_preference.diets else []

        return DietaryPreference(exclude_cuisine, exclude_ingredients, max_sugar, intolerances, diets)

    def set_user_preferences(self, uid, dietary_preference):
        """ Given a user ID and a dietary preference object, sets the preferences in the database """
        with self.app.app_context():
            dietary_preference_model = DietaryPreferenceModel.query.filter_by(user_id=uid).first()

            if dietary_preference_model is None:
                dietary_preference_model = DietaryPreferenceModel(user_id=uid)

            dietary_preference_model.exclude_cuisine = ",".join(dietary_preference.exclude_cuisine)
            dietary_preference_model.exclude_ingredients = ",".join(dietary_preference.exclude_ingredients)
            dietary_preference_model.max_sugar = dietary_preference.max_sugar
            dietary_preference_model.intolerances = ",".join(dietary_preference.intolerances)
            dietary_preference_model.diets = ",".join(dietary_preference.diets)

            db.session.add(dietary_preference_model)
            db.session.commit()

    def get_user(self, user_id):
        """ Gets a user model from the database """
        user = UserModel.query.get(user_id)
        return user

    def get_recipe(self, recipe_id):
        """ Grabs a recipe model from the database and converts it to a recipe object """
        recipe_model = RecipeModel.query.get(recipe_id)
        
        if recipe_model:
            return self.to_recipe_object(recipe_model)
        else:
            return None

    def get_ingredient(self, name, type="OTHER"):
        """ Checks to see if an ingredient exists, returning it if so. """
        name = name.lower()
        existing_ingredient = db.session.query(IngredientModel).filter_by(name=name).first()
        return existing_ingredient


    def recipe_to_recipe_model(self, recipe_object):
        """ Converts an object into a model. """

        recipe_model = RecipeModel(
            title=recipe_object.title,
            cooking_time=recipe_object.cooking_time,
            servings=recipe_object.servings,
            cuisine=recipe_object.cuisine,
            steps=recipe_object.steps,
            diet=recipe_object.diet,
            intolerances=recipe_object.intolerances,
            img_url=recipe_object.img_url
        )

        if recipe_object.ID:
            recipe_model.id = recipe_object.ID

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
            .set_img_url(recipe_model.img_url)
            .build()
        )

        return recipe


    def check_and_create_user(self, uid, email):
        """ Given a UID and email, checks if the user exists locally - makes them if no, setting up the bookmark list too! """
        with self.app.app_context():
            existing_user = UserModel.query.filter_by(id=uid).first()

            if not existing_user:
                user_model = UserModel(id=uid, email=email, name="")
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


    def create_named_list(self, uid, list_name):
        with self.app.app_context():
            new_list = RecipeListModel(name=list_name, user_id=uid)
            db.session.add(new_list)
            db.session.commit()
            return new_list.id
        
    def insert_planned_meal(self, planned_meal):
        """ Inserts a planned meal into the database """
        with self.app.app_context():
            merged_meal = db.session.merge(planned_meal)
            db.session.add(merged_meal)
            db.session.commit()

        return planned_meal
    
    def delete_planned_meal(self, planned_meal):
        """ Inserts a planned meal into the database """
        with self.app.app_context():
            merged_meal = db.session.merge(planned_meal)
            db.session.delete(merged_meal)
            db.session.commit()

        return planned_meal
    
    def commit(self):
        db.session.commit()
        return True




