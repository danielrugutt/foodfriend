import json

class RecipeModel(db.Model):
    __tablename__ = 'PlannedMeal'
    recipe = db.relationship("RecipeModel", back_populates="plannedmeal", cascade="all, delete-orphan")
    user = db.relationship("UserModel", back_populates="plannedmeal", cascade="all, delete-orphan")

    datetime =
    title =
    notes =

    def __init__(self, title, cooking_time, servings, cuisine, steps, diet, intolerances):
        self.title = title
        self.cooking_time = cooking_time
        self.servings = servings
        self.cuisine = cuisine
        self.steps = self.to_blob(steps)
        self.diet = self.to_blob(diet)
        self.intolerances = self.to_blob(intolerances)

