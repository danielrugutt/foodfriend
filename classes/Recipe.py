from typing import List

class RecipeIngredient:
    # units not always needed - eggs, for example
    def __init__(self, name: str, quantity: float, unit: str = None):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    def __str__(self):
        if self.unit is None:
            return self.quantity + " " + self.name
        return self.quantity + " " + self.unit + " of " + self.name

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
                 diet: List[str], intolerances: List[str]):
        self.title = title
        self.ingredients = ingredients
        self.steps = steps
        self.cooking_time = cooking_time
        self.nutrition_info = nutrition_info
        self.servings = servings
        self.cuisine = cuisine
        self.diet = diet
        self.intolerances = intolerances

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

    def build(self):
        return Recipe(self.title, self.ingredients, self.steps,
                      self.cooking_time, self.nutrition_info, self.servings,
                      self.cuisine, self.diet, self.intolerances)


