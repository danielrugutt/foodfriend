from classes.RecipeAdapter import RecipeAdapter
from classes.Recipe import *
import os
import requests 
import time

class SpoonacularRecipeAdapter(RecipeAdapter):
    def __init__(self, spoonacularID):
        self.ID=spoonacularID
        self.api_key=os.getenv("SPOON_API_KEY")
        self.recipe_address=f"https://api.spoonacular.com/recipes/{spoonacularID}/information"
        self.instruction_address=f"https://api.spoonacular.com/recipes/{spoonacularID}/analyzedInstructions"
        self.query_payload={'apiKey':self.api_key}
                            
    def standardizeRecipe(self):
        recipe_info=requests.get(self.recipe_address,self.query_payload)
        recipe_info=recipe_info.json()
        #spoonacular API limit
        time.sleep(1.5)
        steps_info=requests.get(self.instruction_address,self.query_payload)
        steps_info=steps_info.json()
        recipe = RecipeBuilder(recipe_info['title'])
        recipe.set_servings(recipe_info['servings'])
        recipe.set_cuisine(", ".join([item for item in recipe_info['cuisines']]))
        recipe.set_cuisine(", ".join([item for item in recipe_info['diets']]))
        recipe.set_cooking_time(recipe_info['readyInMinutes'])
        ingredients=[]
        for ingredient_info in recipe_info['extendedIngredients']:
            ingredients.append(RecipeIngredient(ingredient_info['name'],ingredient_info['measures']['us']['amount'],ingredient_info['measures']['us']['unitShort']))
        recipe.set_ingredients(ingredients)
        steps=[]
        for step in steps_info[0]['steps']:
            steps.append(step['step'])
            #print(step['step'])
        recipe.set_steps(steps)

        recipe=recipe.build()
        return recipe