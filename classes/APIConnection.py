from abc import ABC,abstractmethod

class APIConnection(ABC):
    @abstractmethod
    def getRecipe():
        #return Recipe object
        pass

    @abstractmethod
    def getSearchResults():
        #returns JSON object of search results with the following fields:
        #title image id
        pass