from db import db
from models import RecipeModel

class PlannedMeal(db.Model):
    __tablename__ = 'PlannedMeal'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'), nullable=False)  # ForeignKey pointing to Recipe table
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)  # ForeignKey pointing to UserModel table

    recipe = db.relationship("RecipeModel", back_populates="plannedmeals")
    user = db.relationship("UserModel", back_populates="plannedmeals")

    datetime = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String, nullable=False, unique=False)
    notes = db.Column(db.String, nullable=True, unique=False)

    def __init__(self, title, user, recipe, datetime, notes):
        self.title = title
        self.user = user
        self.recipe = recipe
        self.datetime = datetime
        self.notes = notes
