from datetime import date
import time

class PlannedMeal:
    def __init__(self, datetime, title, recipe, serving_size, notes = None):
        self.datetime = datetime
        self.title = title
        self.notes = notes
        self.recipe = recipe
        self.serving_size = serving_size
