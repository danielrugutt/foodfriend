import unittest
from unittest.mock import patch, MagicMock
from flask import request, session
from classes.SpoonacularConnection import SpoonacularConnection
from classes.DietaryPreference import DietaryPreference
from classes.RecipeService import RecipeService
import time
from app import app
from dotenv import load_dotenv
load_dotenv()

class DietaryPreferenceTest(unittest.TestCase):

    def test_no_dietary_prefs(self):
        """User has no dietary preferences, results should not be restricted"""
        user_diet=DietaryPreference([],[],999,[],[])
        search_query = "sachertorte"
        #read from seach bar, search bar is what directs to /search
        user_search=SpoonacularConnection()
        response=str(user_search.getSearchResults(search_query,user_diet))
        expected="{'results': [{'id': 66992, 'title': 'Sachertorte', 'image': 'https://img.spoonacular.com/recipes/66992-312x231.jpg', 'imageType': 'jpg', 'nutrition': {'nutrients': [{'name': 'Sugar', 'amount': 30.4627, 'unit': 'g'}]}}], 'offset': 0, 'number': 10, 'totalResults': 1}"
        self.assertEqual(response,expected)

    def test_non_applicable_prefs(self):
        """User has dietary preferences, results should not be restricted"""
        user_diet=DietaryPreference(["greek"],["watermelon"],999,["shellfish","peanut"],[""])
        search_query = "sachertorte"
        #read from seach bar, search bar is what directs to /search
        user_search=SpoonacularConnection()
        response=str(user_search.getSearchResults(search_query,user_diet))
        expected="{'results': [{'id': 66992, 'title': 'Sachertorte', 'image': 'https://img.spoonacular.com/recipes/66992-312x231.jpg', 'imageType': 'jpg', 'nutrition': {'nutrients': [{'name': 'Sugar', 'amount': 30.4627, 'unit': 'g'}]}}], 'offset': 0, 'number': 10, 'totalResults': 1}"
        self.assertEqual(response,expected)

    def test_some_restricting_prefs(self):
        """User has dietary preferences, some results should not be restricted"""
        user_diet=DietaryPreference([],[""],1,[""],["vegan"])
        search_query = "cake"
        #read from seach bar, search bar is what directs to /search
        user_search=SpoonacularConnection()
        response=str(user_search.getSearchResults(search_query,user_diet))
        expected="{'results': [{'id': 634996, 'title': 'Bird Cakes', 'image': 'https://img.spoonacular.com/recipes/634996-312x231.jpg', 'imageType': 'jpg', 'nutrition': {'nutrients': [{'name': 'Sugar', 'amount': 0.816331, 'unit': 'g'}]}}], 'offset': 0, 'number': 10, 'totalResults': 1}"
        self.assertEqual(response,expected)

    def test_entirely_restricting_prefs(self):
        """User has dietary preferences, there should be no results"""
        user_diet=DietaryPreference(["greek"],[""],999,[""],[""])
        search_query = "gyro"
        #read from seach bar, search bar is what directs to /search
        user_search=SpoonacularConnection()
        response=str(user_search.getSearchResults(search_query,user_diet))
        expected="{'results': [], 'offset': 0, 'number': 10, 'totalResults': 0}"
        self.assertEqual(response,expected)
    

