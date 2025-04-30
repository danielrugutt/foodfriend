from datetime import date
import time

class PlannedMeal:
    def __init__(self, datetime, title, recipe, notes = None):
        self.datetime = datetime
        self.title = title
        self.notes = notes
        self.recipe = recipe
