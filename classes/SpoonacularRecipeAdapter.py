from classes.RecipeAdapter import RecipeAdapter
from classes.Recipe import *

class SpoonacularRecipeAdapter(RecipeAdapter):
    def __init__(self, spoonacularID):
        self.ID=spoonacularID
                            
    def standardizeRecipe(self, recipe_info, steps_info):
        try:
            recipe = RecipeBuilder(recipe_info['title'])
            recipe.set_ID(recipe_info['id'])
            recipe.set_servings(recipe_info['servings'])
            recipe.set_cuisine(", ".join([item for item in recipe_info['cuisines']]))
            recipe.set_cuisine(", ".join([item for item in recipe_info['diets']]))
            recipe.set_cooking_time(recipe_info['readyInMinutes'])
            recipe.set_img_url(recipe_info['image'])
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

        except:
            return None
