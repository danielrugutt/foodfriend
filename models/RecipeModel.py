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









