# from customisedError import *
# import getpass
# import re
# from hashUtil import HashUtil
# import pickle

# class b:
#     def registration(self):
#         username = self.__usernameValidation()
#         password, encypted = self.__passwordValidation() 
#         first, last = self.__nameValidation() 
#         email = self.__emailValidation()
        
#         return username,password,encypted, first, last, email  
        
#     def __usernameValidation(self):  
#         username_pattern = r'^[a-zA-Z][a-zA-Z_0-9]*$'  
#         while(True):
#             try:
#                 username = input("Please enter the username: ")
#                 if re.fullmatch(username_pattern,username) and len(username) >= 3:
#                     break
#                 elif not re.fullmatch(username_pattern,username):
#                     raise InvalidUsernameError()
#                 else:
#                     raise UsernameTooShortError()
#             except InvalidUsernameError as iue:
#                 print(iue)
#             except UsernameTooShortError as utse:
#                 print(utse)
#         return username

#     def __passwordValidation(self):
#         password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9\s\n\r])[^\s\n\r]+$'
#         while(True):
#             try:
#                 password = getpass.getpass(prompt="Please enter your password: ")
#                 if re.fullmatch(password_pattern,password) and len(password) >= 6:
#                     confirm_password = getpass.getpass(prompt="Please confirm your password: ")
#                     if confirm_password == password:
#                         encrypted = HashUtil()
#                         encrypted_password = encrypted.make_hs_password(confirm_password)
#                         encrypted = pickle.dumps(encrypted)
#                         break
#                     else:
#                         raise PasswordsInconsistentError()
#                 elif not re.fullmatch(password_pattern,password):
#                     raise InvalidPasswordError()
#                 else:
#                     raise PasswordTooShortError()
                    
#             except InvalidPasswordError as ipe:
#                 print(ipe)
#             except PasswordTooShortError as ptse:
#                 print(ptse)
#             except PasswordsInconsistentError as pie:
#                 print(pie)
#         return encrypted_password, encrypted
    
#     def __nameValidation(self):
#         name_pattern = r'^[a-zA-Z][a-zA-Z_]*$' 
#         while(True):
#             try:
#                 first_name = input("Please enter your first name: ")
#                 if re.fullmatch(name_pattern,first_name):
#                     break
#                 else:
#                     raise InvalidNameError()
#             except InvalidNameError as ine:
#                 prnt(ine)
#         while(True):
#             try:
#                 last_name = input("Please enter your last name: ")
#                 if re.fullmatch(name_pattern,last_name):
#                     break
#                 else:
#                     raise InvalidNameError()
#             except InvalidNameError as ine:
#                 prnt(ine)

#         return first_name, last_name
    
#     def __emailValidation(self):
#         email_pattern = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]+)$'
#         while(True):
#             try:
#                 email = input("Please enter your email: ")
#                 if re.fullmatch(email_pattern,email):
#                     break
#                 else:
#                     raise InvalidEmailError()
#             except InvalidEmailError as iee:
#                 prnt(iee)
#         return email



# # t = b()

# # u,p,e,f,l,em = t.registration()
# # print(u,p,e,f,l,em)
# # print(u,p)

# # i = "aA1!23"
# # s = pickle.loads(e)
# # print(s.check_hs_password(i,p))
# # p = input("in: ")
# # print(type(p))
# # print(p)
# # print(p==1)
# # from datetime import datetime
# # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# import socket

# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# s.connect(("127.0.0.1",6000))
# upload_file = r'c:\Users\Administrator\hello\IOT_assignment2\text.txt'

# with open(upload_file,'r') as fp:
#     line = fp.readline()
#     while True:
#         if not line:
#             print(11111111111)
#             break
#         s.sendall(line.encode())
#         print(line.encode())
#         line = fp.readline()
# msg = s.recv(1024).decode()
# print(msg)
# mmm = s.sendall("yoyoyo",encode())
        


# send_data = "hello, server, nice to meet you!"
# s.sendall(send_data.encode())
# # l=0
# try:
#     while True:
#         data = s.recv(16)
#         print("recieve from server: " + data.decode())
#         if not data:
#             print("no data")
#             break
#         # l+=len(data)
# except:
#     pass


# with open(upload_file,'r') as fp:
#     line = fp.readline().encode()
#     while True:
#         s.sendall(line)
#         line = fp.readline().encode()
#         if not line:
#             break





# # def get_host_ip():
# #     try:
# #         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# #         s.connect(('www.google.com.au', 80))
# #         ipaddr = s.getsockname()[0]
# #     finally:
# #         s.close()
# #     return ipaddr
# # print(get_host_ip())

# import socket

# serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# print(socket.gethostname())
# print(socket.gethostbyname("Hasee-PC"))



# class b():
#     def call_a(self):
#         i = a()
#         y = i.add(2,9)
#         print(y)

# class a():
#     def add(self,a,b):
#         return a+b


# tt = b()
# tt.call_a()


# import socketserver



# class u:
#     def __init__(self):
#         s = socketserver.TCPServer(("127.0.0.1",12345),u.MyTCPSocketHandler)

#         s.serve_forever()
    
#     class MyTCPSocketHandler(socketserver.BaseRequestHandler):
#         def handle(self):
#             self.data = self.request.recv(1024)
#             print("{} sent".format(self.client_address[0]))
#             self.request.sendall(self.data.upper())


# p = u()






import socket,time
from customisedError import *
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
            
           

class Reception(object):
    
    def __init__(self):
        self.client = Client("127.0.0.1",12345)
        self.start_signal = "-- _@**##start##**@_ --"
        self.end_signal = "-- __@**##end##**@__ --"
        
    
    def option(self):
        op = input("option1,2: ")
        if int(op) == 1:
            print("ok")
        if int(op)==2:
            while True:
                usr_name = input("enter name: ")
                if usr_name=="jack":
                    break
       
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

if __name__ =="__main__":
    re = Reception()
    re.option()