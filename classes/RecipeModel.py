from typing import List
from sqlalchemy.dialects.sqlite import BLOB
from .Database import Database, db
import json

class RecipeModel(db.Model):
    __tablename__ = 'Recipe'
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
        self.steps = self._to_blob(steps)
        self.diet = self._to_blob(diet)
        self.intolerances = self._to_blob(intolerances)

    def get_steps(self):
        return self._from_blob(self.steps)

    def get_diet(self):
        return self._from_blob(self.diet)

    def get_intolerances(self):
        return self._from_blob(self.intolerances)
