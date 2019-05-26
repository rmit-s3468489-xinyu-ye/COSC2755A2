import socket, requests, json, time, re, pickle, getpass, hashlib, uuid
from hashutil import hashutil
from MyError import *
from LocalDB import localdb
from datetime import datetime
from dashboard_config import root_url
from Communication import Communicate
from searchByCondition import SearchRecognition
from FacialAuthorized import AuthorizedFacialReconition
import threading
from BarcodeRecognition import BarRecognition
from add_event import addEvent


class Reception(object):
    """
    Reception PI, used for allowing user to interact with the library and it communicates with Master PI 
    to get the result or authorization
    """
    def __init__(self,localDB,client,recognition,
            size=4096,start_signal="-- _@**##start##**@_ --"):
        self.localDB = localDB
        self.client = client
        self.recognition = recognition
        self.size = size
        self.start_signal = start_signal
        self.facial_authorized = AuthorizedFacialReconition()
        

    def option(self):
        """
        option 1, registration.

        option 2, login, when logining in, it will wait the Master pi to deal with it.

        option 3, remove a exist user from the local database.

        option 4, register a face for the person who already exists in the database.

        option 5, login to the system via facial recognition, instead of typing the username and password manually.
        """
        while True:
            try:
                opt = int(input("1. Registration\n2. Login\n3. Remove the user\n4. Register a face\n5. Facial Recognition Login\nPlease select an option: "))
                if opt == 1:
                    self.registration()
                    self.option()
                elif opt == 2:
                    flag = False
                    while True:
                        try:
                            user_name = input("Please enter your username(Forgot username? Enter 'e' to exit): ")
                            if user_name == 'e':
                                break
                            user_password = getpass.getpass(prompt="Please enter your password: ")
                            usr_name = self.login(user_name,user_password)
                            flag = True
                            break
                        except UsernameError as ue:
                            print(ue)
                        except PasswordError as pe:
                            print(pe)
                    if flag:
                        self.client.send_msg(usr_name)
                        self.main_menu(usr_name)
                    else:
                        self.option()
                elif opt == 3:
                    while True:
                        try:
                            user_name = input("Please enter the user name which you want to remove: ")
                            if self.localDB.checkUsername(user_name):
                                self.localDB.removeUser(user_name)
                                break
                            else:
                                raise UserNotFoundError()
                        except UserNotFoundError as une:
                            print(une)
                    self.option()
                elif opt == 4:
                    print("In order to add you photo, we need to verify your identity, please enter your username and password")
                    while True:
                        try:
                            user_name = input("Username(Forgot username? Enter 'e' to exit): ")
                            if user_name == 'e':
                                break
                            user_password = getpass.getpass(prompt="Password: ")
                            usr_name = self.login(user_name,user_password)
                            self.facial_authorized.record_user_face(usr_name)
                            #open a new thread to encode the pic without influencing the main thread 
                            new_thread = threading.Thread(target=self.facial_authorized.encode_user_face,name='encode_thread')
                            new_thread.daemon = True
                            new_thread.start()
                            print("Face recorded successfully")
                            break
                        except UsernameError as ue:
                            print(ue)
                        except PasswordError as pe:
                            print(pe)
                    self.option()
                elif opt == 5:
                    usr_name = self.facial_authorized.recognise_user_face()
                    if usr_name !="":
                        self.client.send_msg(usr_name)
                        self.main_menu(usr_name)
                    else:
                        self.option()
                else:
                    raise InvalidOptionError()
            except InvalidOptionError as ioe:
                print(ioe)
            except ValueError:
                print(InvalidOptionError())
    
    def main_menu(self,usr_name):
        """
        option 1, send a search request to the Master pi, type 'e' to exit.

        option 2, send a borrow request to the Master pi, the format should be following the instruction.

        option 3, show the book this user has already borrowed, send a normal return request to 
        the Master pi, to return a book.

        option 4, scan a barcode instead of typing the book details to return a book

        option 5, log out the system.
        """
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
                                search_option = input("Please enter an option(enter 'e' to exit): ")
                                if search_option == 'e':
                                    self.client.send_msg(search_option)
                                    break
                                elif int(search_option) >= 1 and int(search_option) <= 3:
                                    self.client.send_msg(search_option)
                                    search_book = input("Please enter the search content: ")
                                    self.client.send_msg(search_book)
                                    result = self.client.recv_msg(self.size,False)
                                    result = json.loads(result)
                                    if result:
                                        print("{:30s} {:30s} {:30s}".format("Book title","Book author","Book published date"))
                                        for item in result:
                                            print("{:30s} {:30s} {:30s}".format(item['Title'],item['Author'],item['PublishedDate']))
                                        print()
                                    else:
                                        print("No matched book has been found with provided information !\n")
                                elif int(search_option) == 4:
                                    self.client.send_msg(search_option)
                                    while True:
                                        try:
                                            prmt = "Say the book title to search for."
                                            speach_content = self.recognition.getSearchText(prmt)
                                            confirm_opt = input("Do you mean \'{}\', type 'y' to confirm, or type 'n' to say again: ".format(speach_content))
                                            if confirm_opt == 'y' or confirm_opt == 'Y':
                                                self.client.send_msg(speach_content)
                                                result = self.client.recv_msg(self.size,False)
                                                result = json.loads(result)
                                                if result:
                                                    print("{:30s} {:30s} {:30s}".format("Book title","Book author","Book published date"))
                                                    for item in result:
                                                        print("{:30s} {:30s} {:30s}".format(item['Title'],item['Author'],item['PublishedDate']))
                                                    print()
                                                else:
                                                    print("No matched book has been found with provided information !\n")
                                                break
                                            elif confirm_opt == 'n' or confirm_opt == 'N':
                                                continue
                                            else:
                                                raise InvalidOptionError()
                                        except InvalidOptionError as ioe:
                                            print(ioe)
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
                                book_detail = input("You want to borrow(enter 'e' to exit): ")
                                book_detail = book_detail.split("||")    
                                if len(book_detail) == 3:
                                    send_book = {"Title":book_detail[0],"Author":book_detail[1],"PublishedDate":book_detail[2]}
                                    send_book = json.dumps(send_book)
                                    self.client.send_msg(send_book)
                                    result = json.loads(self.client.recv_msg(self.size,False))
                                    if result['flag']:
                                        addEvent().insert()
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
                                opt = input("Please select a book to return(enter 'e' to exit): ")
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
                        bardata = BarRecognition().add_barcode()
                        self.client.send_msg(str(bardata))
                        self.client.recv_msg(self.size,True)
                        time.sleep(0.2)
                        self.main_menu(usr_name)
                    elif int(send_option) == 5:
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
        self.__init__(localdb(),Client("10.132.106.207",12346),
                SearchRecognition("Sound Blaster Play! 3: USB Audio (hw:1,0)"))
        self.option()
        


    def login(self,user_name,user_password):
        """
        Login function, get the username and password input by the user, and check the password by 
        using the object which created this password, as different object will generate different 
        salt.

        """
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
        
    def registration(self):
        """
        Registration function, verifies all the fields

        """
        username = self.username_validation()
        password, encypted = self.password_validation() 
        first, last = self.name_validation() 
        email = self.email_validation()
        self.localDB.uploadToDB(username,password,encypted,first,last,email)
        send_data = {"UserName":username,"FirstName":first,"LastName":last,"Email":email}
        url = root_url + "/user"
        requests.post(url,data=json.dumps(send_data),headers={'Content-Type': 'application/json'})
       
    def username_validation(self):  
        """
        Username validation, if the username already exists in the database, it 
        will show an error message, and you need to type in a new username, and 
        a new username must start with the letters and is only allowed to 
        contain the letters or _ or numbers.

        """
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

    def password_validation(self):
        """
        Password validation, password must contain at least an uppper case letter and
        a lower case letter and a special character and a number, and the min length of it is 6. 
        After that this method will return the encrypted password and the object used for creating this encrypted password will 
        be returned.

        """
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9\s\n\r])[^\s\n\r]+$'
        while(True):
            try:
                password = getpass.getpass(prompt="Please enter your password: ")
                pmatch = re.fullmatch(password_pattern,password)
                if pmatch and len(password) >= 6:
                    confirm_password = getpass.getpass(prompt="Please confirm your password: ")
                    if confirm_password == password:
                        encrypted = hashutil()
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
    
    def name_validation(self):
        """
        Name validation, a new name must start with letters and is only allowed to contain 
        letters or _.

        """
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
    
    def email_validation(self):
        """
        Email validation, a new email address must follow the following pattern. 

        """
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
    """
    Connect to the server and communicate with it

    """
    def __init__(self,ipaddr,port,end_signal = "-- __@**##end##**@__ --",
    start_signal = "-- _@**##start##**@_ --"):
        self.reception_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.ipaddr = ipaddr
        self.port = port
        self.end_signal = end_signal
        self.start_signal = start_signal
        self.connection = self.reception_socket.connect((ipaddr,port))
    
    #overriding abstract method
    def send_msg(self,msg):
        """
        Send message with end signal

        """
        self.reception_socket.sendall(msg.encode())
        self.reception_socket.sendall(self.end_signal.encode())
            
    
    #overriding abstract method
    def recv_msg(self,size,signal):
        """
        If the received message ends with end signal or start signal or the received message 
        is end signal or start signal, it will stop receiving and return the result.

        """
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
    r = Reception(localdb(),Client("10.132.106.207",12346),
            SearchRecognition("Sound Blaster Play! 3: USB Audio (hw:1,0)"))
    r.option()
