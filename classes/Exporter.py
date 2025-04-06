from abc import ABC, abstractmethod
import os
from fpdf import FPDF
from flask import redirect
import urllib.parse

class Exporter(ABC):
    @abstractmethod
    def exportRecipe(self, destination, recipe):
        pass


class ShareExporter(Exporter):
    def __init__(self, destination, recipe):
        self.api_key=os.getenv("SPOON_API_KEY")
        self.outgoing_email = destination
        self.recipe = recipe
        print(recipe)

    def exportRecipe(self):
        email_subject = "Cool recipe: " + self.recipe.title

        email_body = [
            self.recipe.title,
            "",
            "Ingredients needed:"
        ]

        for ingredients in self.recipe.ingredients:
            email_body.append(str(ingredients))

        email_body.append("")
        for i, step in enumerate(self.recipe.steps, start=1):
            email_body.append(f"Step {i}: {step}")

        completed_body = "\n".join(email_body)

        clean_subject = urllib.parse.quote(email_subject)
        clean_body = urllib.parse.quote(completed_body)

        mailto_link = f"mailto:?subject={clean_subject}&body={clean_body}"

        return redirect(mailto_link)


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
