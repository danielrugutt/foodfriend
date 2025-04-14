import requests
from .DietaryPreference import DietaryPreference
import os

class Search:
    def __init__(self,dietary_preference):
        self.api_key=os.getenv("SPOON_API_KEY")
        self.dietary_preference=dietary_preference
        self.search_address="https://api.spoonacular.com/recipes/complexSearch"

    def search(self, query, dietary_preference=None):
        if dietary_preference is None:
            dietary_preference=self.dietary_preference

        query_payload={'apiKey':self.api_key,
                       'query':query,
                       'diet':dietary_preference.diets,
                       'excludeCuisine':dietary_preference.exclude_cuisine,
                       'excludeIngredients':dietary_preference.exclude_ingredients,
                       'maxSugar':dietary_preference.max_sugar}
        
        response =requests.get(self.search_address, params=query_payload)
        return response.json()


#for recipe in response_json['results']:
#    print(f"Recipe Name: {recipe["title"]} Recipe ID:{recipe["id"]}")

#print(response.json())
