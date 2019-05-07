import hashlib, uuid
import getpass
import re
import pickle
from HashUtil import HashUtil
from customisedError import *
from localDB import LocalDb
from datetime import datetime
# from PI import pi
class Reception(object):
    
    def __init__(self):
        self.localDB = LocalDb()
        
    
    def option(self):
        print("1. registration")
        print("2. log in")
        opt = int(input("Please select the option: "))
        if opt == 1:
            self.__registration()
        if opt == 2:
            self.__login()
            self.sub_option()
    
    def sub_option(self):
        print("1. search a book")
        print("2. borrow a book")
        print("3. return a book")
        print("4. log out")
        opt = int(input("Please select the option: "))

    def __login(self):
        while True:
            try:
                user_name = input("Please enter your username: ")
                user_password = getpass.getpass(prompt="Please enter your password: ")
                if self.localDB.checkUsername(user_name):
                    valid_user = self.localDB.getInfo(user_name)
                    original = pickle.loads(valid_user[3])
                    condition = original.check_hs_password(user_password,valid_user[2])
                    if condition:
                        print("--------------------------------------------------------")
                        print("Login successful!")
                        print("Welcome to Library System")
                        print("Login: "+ datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        print("--------------------------------------------------------")
                        break
                    else:
                        raise PasswordError()
                else:
                    raise UsernameError()
            except UsernameError as ue:
                print(ue)
            except PasswordError as pe:
                print(pe)
        
    def __registration(self):
        username = self.__usernameValidation()
        password, encypted = self.__passwordValidation() 
        first, last = self.__nameValidation() 
        email = self.__emailValidation()
        self.localDB.uploadToDB(username,password,encypted,first,last,email)
       
    def __usernameValidation(self):  
        username_pattern = r'^[a-zA-Z][a-zA-Z_0-9]*$'  
        while(True):
            try:
                username = input("Please enter the username: ")
                umatch = re.fullmatch(username_pattern,username)
                exist = self.localDB.checkUsername(username)
                if umatch and not exist and len(username) >= 3 and len(username) < 100:
                    break
                elif not umatch:
                    raise InvalidUsernameError()
                elif exist:
                    raise DuplicatedUsernameError()
                else:
                    raise UsernameLengthError()
            except InvalidUsernameError as iue:
                print(iue)
            except DuplicatedUsernameError as due:
                print(due)
            except UsernameLengthError as ule:
                print(ule)
        return username

    def __passwordValidation(self):
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9\s\n\r])[^\s\n\r]+$'
        while(True):
            try:
                password = getpass.getpass(prompt="Please enter your password: ")
                pmatch = re.fullmatch(password_pattern,password)
                if pmatch and len(password) >= 6:
                    confirm_password = getpass.getpass(prompt="Please confirm your password: ")
                    if confirm_password == password:
                        encrypted = HashUtil()
                        encrypted_password = encrypted.make_hs_password(confirm_password)
                        encrypted = pickle.dumps(encrypted)
                        break
                    else:
                        raise PasswordsInconsistentError()
                elif not pmatch:
                    raise InvalidPasswordError()
                else:
                    raise PasswordTooShortError()
                    
            except InvalidPasswordError as ipe:
                print(ipe)
            except PasswordTooShortError as ptse:
                print(ptse)
            except PasswordsInconsistentError as pie:
                print(pie)
        return encrypted_password, encrypted
    
    def __nameValidation(self):
        name_pattern = r'^[a-zA-Z][a-zA-Z_]*$' 
        while(True):
            try:
                first_name = input("Please enter your first name: ")
                fnmatch = re.fullmatch(name_pattern,first_name)
                if fnmatch and len(first_name) > 0 and len(first_name) < 100:
                    break
                elif not fnmatch:
                    raise InvalidNameError()
                else:
                    raise NameLengthError()
            except InvalidNameError as ine:
                print(ine)
            except NameLengthError as nle:
                print(nle)
        while(True):
            try:
                last_name = input("Please enter your last name: ")
                lnmatch = re.fullmatch(name_pattern,last_name)
                if lnmatch and len(last_name) > 0 and len(last_name) < 100:
                    break
                elif not lnmatch:
                    raise InvalidNameError()
                else:
                    raise NameLengthError()
            except InvalidNameError as ine:
                print(ine)
            except NameLengthError as nle:
                print(nle)

        return first_name, last_name
    
    def __emailValidation(self):
        email_pattern = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]+)$'
        while(True):
            try:
                email = input("Please enter your email: ")
                ematch = re.fullmatch(email_pattern,email)
                if ematch and len(email) < 100:
                    break
                else:
                    raise InvalidEmailError()
            except InvalidEmailError as iee:
                print(iee)
        return email
