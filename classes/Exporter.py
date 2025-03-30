from abc import ABC, abstractmethod
import os

class Exporter(ABC):
    @abstractmethod
    def formatRecipe(self):
        pass

    @abstractmethod
    def exportRecipe(self):
        pass

    @abstractmethod
    def retrieveRecipe(self):
        pass


class ShareExporter(Exporter):
    def __init__(self, recipe):
        self.api_key=os.getenv("SPOON_API_KEY")
        self.outgoing_email = outgoing_email
        self.recipe = recipe

    def formatRecipe(self):
        pass

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
