from classes.APIConnection import APIConnection
import os
import requests
from classes.SpoonacularRecipeAdapter import SpoonacularRecipeAdapter
import time

class SpoonacularConnection(APIConnection):
    
    def __init__(self):
        self.api_key=os.getenv("SPOON_API_KEY")
        self.search_address="https://api.spoonacular.com/recipes/complexSearch"
        

    def getRecipe(self,ID):
        recipe_adapter=SpoonacularRecipeAdapter(ID)
        recipe_address=f"https://api.spoonacular.com/recipes/{ID}/information"
        instruction_address=f"https://api.spoonacular.com/recipes/{ID}/analyzedInstructions"
        query_payload={'apiKey':self.api_key}
        recipe_info=requests.get(recipe_address,query_payload)
        recipe_info=recipe_info.json()
        #spoonacular API limit
        time.sleep(1.5)
        steps_info=requests.get(instruction_address,query_payload)
        steps_info=steps_info.json()
        return recipe_adapter.standardizeRecipe(recipe_info,steps_info)

    def getSearchResults(self,query,dietary_preference=None):
        query_payload={'apiKey':self.api_key,
                'query':query,
                'diet':dietary_preference.diets,
                'excludeCuisine':dietary_preference.exclude_cuisine,
                'excludeIngredients':dietary_preference.exclude_ingredients,
                'maxSugar':dietary_preference.max_sugar}
        
        response =requests.get(self.search_address, params=query_payload)
        return response.json()
    
    def getSimilarResults(self, ID):
        similar_address=f"https://api.spoonacular.com/recipes/{ID}/similar"
        query_payload={'apiKey':self.api_key}
        similar_recipies=requests.get(similar_address,query_payload)
        #print(similar_recipies.json())
        similar_recipies=similar_recipies.json()
        return similar_recipies

        

        