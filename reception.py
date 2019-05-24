import socket, requests, json, time, re, pickle, getpass, hashlib, uuid
from hashUtil import HashUtil
from customisedError import *
from localDB import LocalDb
from datetime import datetime
from dashboard_config import root_url
from communicate import Communicate
# from PI import pi

class Reception(object):
    
    def __init__(self):
        self.localDB = LocalDb()
        self.client = Client("127.0.0.1",12346)
        self.size = 4096
        self.start_signal = "-- _@**##start##**@_ --"
        
    def checkBorrowed():
        pass

    def option(self):
        while True:
            try:
                opt = int(input("1. registration\n2. log in\n3. remove the user\nPlease select the option: "))
                if opt == 1:
                    self.__registration()
                    self.option()
                elif opt == 2:
                    while True:
                        try:
                            user_name = input("Please enter your username: ")
                            user_password = getpass.getpass(prompt="Please enter your password: ")
                            usr_name,first_name,last_name,email_addr = self.__login(user_name,user_password)
                            break
                        except UsernameError as ue:
                            print(ue)
                        except PasswordError as pe:
                            print(pe)
                    self.client.send_msg(usr_name)
                    self.main_menu(usr_name)
                elif opt == 3:
                    while True:
                        try:
                            user_name = input("Please enter the user name which you want to remove: ")
                            if self.localDB.checkUsername(user_name):
                                self.localDB.removeUser(user_name)
                                break
                                pass
                            else:
                                raise UserNotFoundError()
                        except UserNotFoundError as une:
                            print(une)
                    self.option()
                else:
                    raise InvalidOptionError()
            except InvalidOptionError as ioe:
                print(ioe)
            except ValueError:
                print(InvalidOptionError())
    
    def main_menu(self,usr_name):
        dataset = self.client.recv_msg(self.size,True)
        if self.start_signal in dataset:
            while True:
                try:
                    send_option = input("Please select an option: ")
                    if int(send_option) == 1:
                        self.client.send_msg(send_option)
                        self.client.recv_msg(self.size,True)
                        while True:
                            try:
                                search_option = input("please enter an option(enter e to exit): ")
                                if search_option == 'e':
                                    self.client.send_msg(search_option)
                                    break
                                elif int(search_option) >= 1 and int(search_option) <= 3:
                                    self.client.send_msg(search_option)
                                    search_book = input("please enter the search content: ")
                                    self.client.send_msg(search_book)
                                    result = self.client.recv_msg(self.size,False)
                                    if result:
                                        result = json.loads(result)
                                        print("{:30s} {:30s} {:30s}".format("Book title","Book author","Book published date"))
                                        for item in result:
                                            print("{:30s} {:30s} {:30s}".format(item['Title'],item['Author'],item['PublishedDate']))
                                        print()
                                    else:
                                        print("The book has not been founded\n")
                                else:
                                    raise InvalidOptionError()
                            except InvalidOptionError as ioe:
                                print(ioe)
                            except ValueError:
                                print(InvalidOptionError())
                        self.main_menu(usr_name) 
                    elif int(send_option) == 2:
                        self.client.send_msg(send_option)
                        self.client.recv_msg(self.size,True)
                        while True:
                            try:
                                book_detail = input("You want to borrow(enter e to exit): ")
                                book_detail = book_detail.split("||")    
                                if len(book_detail) == 3:
                                    send_book = {"Title":book_detail[0],"Author":book_detail[1],"PublishedDate":book_detail[2]}
                                    send_book = json.dumps(send_book)
                                    self.client.send_msg(send_book)
                                    result = json.loads(self.client.recv_msg(self.size,False))
                                    if result['flag']:
                                        print(result['message'])
                                    
                                    else:
                                        raise BorrowedFailedError(result['message'])
                                    time.sleep(1)
                                elif len(book_detail) == 1 and book_detail[0] == 'e':
                                    send_book = {"Book":"Enough"}
                                    send_book = json.dumps(send_book)
                                    self.client.send_msg(send_book)
                                    time.sleep(1)
                                    break
                                else:
                                    raise InvalidInputFormatError()
                            except InvalidInputFormatError as iife:
                                print(iife)
                            except BorrowedFailedError as bfe:
                                print(bfe.message)
                        self.main_menu(usr_name)                              
                    elif int(send_option) == 3:
                        self.client.send_msg(send_option)
                        recieve_list = json.loads(self.client.recv_msg(self.size,False))
                        print("{:5s} {:30s} {:30s} {:25s} {:25s} {:25s}".format("Item",
                        "Title","Author","Publish date","Borrowed date","Return date"))
                        for i in recieve_list:
                            print("{:5s} {:30s} {:30s} {:25s} {:25s} {:25s}".format(str(i['itemID']),
                            i['bTitle'],i['bAuthor'],i['bPublishDate'],i['BorrowedDate'],i['ReturnedDate']))
                        while True:
                            try:
                                opt = input("Please select one book to return(enter e to exit): ")
                                if opt == 'e':
                                    self.client.send_msg(str(opt))
                                    break
                                if recieve_list:
                                    if int(opt) <= len(recieve_list) and int(opt) >= 1:
                                        self.client.send_msg(str(opt))
                                        self.client.recv_msg(self.size,True)
                                    else:
                                        raise InvalidOptionError()
                                else:
                                    raise InvalidOptionError()
                            except InvalidOptionError as ioe:
                                print(ioe)
                            except ValueError:
                                print(InvalidOptionError())
                        self.main_menu(usr_name)
                    elif int(send_option) == 4:
                        self.client.send_msg(send_option)
                        message = "User {} log out\n".format(usr_name)
                        time.sleep(0.25)
                        self.client.send_msg(message)
                        self.client.recv_msg(self.size,True)
                        time.sleep(0.25)
                        self.client.reception_socket.close()
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
                return user_name, valid_user[4], valid_user[5], valid_user[6]
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
        send_data = {"UserName":username,"FirstName":first,"LastName":last,"Email":email}
        url = root_url + "/user"
        requests.post(url,data=json.dumps(send_data),headers={'Content-Type': 'application/json'})
       
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


class Client(Communicate):
    def __init__(self,ipaddr,port):
        self.reception_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.ipaddr = ipaddr
        self.port = port
        self.end_signal = "-- __@**##end##**@__ --"
        self.start_signal = "-- _@**##start##**@_ --"
        self.connection = self.reception_socket.connect((ipaddr,port))
    
    #overriding abstract method
    def send_msg(self,msg):
        self.reception_socket.sendall(msg.encode())
        self.reception_socket.sendall(self.end_signal.encode())
            
    
    #overriding abstract method
    def recv_msg(self,size,signal):
        
        dataset = []
        while 1:
            data = self.reception_socket.recv(size).decode()
            if data == self.end_signal:
                break
            if data.endswith(self.start_signal): 
                show_data = data[:-23]
                dataset.append(show_data)
                dataset.append(data[-23:])
                if signal:
                    print(show_data)
                break
            if data.endswith(self.end_signal):
                show_data = data[:-23]
                dataset.append(show_data)
                if signal:
                    print(show_data)
                break
            dataset.append(data)
            if data == self.start_signal:
                break
            if signal:
                print(data)
        if len(dataset) == 0:
            return None
        elif len(dataset) == 1:
            return dataset[0]
        else:
            return dataset


if __name__ =="__main__":
    r = Reception()
    r.option()
