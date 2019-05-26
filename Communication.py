
from abc import ABC, abstractmethod

class Communicate(ABC):
    """
    Abstract Class

    """
    
    @abstractmethod
    def send_msg(self,message):
        """
        Used for sending a message by the TCP protocol.

        """
        pass
    
    @abstractmethod
    def recv_msg(self,size,signal):
        """
        Used for receiving a message by the TCP protocol, 
        parameter size is the buffer size to receive each time,
        parameter signal determines whether the result should be printed.

        """
        pass
