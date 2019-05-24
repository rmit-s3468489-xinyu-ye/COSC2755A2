
from abc import ABC, abstractmethod

class Communicate(ABC):
    
    @abstractmethod
    def send_msg(self,message):
        pass
    
    @abstractmethod
    def recv_msg(self,size,signal):
        pass
