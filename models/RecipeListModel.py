from db import db

class RecipeListModel(db.Model):
    __tablename__ = 'RecipeList'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    user = db.relationship("UserModel", backref="recipe_lists")

    recipes = db.relationship("RecipeListRecipeModel", back_populates="recipe_list", cascade="all, delete-orphan")


    def recipe_objects(self):
        return [entry.recipe for entry in self.recipes]

class RecipeListRecipeModel(db.Model):
    """ Join table, since recipelist to recipes is a many to many and we need to break it up """
    __tablename__ = 'RecipeList_Recipes'

    recipe_list_id = db.Column(db.Integer, db.ForeignKey('RecipeList.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'), primary_key=True)

    recipe_list = db.relationship("RecipeListModel", back_populates="recipes")
    recipe = db.relationship("RecipeModel")
