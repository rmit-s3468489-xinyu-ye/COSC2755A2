import socketserver, time
from datetime import datetime
from customisedError import *

class Master:

    def __init__():
        pass
    
    def option(self):
        pass


class Server():
   
    def __init__(self):
        self.ipadress = "127.0.0.1"
        self.port = 12345
        self.master_socket = socketserver.TCPServer((self.ipadress,self.port),Server.TCPSocketHandler)
        self.master_socket.serve_forever()
              
    
    class TCPSocketHandler(socketserver.BaseRequestHandler):
        end_signal = "-- __@**##end##**@__ --"
        
        def main_menu(self,user,send_msg,end_signal):
            self.send_start(send_msg)
            recv_option = int(self.recv_msg())
            
            if recv_option == 1:
                search_menu = "1. search by author\n2. search by title\n3. search by publish date"
                self
            elif recv_option == 2:
                pass
            elif recv_option == 3:
                pass
            else:
                end_message = self.recv_msg()
                print(end_message)
                send_logout = "Log out successful!\n"
                self.send_msg(send_logout,Server.TCPSocketHandler.end_signal)
                time.sleep(0.5)
                self.request.close()
            
        def handle(self):
            user_name = self.recv_msg()
            print("Login from {}, the user is {}".format(self.client_address[0],user_name))
            
            send_first = "Waiting for processing....."

            self.continuosly_sending(send_first)

            display_menu = "1. Allow this user login\n2. Log out this user"
            
            print(display_menu)
            while True:
                try:
                    menu_choice = int(input("please select the option: "))

                    if menu_choice == 1:
                        send_menu = "--------------------------------------------------------\n\
Login successful!\nWelcome to Library System\nLogin: {}\n--------------------------------------------------------\n\
1. search a book\n2. borrow a book\n3. return a book\n4. log out\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        self.main_menu(user_name,send_menu,Server.TCPSocketHandler.end_signal)
                        break
                    elif menu_choice == 2:
                        send_refuse = "You are denied login for some reasons, please contact with the reception staff directly!\n"
                        self.send_msg(send_refuse,Server.TCPSocketHandler.end_signal)
                        time.sleep(0.5)
                        self.request.close()
                        print("User {} has been denied login!".format(user_name))
                        break
                    else:
                        raise InvalidOptionError()
                except InvalidOptionError as ioe:
                    print(ioe)
                except ValueError:
                    print(InvalidOptionError())
        
        def continuosly_sending(self,msg):
            self.request.sendall(msg.encode())

        def send_msg(self,msg,end_signal):
            self.request.sendall(msg.encode())
            self.request.sendall(Server.TCPSocketHandler.end_signal.encode())   

        def send_start(self,msg):  
            start = "-- _@**##start##**@_ --"
            self.request.sendall(msg.encode())
            self.request.sendall(start.encode())
    
        def recv_msg(self):
            dataset = []
            while 1:
                data = self.request.recv(4096).decode()
                if data == Server.TCPSocketHandler.end_signal:
                    break
                dataset.append(data)
            if len(dataset) == 0:
                return None
            elif len(dataset) == 1:
                return dataset[0]
            else:
                return dataset
        
            
ss = Server()
    
   