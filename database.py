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

def insert_recipe(data):
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Recipe (title, cooking_time, servings, cuisine, steps, diet, intolerances)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data["title"],
            data["cookingTime"],
            data["servings"],
            data["cuisine"],
            json.dumps(data["steps"]),
            json.dumps(data["diet"]),
            json.dumps(data["intolerances"]),
        ))
        connection.commit()

def get_all_recipes():
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Recipe")
        return [dict(row) for row in cursor.fetchall()]
