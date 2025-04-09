from db import db

class RecipeIngredientModel(db.Model):
    __tablename__ = 'RecipeIngredient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Float)
    unit = db.Column(db.String)

    recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'), nullable=False)
    recipe = db.relationship("RecipeModel", back_populates="ingredients")
