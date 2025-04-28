class DietaryPreference:
    def __init__(self,exclude_cuisine,exclude_ingredients,max_sugar,intolerances,diets):
        self.exclude_cuisine=exclude_cuisine
        self.exclude_ingredients=exclude_ingredients
        self.max_sugar=max_sugar
        self.intolerances=intolerances
        self.diets=diets

    def update_preferences(self, new_pref):
        self.exclude_cuisine = new_pref.exclude_cuisine
        self.exclude_ingredients = new_pref.exclude_ingredients
        self.max_sugar = new_pref.max_sugar
        self.intolerances = new_pref.intolerances
        self.diets = new_pref.diets