class EmailExportTest(unittest.TestCase):
    """ Testing for 'email recipe' use case with 5 total paths
    Natalie's test cases
    This is a bit weird, references https://docs.python.org/3/library/unittest.mock.html """

    @patch('classes.RecipeService.RecipeService.get_recipe_from_database')
    def test_export_recipe_not_found(self, mock_get_recipe_from_database):
        """ Tests output of email export when recipe is not found """
        mock_get_recipe_from_database.return_value = None

        response = RecipeService.export_recipe(123, "email")

        self.assertEqual(response[1], 404)
        self.assertEqual(response[0], "Recipe not found")

    @patch('classes.RecipeService.RecipeService.get_recipe_from_database')
    def test_export_recipe_with_ingredients_and_steps(self, mock_get_recipe_from_database):
        """ Tests output of email export when recipe has both steps and ingredients """
        # mock recipe
        mock_recipe = MagicMock()
        mock_recipe.title = "Cake"
        mock_recipe.cooking_time = 30
        mock_recipe.servings = 4
        mock_recipe.ingredients = ["Flour", "Eggs", "Sugar"]
        mock_recipe.steps = ["Mix ingredients", "Bake at 350F for 25 minutes"]

        # patching return value of method to the mock recipe
        mock_get_recipe_from_database.return_value = mock_recipe
        response = RecipeService.export_recipe(1, "email")

        # this is pretty quick and easy to compare to rather than a whole wave of asserts
        ideal_result = "mailto:?subject=Cool%20recipe%3A%20Cake&body=Cake%0ACooking%20time%3A%2030%0AServings%3A%204%0A%0AIngredients%20needed%3A%0AFlour%0AEggs%0ASugar%0A%0AStep%201%3A%20Mix%20ingredients%0AStep%202%3A%20Bake%20at%20350F%20for%2025%20minutes"
        self.assertEqual(response.status, "302 FOUND")
        self.assertEqual(ideal_result, response.headers['Location'])

    @patch('classes.RecipeService.RecipeService.get_recipe_from_database')
    def test_export_recipe_no_steps_ingredients(self, mock_get_recipe_from_database):
        """ Tests output of email export when recipe has no steps and ingredients """
        mock_recipe = MagicMock()
        mock_recipe.title = "Cake"
        mock_recipe.cooking_time = 30
        mock_recipe.servings = 4

        mock_get_recipe_from_database.return_value = mock_recipe
        response = RecipeService.export_recipe(2, "email")

        ideal_result = "mailto:?subject=Cool%20recipe%3A%20Cake&body=Cake%0ACooking%20time%3A%2030%0AServings%3A%204%0A%0AIngredients%20needed%3A%0A"
        self.assertEqual(response.status, "302 FOUND")
        self.assertEqual(ideal_result, response.headers['Location'])

    @patch('classes.RecipeService.RecipeService.get_recipe_from_database')
    def test_export_recipe_only_ingredients(self, mock_get_recipe_from_database):
        """ Tests output of email export when recipe has ingredients, but no steps """
        mock_recipe = MagicMock()
        mock_recipe.title = "Cake"
        mock_recipe.cooking_time = 30
        mock_recipe.servings = 4
        mock_recipe.ingredients = ["Flour", "Eggs", "Sugar"]

        mock_get_recipe_from_database.return_value = mock_recipe
        response = RecipeService.export_recipe(2, "email")

        ideal_result = "mailto:?subject=Cool%20recipe%3A%20Cake&body=Cake%0ACooking%20time%3A%2030%0AServings%3A%204%0A%0AIngredients%20needed%3A%0AFlour%0AEggs%0ASugar%0A"
        self.assertEqual(response.status, "302 FOUND")
        self.assertEqual(ideal_result, response.headers['Location'])

    @patch('classes.RecipeService.RecipeService.get_recipe_from_database')
    def test_export_recipe_only_steps(self, mock_get_recipe_from_database):
        """ Tests output of email export when recipe has steps, but no ingredients """
        mock_recipe = MagicMock()
        mock_recipe.title = "Cake"
        mock_recipe.cooking_time = 30
        mock_recipe.servings = 4
        mock_recipe.steps = ["Mix ingredients", "Bake at 350F for 25 minutes"]

        mock_get_recipe_from_database.return_value = mock_recipe
        response = RecipeService.export_recipe(2, "email")

        ideal_result = "mailto:?subject=Cool%20recipe%3A%20Cake&body=Cake%0ACooking%20time%3A%2030%0AServings%3A%204%0A%0AIngredients%20needed%3A%0A%0AStep%201%3A%20Mix%20ingredients%0AStep%202%3A%20Bake%20at%20350F%20for%2025%20minutes"

        self.assertEqual(response.status, "302 FOUND")
        self.assertEqual(ideal_result, response.headers['Location'])

if __name__ == '__main__':
    unittest.main()
