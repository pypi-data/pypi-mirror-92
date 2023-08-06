from abc import ABC, abstractmethod

class HtmlDescriptionProvider(ABC):

    @abstractmethod
    def getHtmlDescription(self):
        pass
