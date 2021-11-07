from abc import ABC, abstractmethod
# base class for the controllers

class Controller(ABC):
    def __init__(self):
        # store instance of the respective view and model
        self.model = ""
        self.view = ""

    # method for the controller to bind methods to view widgets
    @abstractmethod
    def init(self):
        pass
