import unittest
from classes.SpoonacularConnection import SpoonacularConnection
from classes.DietaryPreference import DietaryPreference
import time
from dotenv import load_dotenv
load_dotenv()

class TestRecipeExport(unittest.TestCase):

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
    



if __name__ == '__main__':
    unittest.main()