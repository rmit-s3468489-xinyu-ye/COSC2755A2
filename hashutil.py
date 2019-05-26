import hashlib, uuid
class hashutil():
    def __init__(self):
        self.__salt = uuid.uuid4().hex
    
    def make_hs_password(self,password):
        """
        encypt the password by using the hash and salt
        """
        return hashlib.sha256(str.encode(password+self.__salt)).hexdigest()
    
    def check_hs_password(self,password,hashsalt):
        """
        ckeck whether password is correct one
        """
        if self.make_hs_password(password) == hashsalt:
            return True
        return False
