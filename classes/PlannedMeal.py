from datetime import date
import time

class PlannedMeal:
    def __init__(self, day, time, title, recipe, notes = None):
        self.day = day
        self.time = time
        self.title = title
        self.notes = notes
        self.recipe = recipe
