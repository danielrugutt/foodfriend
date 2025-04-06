from abc import ABC, abstractmethod
import os
from fpdf import FPDF

class Exporter(ABC):
    @abstractmethod
    def exportRecipe(self, destination, recipe):
        pass


class ShareExporter(Exporter):
    def __init__(self, destination, recipe):
        self.api_key=os.getenv("SPOON_API_KEY")
        self.outgoing_email = destination
        self.recipe = recipe

    def exportRecipe(self):
        self.email_subject = (
            "Cool recipe: ", self.recipe.title
        )

        email_text = []
        email_text.append(self.recipe.title)
        email_text.append("Ingredients needed:")
        for ingredient in self.recipe.ingredients:
            email_text.append(ingredient.str())

        stepNumber = 1
        for step in self.recipe.steps:
            email_text.append("Step " + stepNumber + ": " + step)

        print(email_text)


class DownloadExporter(Exporter):
    def __init__(self, destination, recipe):
        self.api_key=os.getenv("SPOON_API_KEY")
        self.recipe = recipe
        self.pdf = None

    def formatRecipe(self):
        self.pdf = FPDF("P", "in", "Letter")
        self.pdf.add_page()
        self.pdf.set_font('Courier', 16)
        self.pdf.cell(0, 0, self.recipe.title)

    def exportRecipe(self):
        pass

    def retrieveRecipe(self):
        pass
