from abc import ABC,abstractmethod

class RecipeAdapter(ABC):
    @abstractmethod
    def standardizeRecipe():
        pass