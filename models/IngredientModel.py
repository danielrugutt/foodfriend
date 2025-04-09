from db import db
import enum

class IngredientType(enum.Enum):
    PROTEIN = "Protein"
    DAIRY = "Dairy"
    OTHER = "Other"

class IngredientModel(db.Model):
    __tablename__ = 'Ingredient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    type = db.Column(db.Enum(IngredientType), nullable=False)

    recipes = db.relationship('RecipeIngredientModel', back_populates='ingredient')
