from flask import Flask, render_template, request, session, abort, jsonify, redirect
from datetime import datetime,timedelta, time
from classes.Database import Database
from models.UserModel import UserModel
from models.RecipeModel import RecipeModel
from models.RecipeListModel import RecipeListModel
from models.PlannedMeal import PlannedMeal

class CalendarService:
    database = None

    @classmethod
    def init(cls, app):
        """ Initializes the database and makes it a class variable. Must be initialized before using in app.py """
        cls.database = Database(app)
        cls.database.initialize_database()

    @staticmethod
    def add_meal(session):
        """ Creates a planned meal and adds it to the database """
        data = request.get_json()

        title = data.get("title")
        start_time = data.get("startTime")  # e.g., "14:00"
        serving_size = data.get("serving_size")
        notes = data.get("notes")
        recipe_id = data.get("recipe_id")
        start_date = data.get("start")      # e.g., "2025-04-29"

        if not all([title, start_time, start_date, serving_size]):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            combined_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            return jsonify({"error": "Invalid time format. Use 24 Hour format (00:00)"}), 400
        
        user_id = session.get("uid")
        if not user_id:
            return jsonify({"error": "User not logged in"}), 401

        user = CalendarService.database.get_user(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        recipe = CalendarService.database.get_recipe(recipe_id) if recipe_id else None
        recipe_model = CalendarService.database.recipe_to_recipe_model(recipe)

        new_meal = PlannedMeal(
            title=title,
            datetime=combined_datetime,
            serving_size=serving_size,
            notes=notes,
            user=user,
            recipe=recipe_model if recipe_model else None
        )

        CalendarService.database.insert_planned_meal(new_meal)

        return jsonify({"message": "Meal added successfully"}), 200
    
    @staticmethod
    def delete_meal(meal_id):
        """ Deletes a meal from the database given its id """
        meal = PlannedMeal.query.get(meal_id)
        if not meal:
            return jsonify({"error": "Meal not found"}), 404

        CalendarService.database.delete_planned_meal(meal)
        return jsonify({"message": "Meal deleted successfully"})

    @staticmethod
    def edit_meal():
        """ Updates a meal in the database with new information """
        data = request.get_json()
        meal_id = data.get("id")
        title = data.get("title")
        serving_size = data.get("serving_size")
        start_time = data.get("startTime")
        notes = data.get("notes")
        recipe_id = data.get("recipe_id")
        start_date = data.get("start")

        if not all([meal_id, title, start_time, start_date, serving_size]):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            combined_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            return jsonify({"error": "Invalid time format. Use 24 Hour format (00:00)"}), 400

        meal = PlannedMeal.query.get(meal_id)
        if not meal:
            return jsonify({"error": "Meal not found"}), 404

        meal.title = title
        meal.serving_size = serving_size
        meal.datetime = combined_datetime
        meal.notes = notes
        meal.recipe_id = recipe_id

        CalendarService.database.commit()
        return jsonify({"message": "Meal updated successfully"})
    
    @staticmethod
    def get_all_recipes():
        """ Retrieves and formats all the bookmarked recipes and the list they belong to """
        test_user_id = session.get("uid")
        if not test_user_id:
            return redirect('/login')

        # Fetch all recipe lists for the user
        recipe_lists = RecipeListModel.query.filter_by(user_id=test_user_id).all()

        grouped_recipes = []
        for recipe_list in recipe_lists:
            # Get recipes for each list
            recipes = recipe_list.recipe_objects()
            grouped_recipes.append({
                'list_name': recipe_list.name,
                'recipes': [{'id': recipe.id, 'name': recipe.title} for recipe in recipes]
            })

        return jsonify(grouped_recipes)
    
    @staticmethod
    def get_planned_meals():
        """ Retrievs all the planned meals from the database, formats them, and returns a json with them """
        user_id = session.get("uid")
        if not user_id:
            return jsonify({"error": "User not logged in"}), 401
        user = session.get(UserModel, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        if not user:
            return jsonify([])

        meals = PlannedMeal.query.filter_by(user_id=user_id).all()

        events = []
        for meal in meals:
            start_dt = meal.datetime
            end_dt = start_dt + timedelta(hours=1)

            events.append({
                "title": f"{meal.title}",
                "id": f"{meal.id}",
                "start": start_dt.isoformat(),
                "end": end_dt.isoformat(),
                "extendedProps": {
                    "recipe_id": meal.recipe.id,
                    "serving_size": meal.serving_size,
                    "notes": meal.notes or ""
                }
            })

        return jsonify(events)
    
    @staticmethod
    def format_meal_page(meal_id, session):
        """ Returns the meal page given an ID """
        meal = PlannedMeal.query.get(meal_id)
        recipe = meal.recipe
        steps = recipe.get_steps()

        if recipe is None:
            return "Recipe not found.", 404

        uid = session.get("uid")

        return render_template("meal_recipe.html", meal=meal, uid=uid, steps=steps)