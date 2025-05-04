import unittest
from unittest.mock import patch, MagicMock
from flask import request, session, json
from classes.SpoonacularConnection import SpoonacularConnection
from classes.DietaryPreference import DietaryPreference
from classes.RecipeService import RecipeService
from classes.AuthService import AuthService
from classes.CalendarService import CalendarService
from datetime import datetime
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

# @patch('classes.AuthService.auth')
class AuthServiceTest(unittest.TestCase):
    
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        
    def tearDown(self):
        """Clean up the app context after each test."""
        app.view_functions.pop('protected', None)

    @patch('classes.AuthService.auth.verify_id_token')
    def test_authorize_valid_token(self, mock_verify_id_token):
        """Test the /auth route with a valid Firebase ID token."""
        # Mock the Firebase ID token verification
        mock_verify_id_token.return_value = {'uid': '12345', 'email': 'test@example.com'}

        # Simulate a POST request to the /auth route with a valid token
        response = self.app.post('/auth', headers={
            'Authorization': 'Bearer valid_token'
        })

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User authenticated successfully', response.data)
        
    @patch('classes.AuthService.auth.verify_id_token')
    def test_authorize_invalid_token(self, mock_verify_id_token):
        """Test the /auth route with an invalid Firebase ID token."""
        # Mock the Firebase ID token verification to raise an exception
        mock_verify_id_token.side_effect = Exception("Invalid token")

        # Simulate a POST request to the /auth route with an invalid token
        response = self.app.post('/auth', headers={
            'Authorization': 'Bearer invalid_token'
        })

        # Assert the response
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Unauthorized', response.data)
        
    @patch('classes.AuthService.auth.verify_id_token')
    def test_logout(self, mock_verify_id_token):
        """Test the /logout route to ensure the user is logged out."""
        # Simulate a user session
        with self.app.session_transaction() as session:
            session['user'] = {'uid': '12345', 'email': 'test@example.com'}

        # Simulate a GET request to the /logout route
        response = self.app.get('/logout')

        # Assert the response
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/login', response.location)
        
        # Ensure the session is cleared
        with self.app.session_transaction() as session:
            self.assertNotIn('user', session)

    def test_auth_required_decorator(self):
        """Test the @auth_required decorator to enforce authentication."""
        @app.route('/protected')
        @AuthService.auth_required
        def protected_route():
            return "Protected content", 200

        # Simulate a request without a user session
        response = self.app.get('/protected')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)  # Check for relative URL

        # Add a user session to simulate authentication
        with self.app.session_transaction() as session:
            session['user'] = {'uid': '12345', 'email': 'test@example.com'}

        # Simulate a request with a user session
        response = self.app.get('/protected')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Protected content', response.data)

    def test_authorize_missing_token(self):
        """Test the /auth route with a missing Authorization header."""
        response = self.app.post('/auth')  # No headers
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'"error":"Authorization header missing or invalid"', response.data)


class AddMealTest(unittest.TestCase):
    """ Testing for 'add meal' use case with 6 total paths """

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.context = app.app_context()
        self.context.push()

        self.valid_data = {
            "title": "Lunch",
            "startTime": "12:30",
            "notes": "Healthy food",
            "recipe_id": 1,
            "start": "2025-04-30",
            "serving_size": 2  
        }
        self.mock_session = {"uid": "user123"}

    def tearDown(self):
        self.context.pop()

    @patch('classes.CalendarService.CalendarService.database')
    def test_add_meal_success(self, mock_db):
        mock_user = MagicMock()
        mock_recipe = MagicMock()
        mock_recipe_model = MagicMock()

        mock_db.get_user.return_value = mock_user
        mock_db.get_recipe.return_value = mock_recipe
        mock_db.recipe_to_recipe_model.return_value = mock_recipe_model
        mock_db.insert_planned_meal.return_value = None

        with app.test_request_context(json=self.valid_data):
            response, status = CalendarService.add_meal(self.mock_session)

        self.assertEqual(status, 200)
        self.assertEqual(response.get_json()["message"], "Meal added successfully")

    def test_add_meal_missing_required_fields(self):
        incomplete_data = self.valid_data.copy()
        incomplete_data.pop("startTime")

        with app.test_request_context(json=incomplete_data):
            response, status = CalendarService.add_meal(self.mock_session)

        self.assertEqual(status, 400)
        self.assertEqual(response.get_json()["error"], "Missing required fields")

    def test_add_meal_invalid_datetime_format(self):
        invalid_data = self.valid_data.copy()
        invalid_data["startTime"] = "99:99"

        with app.test_request_context(json=invalid_data):
            response, status = CalendarService.add_meal(self.mock_session)

        self.assertEqual(status, 400)
        self.assertEqual(response.get_json()["error"], "Invalid time format. Use 24 Hour format (00:00)")

    def test_add_meal_user_not_logged_in(self):
        with app.test_request_context(json=self.valid_data):
            response, status = CalendarService.add_meal(session={})

        self.assertEqual(status, 401)
        self.assertEqual(response.get_json()["error"], "User not logged in")

    @patch('classes.CalendarService.CalendarService.database')
    def test_add_meal_user_not_found(self, mock_db):
        mock_db.get_user.return_value = None

        with app.test_request_context(json=self.valid_data):
            response, status = CalendarService.add_meal(self.mock_session)

        self.assertEqual(status, 404)
        self.assertEqual(response.get_json()["error"], "User not found")

    @patch('classes.CalendarService.CalendarService.database')
    def test_add_meal_without_recipe(self, mock_db):
        mock_user = MagicMock()

        mock_db.get_user.return_value = mock_user
        mock_db.get_recipe.return_value = None
        mock_db.recipe_to_recipe_model.return_value = None
        mock_db.insert_planned_meal.return_value = None

        no_recipe_data = self.valid_data.copy()
        no_recipe_data["recipe_id"] = None

        with app.test_request_context(json=no_recipe_data):
            response, status = CalendarService.add_meal(self.mock_session)

        self.assertEqual(status, 200)
        self.assertEqual(response.get_json()["message"], "Meal added successfully")



if __name__ == '__main__':
    unittest.main()
