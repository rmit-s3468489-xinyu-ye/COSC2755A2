import MySQLdb

class localdb(object):

    def __init__(self):
        self.host = "localhost"
        self.user = "pi"
        self.password = "secret"
        self.database = "LMS"
        self.connection = MySQLdb.connect(self.host,self.user,self.password,self.database)
    
    def createTable(self):
        """
        Create the table UserInfo, id is the primary key, username is unique, and the encypt used 
        for storing the class hashutil object.

        """
        with self.connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS UserInfo")
            cursor.execute('''CREATE TABLE UserInfo(id INT AUTO_INCREMENT PRIMARY KEY,
             username VARCHAR(100) UNIQUE NOT NULL, password VARCHAR(100) NOT NULL, 
             encrypt MEDIUMBLOB, firstname VARCHAR(100) NOT NULL, lastname VARCHAR(100) NOT NULL,
             email VARCHAR(100) NOT NULL)''')
            self.connection.commit()
    
    def uploadToDB(self,username,password,encrypt,firstname,lastname,email):
        """
        Upload the user information to the local database.

        """
        dataset = (username,password,encrypt,firstname,lastname,email,)
        stmt = '''INSERT INTO UserInfo(username,password,encrypt,firstname,
        lastname,email) VALUES (%s,%s,%s,%s,%s,%s)'''
        with self.connection.cursor() as cursor:
            cursor.execute(stmt,dataset)
            self.connection.commit()
    
    def removeUser(self,username):
        """
        Remove a user by username.

        """
        dataset = (username,)
        stmt = '''DELETE FROM UserInfo WHERE username = %s'''
        with self.connection.cursor() as cursor:
            cursor.execute(stmt,dataset)
            self.connection.commit()
    
    def getInfo(self,username):
        """
        Get all the information by a specific username.

        """
        result = list()
        stmt = "SELECT * from UserInfo where username = %s"
        dataset = (username,)
        with self.connection.cursor() as cursor:
            cursor.execute(stmt,dataset)
            for row in cursor.fetchall():
                for i in row:
                    result.append(i)
        return result
            
    def checkUsername(self,username):
        """
        Check whether the username already exists in the database.

        """
        if self.getInfo(username):
            return True
        return False

if __name__ == "__main__":
    localdb().createTable()

