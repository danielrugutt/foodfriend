class DietaryPreference:
    def __init__(self,exclude_cuisine,exclude_ingredients,max_sugar,intolerances,diets):
        self.exclude_cuisine=exclude_cuisine
        self.exclude_ingredients=exclude_ingredients
        self.max_sugar=max_sugar
        self.intolerances=intolerances
        self.diets=diets

    def update_preferences(self, DietaryPreference):
        self=DietaryPreference
