import hashlib, uuid
class HashUtil():
    def __init__(self):
        self.__salt = uuid.uuid4().hex
    
    def make_hs_password(self,password):
        return hashlib.sha256(str.encode(password+self.__salt)).hexdigest()
    
    def check_hs_password(self,password,hashsalt):
        if self.make_hs_password(password) == hashsalt:
            return True
        return False
