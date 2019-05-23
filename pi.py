from abc import ABC, abstractmethod

class pi(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def option(self):
        """
        This method is used for displaying the option for the users who are using 
        this system, for example, for normal user, the need options to register and 
        login, for admin, they can 
        """
        pass
