from abc import ABC, abstractmethod
import os
from fpdf import FPDF

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

        email_text = []
        email_text.append(recipe.title)
        email_text.append("Ingredients needed:")
        for ingredient in recipe.ingredients:
            email_text.append(indedrient.str())


    def exportRecipe(self):
        pass

    def retrieveRecipe(self):
        pass


class DownloadExporter(Exporter):
    def __init__(self, recipe):
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
