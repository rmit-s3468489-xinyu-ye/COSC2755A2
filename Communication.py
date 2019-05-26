
from abc import ABC, abstractmethod

class Communicate(ABC):
    """
    abstract class
    """
    
    @abstractmethod
    def send_msg(self,message):
        """
        used for sending a message by using TCP protocol 
        """
        pass
    
    @abstractmethod
    def recv_msg(self,size,signal):
        """
        used for receive a message by using TCP protocol 
        parameter size is the buffer size each time to receive 
        parameter signal is judge whether should print the result
        """
        pass
