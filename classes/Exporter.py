from abc import ABC, abstractmethod
import os
from fpdf import FPDF
from flask import redirect, make_response
import io
import urllib.parse

# class Creator(ABC):
#     @abstractmethod
#     def factory_method(self, recipe):
#         pass
#
#
# class ExporterCreator(Creator):
#     def factory_method(self, recipe) -> PDFExporter:
#         return PDFExporter(recipe)

class Exporter(ABC):
    @abstractmethod
    def exportRecipe(self, recipe):
        pass

class EmailExporter(Exporter):
    def __init__(self, recipe):
        self.recipe = recipe

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


class PDFExporter(Exporter):
    def __init__(self, recipe):
        self.recipe = recipe

    # NOTE WHEN ADDING TO THIS - IF YOU DO NOT DO PDF.LN BEFORE ADDING ANOTHER CELL, FORMATTING WILL BREAK IN STRANGE AND DRAMATIC WAYS
    def exportRecipe(self):
        # initial setup
        pdf = FPDF("P", "in", "Letter")
        pdf.add_page()
        pdf.set_font("Courier", size=16)
        pdf.cell(0, 0.5, self.recipe.title)
        pdf.ln(0.3)

        # ingredients
        pdf.set_font("Courier", size=12)
        pdf.cell(0, 0.3, "Ingredients")
        pdf.ln(0.3)
        for ingredient in self.recipe.ingredients:
            pdf.cell(0, 0.3, str(ingredient), ln=True)
        pdf.ln(0.3)

        # steps
        pdf.cell(0, 0.3, "Steps")
        pdf.ln(0.3)
        for i, step in enumerate(self.recipe.steps, start=1):
            pdf.multi_cell(0, 0.3, txt=f"{i}. {step}")

        # saving in RAM to not have to make temporary files
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        pdf_output = io.BytesIO(pdf_bytes)

        response = make_response(pdf_output.read())
        response.headers.set("Content-Type", "application/pdf")
        response.headers.set(
            "Content-Disposition", f"attachment; filename={self.recipe.title}"
        )
        return response

