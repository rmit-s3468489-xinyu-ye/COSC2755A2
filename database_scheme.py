import sqlite3

class DatabaseScheme:
    def __init__(self, connection = None):
        if(connection == None):
            connection = self.createConnection()
        self.connection = connection

    def __enter__(self):
        return self

    def close(self):
        self.connection.close()

    def __exit__(self, type, value, traceback):
        self.close()
    
    def createConnection(self):
        try:
            conn = sqlite3.connect('cosc2755a2.db')
            return conn
        except:
            raise Exception("Database Connection Failure")

    def createUsersTable(self):
        conn=self.createConnection()
        cur=conn.cursor()
        try:
            cur.execute('CREATE TABLE if not exists Users(username CHAR(20) PRIMARY KEY NOT NULL,'
                                                         'password CHAR(50) NOT NULL,'
                                                         'firstname CHAR(10) NOT NULL,'
                                                         'lastname CHAR(10) NOT NULL,'
                                                         'email CHAR(25) NOT NULL)')
            conn.commit()
            conn.close()
        except:
            conn.close()
            raise Exception("Failed to create table Users")

    def insertNewUser(self,newData):
        conn=self.createConnection()
        cur=conn.cursor()
        try:
            cur.execute("insert into Users(username, password, firstname, lastname, email) values (?, ?, ?, ?, ?)", (newData))
            conn.commit()
            conn.close()
            return True
        except:
            conn.close()
            return False
            

    def searchUser(self,userData):
        conn=self.createConnection()
        cur=conn.cursor()
        try:
            cur.execute("select password from Users where username=?", (userData,))
            row = cur.fetchone()
            conn.commit()
            conn.close()
            return row
        except:
            conn.close()
            raise Exception("Failed to search the table")