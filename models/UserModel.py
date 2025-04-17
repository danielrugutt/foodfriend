from models import DietaryPreferenceModel
from db import db

class UserModel(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False)

    recipe_lists = db.relationship("RecipeListModel", back_populates="user", cascade="all, delete-orphan")
    # mealhistory

    # uselist makes it a one to one relationship
    dietary_preferences = db.relationship("DietaryPreferenceModel", back_populates="user", cascade="all, delete-orphan", uselist=False)

