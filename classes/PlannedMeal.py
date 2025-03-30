from datetime import date
import time

class PlannedMeal:
    def __init__(self, day, time, title, recipe, notes):
        self.day = day
        self.time = time
        self.title = title
        self.notes = notes
        self.recipe = recipe

    def __init__(self, day, time, title, recipe):
        """ Initialization without notes """
        self.day = day
        self.time = time
        self.title = title
        self.recipe = recipe
