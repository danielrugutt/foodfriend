from datetime import date
import time

class PlannedDay:
    def __init__(self, day, count, plannedMeals = List[PlannedMeal]):
        self.day = day
        self.count = count
        self.plannedMeals = plannedMeals
