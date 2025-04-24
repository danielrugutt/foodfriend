from models.RecipeListModel import RecipeListModel
from classes.Database import Database

class RecipeService:
    database = None

    @classmethod
    def init(cls, app):
        cls.database = Database(app)
        cls.database.initialize_database()

    @staticmethod
    def get_recipe_from_database(recipe_id):
        recipe = RecipeService.database.get_recipe(recipe_id)

        if recipe is None:
            spoon = SpoonacularConnection()
            recipe = spoon.getRecipe(recipe_id)
            RecipeService.database.insert_recipe(recipe)

        return recipe

    @staticmethod
    def format_recipe_page(recipe_id, session):
        recipe = RecipeService.get_recipe_from_database(recipe_id)

        if recipe is None:
            return "Recipe not found", 404

        uid = session.get("uid")
        user_lists = []

        if uid:
            user_lists = RecipeListModel.query.filter_by(user_id=uid).all()

        return recipe, user_lists, uid
