import socketserver, time
from datetime import datetime,timedelta
from MyError import *
from Communication import Communicate
from dashboard_config import root_url
import requests, json
from BarcodeRecognition import BarRecognition

class Master():
    """
    Master pi, which is used for communicating with Flask Restful API
    to do the google cloud sql crud

    """
    def __init__(self,ipaddress,port):
        self.ipaddress = ipaddress
        self.port = port
        self.master_socket = socketserver.TCPServer((self.ipaddress,self.port),Master.TCPSocketHandler)
        self.master_socket.serve_forever()
    
            
    class TCPSocketHandler(socketserver.BaseRequestHandler,Communicate):
        end_signal = "-- __@**##end##**@__ --"
        start_signal = "-- _@**##start##**@_ --"
        size = 4096
        @staticmethod
        def return_userId(username):
            """
            return the userId by username

            """
            url_userid = root_url + "/user/n/" + username
            name_signal = json.loads(requests.get(url_userid).text)
            return name_signal['LMSUserID']

        def main_menu(self,user,send_msg):
            """
            Main menu for responding to the Reception PI. 
            
            Option 1 is the search function, using socket to communicate with Flask API, 
            get the search result and then return it to the Reception PI. 

            Option 2 is the borrow function, getting the json send by Reception PI, and send the book detail to the Flask API, then
            get the result and send it back to the Rception PI. 

            Option 3 is the normal return function, if the Reception PI send a return book request, Master pi should find the corresponding
            borrowed record from google cloud sql through Flask API, then remove this record. 

            Option 4 is the barcode return function, get the barcode information from the Reception PI, and find out the corresponding 
            borrowed record and remove it.

            Option 5 is the log out function, the Master pi will send back the close message to the Reception pi to close this socket

            """
            self.send_start(send_msg)
            recv_option = self.recv_msg(self.size,False)
            
            if int(recv_option) == 1:
                search_menu = "1. Search by title\n2. Search by author\n3. Search by publish date\n4. Search by speech recognition"
                self.send_msg(search_menu)
                while True:
                    search_opt = self.recv_msg(self.size,False)
                    url = str()
                    if search_opt == 'e':
                        break
                    elif int(search_opt) == 1 or int(search_opt) == 4:
                        book_condition = self.recv_msg(self.size,False)
                        url = root_url + "/book/t/" + book_condition
                    elif int(search_opt) == 2:
                        book_condition = self.recv_msg(self.size,False)
                        url = root_url + "/book/a/" + book_condition
                    else:
                        book_condition = self.recv_msg(self.size,False)
                        url = root_url + "/book/p/" + book_condition
                    result = requests.get(url).text
                    self.send_msg(result)
                self.main_menu(user,send_msg)
            elif int(recv_option) == 2:
                send_borrow = "Please write down the book details, and use && to seperate each field, \
the order of fields should be 'title||author||published date'"
                self.send_msg(send_borrow)
                while True:
                    send_data = self.recv_msg(self.size,False)
                    send_dict = json.loads(send_data)
                    if len(send_dict) == 3: 
                        url_book = root_url + "/book/i"
                        check_book = json.loads(requests.post(url_book,data=send_data,headers={'Content-Type': 'application/json'}).text)
                        if check_book:
                            url_borrowed_book = root_url + "/borrowed/b/" + str(check_book['BookID'])
                            check_borrow = json.loads(requests.get(url_borrowed_book).text)
                            if not check_borrow:
                                uid = Master.TCPSocketHandler.return_userId(user)
                                bid = check_book["BookID"]
                                send_borrowed = {"BookID":bid,"LMSUserID":uid}
                                url_submit = root_url + "/borrowed"
                                requests.post(url_submit,data=json.dumps(send_borrowed),headers={'Content-Type': 'application/json'})
                                send_check_message = {"message":"Borrowed successfully!","flag":True}
                            else:
                                send_check_message = {"message":"This book has already been borrowed","flag":False}
                        else:
                            send_check_message = {"message":"Wrong book details","flag":False}
                        self.send_msg(json.dumps(send_check_message))
                    if send_dict.get("Book") == "Enough":
                        break
                self.main_menu(user,send_msg)
            elif int(recv_option) == 3:
                url_borrowed = root_url + "/borrowed/u/" + str(Master.TCPSocketHandler.return_userId(user))
                return_menu = json.loads(requests.get(url_borrowed).text)
                number = 1
                for item in return_menu:
                    item['itemID'] = number
                    url_bookinfo = root_url + "/book/" + str(item['BookID'])
                    book = json.loads(requests.get(url_bookinfo).text)
                    item['bTitle'] = book['Title']
                    item['bAuthor'] = book['Author']
                    item['bPublishDate'] = book['PublishedDate']
                    number += 1
                self.send_msg(json.dumps(return_menu))
                while True:
                    recv_option = self.recv_msg(self.size,False)
                    if recv_option == 'e':
                        break
                    else:
                        recv_option = int(recv_option)
                        remove_item = dict()
                        for i in return_menu:
                            if i['itemID'] == recv_option:
                                remove_item = i
                                break
                        url_remove = root_url + "/borrowed/" + str(remove_item['BookBorrowedID'])
                        requests.delete(url_remove)
                        return_msg = "This book has been returned successfully!"
                        self.send_msg(return_msg)
                self.main_menu(user,send_msg)
            elif int(recv_option) == 4:
                bardata = self.recv_msg(self.size,False)
                print(bardata)
                bid = BarRecognition().recognize_barcode(bardata)
                print(bid)
                return_message = ""
                if bid != -1:
                    uid = Master.TCPSocketHandler.return_userId(user)
                    send_data = {"BookID":bid,"LMSUserID":uid}
                    url_del = root_url + "/return/" + json.dumps(send_data)
                    requests.delete(url_del)
                    return_message = "This book has been returned successfully!"
                else:
                    return_message = "Sorry, you did not borrow this book!"
                self.send_msg(return_message)
                time.sleep(0.2)
                self.main_menu(user,send_msg)
            else:
                end_message = self.recv_msg(self.size,False)
                print(end_message)
                send_logout = "Logged out successfully!\n"
                self.send_msg(send_logout)
            
        def handle(self):
            """
            waiting for the socket connectted to, when receiving a login request, the Master pi
            decides whether to allow this user to log in or not, if it is allowed, the main menu information
            will be sent back to the Reception pi.

            """
            user_name = self.recv_msg(self.size,False)
            print("Login from {}, the user is {}".format(self.client_address[0],user_name))
            
            send_first = "Waiting for processing....."

            self.continuosly_sending(send_first)

            display_menu = "1. Allow this user to login\n2. Log out this user"
            print(display_menu)
            while True:
                try:
                    menu_choice = int(input("Please select an option: "))

                    if menu_choice == 1:
                        send_menu = "--------------------------------------------------------\n\
Logged in successfully!\nWelcome to the Library System\nLogin: {}\n--------------------------------------------------------\n\
1. Search a book\n2. Borrow a book\n3. Return a book\n4. Return a book by using barcode\n5. Log out".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        self.main_menu(user_name,send_menu)
                        break
                    elif menu_choice == 2:
                        send_refuse = "You are denied login for some reasons, please contact with the librarian directly!\n"
                        self.send_msg(send_refuse)
                        time.sleep(1)
                        self.request.close()
                        print("User {} has been denied login!\n".format(user_name))
                        break
                    else:
                        raise InvalidOptionError()
                except InvalidOptionError as ioe:
                    print(ioe)
                except ValueError:
                    print(InvalidOptionError())
        
        def continuosly_sending(self,msg):
            """
            Continuosly sending without end signal.

            """
            self.request.sendall(msg.encode())
          

        def send_start(self,msg):  
            """
            Send start menu with start signal.

            """
            start = "-- _@**##start##**@_ --"
            self.request.send(msg.encode('UTF-8'))
            self.request.send(start.encode('UTF-8'))
        
        #overriding abstract method
        def send_msg(self,msg):
            """
            Send message with end signal.

            """
            self.request.sendall(msg.encode())
            self.request.sendall(Master.TCPSocketHandler.end_signal.encode()) 
        
        #overriding abstract method
        def recv_msg(self,size,signal):
            """
            If receive message end with end signal or start signal or the receive message 
            is end signal or start signal, it will stop receive and return the result.

            """
            dataset = []
            while 1:
                data = self.request.recv(size).decode()
                if data == Master.TCPSocketHandler.end_signal:
                    break
                if data.endswith(Master.TCPSocketHandler.start_signal):
                    show_data = data[:-23]
                    dataset.append(show_data)
                    dataset.append(data[-23:])
                    if signal:
                        print(show_data)
                    break
                if data.endswith(Master.TCPSocketHandler.end_signal):
                    show_data = data[:-23]
                    dataset.append(show_data)
                    if signal:
                        print(show_data)
                    break
                dataset.append(data)
                if data == Master.TCPSocketHandler.start_signal:
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
    ss = Master("10.132.106.207",12346)
    