from db import db

class RecipeIngredientModel(db.Model):
    __tablename__ = 'RecipeIngredient'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float)
    unit = db.Column(db.String)

    recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('Ingredient.id'), nullable=False)

    recipe = db.relationship("RecipeModel", back_populates="ingredients")
    ingredient = db.relationship("IngredientModel", back_populates="recipes")

