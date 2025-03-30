from abc import ABC, abstractmethod
import os

class Exporter(ABC):
    @abstractmethod
    def formatRecipe(self):
        pass

    @abstractmethod
    def exportRecipe(self, destination, recipe):
        pass

    @abstractmethod
    def retrieveRecipe(self):
        pass


class ShareExporter(Exporter):
    def __init__(self, destination, recipe):
        self.api_key=os.getenv("SPOON_API_KEY")
        self.outgoing_email = destination
        self.recipe = recipe

    def formatRecipe(self):
        self.email_subject = (
            "Cool recipe: ", recipe.title
        )

        # email_text = []
        # email_text.append(recipe.title)
        # email_text.append("Ingredients needed:")
        # for RecipeIngredient in recipe.ingredients:
        #     email_text.append(


    def exportRecipe(self):
        pass

    def retrieveRecipe(self):
        pass


class DownloadExporter(Exporter):
    def __init__(self, recipe):
        self.api_key=os.getenv("SPOON_API_KEY")
        self.recipe = recipe

    def formatRecipe(self):
        pass

    def exportRecipe(self):
        pass

    def retrieveRecipe(self):
        pass
