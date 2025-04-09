from db import db
from models.RecipeIngredientModel import RecipeIngredientModel
import json

class RecipeModel(db.Model):
    __tablename__ = 'Recipe'
    ingredients = db.relationship("RecipeIngredientModel", back_populates="recipe", cascade="all, delete-orphan")

    # LargeBinary is like a blob
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    cooking_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    cuisine = db.Column(db.String)
    steps = db.Column(db.LargeBinary)
    diet = db.Column(db.LargeBinary)
    intolerances = db.Column(db.LargeBinary)

    def __init__(self, title, cooking_time, servings, cuisine, steps, diet, intolerances):
        self.title = title
        self.cooking_time = cooking_time
        self.servings = servings
        self.cuisine = cuisine
        self.steps = self.to_blob(steps)
        self.diet = self.to_blob(diet)
        self.intolerances = self.to_blob(intolerances)

    def to_blob(self, data):
        return json.dumps(data).encode("utf-8") if data else b''

    def from_blob(self, blob_data):
        return json.loads(blob_data.decode("utf-8")) if blob_data else []

    def get_steps(self):
        return self.from_blob(self.steps)

    def get_diet(self):
        return self.from_blob(self.diet)

    def get_intolerances(self):
        return self.from_blob(self.intolerances)

    @staticmethod
    def recipe_to_recipe_model(recipe_object):
        recipe_model = RecipeModel(
            title=recipe_object.title,
            cooking_time=recipe_object.cooking_time,
            servings=recipe_object.servings,
            cuisine=recipe_object.cuisine,
            steps=recipe_object.steps,
            diet=recipe_object.diet,
            intolerances=recipe_object.intolerances
        )

        recipe_model.ingredients = [
            RecipeIngredientModel(
                name=ingredient.name,
                quantity=ingredient.quantity,
                unit=ingredient.unit,
                recipe=recipe_model
            )
            for ingredient in recipe_object.ingredients
        ]

        return recipe_model

    def to_recipe_object(self):
        from classes.Recipe import Recipe, RecipeIngredient, Nutrition


        ingredient_list = []
        for ingredient in self.ingredients:
            ingredient_list.append(RecipeIngredient(name=ingredient.name, quantity=ingredient.quantity, unit=ingredient.unit))

         # placeholder
        nutrition_info = Nutrition(0, 0, 0, 0)

        return Recipe(
            title=self.title,
            ingredients=ingredient_list,
            steps=self.get_steps(),
            cooking_time=self.cooking_time,
            nutrition_info=nutrition_info,
            servings=self.servings,
            cuisine=self.cuisine,
            diet=self.get_diet(),
            intolerances=self.get_intolerances(),
            ID=self.id,
            img_url=None
        )


