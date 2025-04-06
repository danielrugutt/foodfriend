import sqlite3
import json
import os
from .Recipe import Recipe, RecipeBuilder, RecipeIngredient


class Singleton(type):
    """ A metaclass for making Database a singleton"""
    _instances = {}

    def __call__(database_class, *args, **kwargs):
        if database_class not in database_class._instances:
            database_class._instances[database_class] = super(Singleton, database_class).__call__(*args, **kwargs)
        return database_class._instances[database_class]

class Database(metaclass=Singleton):
    def __init__(self):
        self.database_path = "database/foodfriend.db"
        self.database_schema = "database/testing.sql"

    def initialize_database(self):
        if not os.path.exists(self.database_path):
            print("Database does not exist, creating!");
            connection = sqlite3.connect(self.database_path)
            databaseFile = open(self.database_schema, "r")
            connection.executescript(databaseFile.read())
            databaseFile.close()

    def insert_recipe(self, recipe):
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO Recipe (title, cooking_time, servings, cuisine, steps, diet, intolerances)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                recipe.title,
                recipe.cooking_time,
                recipe.servings,
                recipe.cuisine,
                json.dumps(recipe.steps),
                json.dumps(recipe.diet),
                json.dumps(recipe.intolerances),
            ))

            new_recipe_id = cursor.lastrowid

            # note that this currently does not connect to ingredient correctly, just testIngredient
            for recipe_ingredient in recipe.ingredients:
                cursor.execute("""
                    INSERT INTO TestIngredient (name, quantity, unit, recipe_id)
                    VALUES (?, ?, ?, ?)
                """, (
                    recipe_ingredient.name,
                    recipe_ingredient.quantity,
                    recipe_ingredient.unit,
                    new_recipe_id
                ))

            connection.commit()

            return new_recipe_id


    def get_all_recipes(self):
        with sqlite3.connect(self.database_path) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Recipe")
            return [dict(row) for row in cursor.fetchall()]

    def get_recipe(self, recipe_id):
        with sqlite3.connect(self.database_path) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Recipe WHERE id = ?", (recipe_id,))
            row = cursor.fetchone()

            if row:
                recipe_dict =  {
                    "id": row["id"],
                    "title": row["title"],
                    "cuisine": row["cuisine"],
                    "cooking_time": row["cooking_time"],
                    "servings": row["servings"],
                    "diet": json.loads(row["diet"]),
                    "intolerances": json.loads(row["intolerances"]),
                    "steps": json.loads(row["steps"]),
                    "ingredients": self.get_recipe_ingredients(recipe_id),
                }
                return self.construct_recipe_from_dict(recipe_dict)

            else:
                return None

    def get_recipe_ingredients(self, recipe_id):
        with sqlite3.connect(self.database_path) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM TestIngredient WHERE recipe_id = ?", (recipe_id,))
            return [dict(row) for row in cursor.fetchall()]

    def construct_recipe_from_dict(self, dictionary):
        builder = RecipeBuilder(dictionary["title"])

        ingredientList = []
        for ingredient in dictionary["ingredients"]:
            ingredientList.append(RecipeIngredient(ingredient["name"], ingredient["quantity"], ingredient["unit"]))


        recipe = (
            builder
            .set_ID(dictionary["id"])
            .set_ingredients(ingredientList)
            .set_steps(dictionary["steps"])
            .set_cooking_time(dictionary["cooking_time"])
            .set_servings(dictionary["servings"])
            .set_cuisine(dictionary["cuisine"])
            .set_diet(dictionary["diet"])
            .set_intolerances(dictionary["intolerances"])
            .build()
        )

        return recipe

