from typing import List

class RecipeIngredient:
    # units not always needed - eggs, for example
    def __init__(self, name: str, quantity: float, unit: str = None):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    def __str__(self):
        if self.unit is None:
            return str(self.quantity) + " " + self.name
        return str(self.quantity) + " " + self.unit + " " + self.name

class Nutrition:
    # THIS IS MISSING SO MUCH STUFF but it's just a placeholder for now
    def __init__(self, calories: int, protein: float, carbs: float, fats: float):
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fats = fats

class Recipe:
    def __init__(self, title: str, ingredients: List[RecipeIngredient], steps: List[str],
                 cooking_time: int, nutrition_info: Nutrition, servings: int, cuisine: str,
                 diet: List[str], intolerances: List[str], ID: int, img_url: str = None):
        self.img_url = img_url
        self.title = title
        self.ingredients = ingredients
        self.steps = steps
        self.cooking_time = cooking_time
        self.nutrition_info = nutrition_info
        self.servings = servings
        self.cuisine = cuisine
        self.diet = diet
        self.intolerances = intolerances
        self.ID = ID

class RecipeBuilder:
    def __init__(self, title):
        self.title = title
        self.ingredients = []
        self.steps = []
        self.cooking_time = 0
        self.nutrition_info = None
        self.servings = 0
        self.cuisine = None
        self.diet = []
        self.intolerances = []
        self.ID = 0
        self.img_url = None

    def set_ingredients(self, ingredients: List[RecipeIngredient]):
        self.ingredients = ingredients
        return self

    def set_steps(self, steps: List[str]):
        self.steps = steps
        return self

    def set_cooking_time(self, time: int):
        self.cooking_time = time
        return self

    def set_nutrition_info(self, info: Nutrition):
        self.nutrition_info = info
        return self

    def set_servings(self, servings: int):
        self.servings = servings
        return self

    def set_cuisine(self, cuisine: str):
        self.cuisine = cuisine
        return self

    def set_diet(self, diet: List[str]):
        self.diet = diet
        return self

    def set_intolerances(self, intolerances: List[str]):
        self.intolerances = intolerances
        return self

    # only use this when grabbing a recipe from the database! the recipe will have its ID set when being entered into the database, and if this is set then, it will be ignored
    def set_ID(self, ID: int):
        self.ID = ID
        return self

    def set_img_url(self, img_url: str):
        self.img_url = img_url
        return self

    def build(self):
        return Recipe(self.title, self.ingredients, self.steps,
                      self.cooking_time, self.nutrition_info, self.servings,
                      self.cuisine, self.diet, self.intolerances, self.ID,self.img_url)


