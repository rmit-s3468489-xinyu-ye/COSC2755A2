import socket, requests, json, time, re, pickle, getpass, hashlib, uuid
from hashUtil import HashUtil
from customisedError import *
from localDB import LocalDb
from datetime import datetime
from dashboardConfig import root_url
# from PI import pi
class Reception(object):
    
    def __init__(self):
        self.localDB = LocalDb()
        self.client = Client("127.0.0.1",12345)
        self.start_signal = "-- _@**##start##**@_ --"
        self.end_signal = "-- __@**##end##**@__ --"
        
    
    def option(self):
        opt = int(input("1. registration\n2. log in\nPlease select the option: "))
        if opt == 1:
            self.__registration()
            self.option()
        if opt == 2:
            while True:
                try:
                    user_name = input("Please enter your username: ")
                    user_password = getpass.getpass(prompt="Please enter your password: ")
                    usr_name = self.__login(user_name,user_password)
                    break
                except UsernameError as ue:
                    print(ue)
                except PasswordError as pe:
                    print(pe)
            self.client.send_msg(usr_name,self.end_signal)
            dataset = self.client.recv_msg()

            if self.start_signal in dataset:
                while True:
                    try:
                        send_option = input("Please select an option: ")
                        if int(send_option) > 0 and int(send_option) < 4:
                            self.client.send_msg(send_option,self.end_signal)
                            self.client.recv_msg()
                            break
                        elif int(send_option) == 4:
                            self.client.send_msg(send_option,self.end_signal)
                            message = "User {} log out".format(usr_name)
                            self.client.send_msg(message,self.end_signal)
                            self.client.recv_msg()
                            break
                        else:
                            raise InvalidOptionError()
                    except InvalidOptionError as ioe:
                        print(ioe)
                    except ValueError:
                        print(InvalidOptionError())
            time.sleep(0.5)
            self.__init__()
            self.option()


    def __login(self,user_name,user_password):
        if self.localDB.checkUsername(user_name):
            valid_user = self.localDB.getInfo(user_name)
            original = pickle.loads(valid_user[3])
            condition = original.check_hs_password(user_password,valid_user[2])
            if condition:
                return user_name
            else:
                raise PasswordError()
        else:
            raise UsernameError()
        
    def __registration(self):
        username = self.__username_validation()
        password, encypted = self.__password_validation() 
        first, last = self.__name_validation() 
        email = self.__email_validation()
        self.localDB.uploadToDB(username,password,encypted,first,last,email)
        #send_data = {"UserName":username,"FirstName":first,"LastName":last,"Email":email}
        #url = root_url + "/user"
        #requests.post(url,data=json.dumps(send_data),headers={'Content-Type': 'application/json'})
       
    def __username_validation(self):  
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

    def __password_validation(self):
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9\s\n\r])[^\s\n\r]+$'
        while(True):
            try:
                password = getpass.getpass(prompt="Please enter your password: ")
                pmatch = re.fullmatch(password_pattern,password)
                if pmatch and len(password) >= 6:
                    confirm_password = getpass.getpass(prompt="Please confirm your password: ")
                    if confirm_password == password:
                        encrypted U hashutil()
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
    
    def __name_validation(self):
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
    
    def __email_validation(self):
        email_pattern = r'^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]+)$'
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


class Client:
    def __init__(self,ipaddr,port):
        self.reception_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.ipaddr = ipaddr
        self.port = port
        self.connection = self.reception_socket.connect((ipaddr,port))

    def send_msg(self,msg,end_signal):
        self.reception_socket.sendall(msg.encode())
        self.reception_socket.sendall(end_signal.encode())
            
    
    def recv_msg(self):
        end_signal = "-- __@**##end##**@__ --"
        start_signal = "-- _@**##start##**@_ --"
        dataset = []
        while 1:
            data = self.reception_socket.recv(4096).decode()
            if data == end_signal:
                break
            dataset.append(data)
            if data == start_signal:
                break
            print(data)
            
        if len(dataset) == 0:
            return None
        elif len(dataset) == 1:
            return dataset[0]
        return dataset
            
if __name__ =="__main__":
    r = Reception()
    r.option()
