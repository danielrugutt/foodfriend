import sqlite3
import json
import os

DATABASE_PATH = "database/foodfriend.db"
DATABASE_SCHEMA = "database/testing.sql"

def initialize_database():
    if not os.path.exists(DATABASE_PATH):
        print("Database does not exist, creating!");
        connection = sqlite3.connect(DATABASE_PATH)
        databaseFile = open(DATABASE_SCHEMA, "r")
        connection.executescript(databaseFile.read())
        databaseFile.close()

def insert_recipe(recipe):
    with sqlite3.connect(DATABASE_PATH) as connection:
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


def get_all_recipes():
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Recipe")
        return [dict(row) for row in cursor.fetchall()]

def get_recipe(recipe_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Recipe WHERE id = ?", (recipe_id,))
        row = cursor.fetchone()

        if row:
            return {
                "id": row["id"],
                "title": row["title"],
                "cuisine": row["cuisine"],
                "cooking_time": row["cooking_time"],
                "servings": row["servings"],
                "diet": json.loads(row["diet"]),
                "intolerances": json.loads(row["intolerances"]),
                "steps": json.loads(row["steps"]),
                "ingredients": get_recipe_ingredients(recipe_id),
            }
        else:
            return None

def get_recipe_ingredients(recipe_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM TestIngredient WHERE recipe_id = ?", (recipe_id,))
        return [dict(row) for row in cursor.fetchall()]
