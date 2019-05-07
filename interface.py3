from database_scheme import DatabaseScheme
from validation_scheme import ValidationScheme
from passlib.hash import sha256_crypt


class Menu:
    def __init__(self):
        self.validateInstance=ValidationScheme()

    def main(self):
        with DatabaseScheme() as db:
            db.createUsersTable()
        self.displayMenu()
        
    def displayMenu(self):
        while(True):
            print()
            print("1. Register a new user")
            print("2. Login")
            print("3. Exit")
            selection = input("Please select an operation: ")
            print()
            if(selection == "1"):
                self.registerUser()
            elif(selection == "2"):
                self.login()
            elif(selection == "3"):
                exit("Exited successfully.")
            else:
                print("Invalid selection - please try again.")

    def registerUser(self):
        print("**** Register a New User ****")
        with DatabaseScheme() as db:
            
            username=self.inputUsername("Please input the username: ")
            password=self.hashPassword(self.inputPassword("Please input the password: "))
            firstname=self.inputName("Please input the first name for the user: ")    
            lastname=self.inputName("Please input the last name for the user: ")
            email=self.inputEmail()
            
            #save all input data to a tuple
            inputData = (username, password, firstname, lastname, email)
            
            if(db.insertNewUser(inputData)==True):
                print("Registered as {} successfully.".format(username))
            else:
                print("User {} already exists. Failed to register. ".format(username))

    def inputUsername(self,para):
        username = input("Please enter the username {}: (Back to main menu->'-')".format(para))
        
        self.backToMainMenu(username)
        
    def checkLetterNumberInput(self,formalPara,input):
        if self.validateInstance.detectNullInput("username",username) == False or self.validateInstance.detectSpaceInput("username",username) == False or self.validateInstance.checkLetterNumberInput("username",username) == False:
            self.inputUsername(para)
        return username

    def inputPassword(self,para):
        password = input("Enter the {} password (Back to main menu->'-'): ".format(para))
        
        self.backToMainMenu(password)
        if self.validateInstance.detectNullInput("password",password) == False or self.validateInstance.detectSpaceInput("password",password) == False:
            self.inputPassword(para)
        return password

    def inputName(self,para):
        temp = input("Enter the new user's {} (Back to main menu->'-'): ".format(para))
        
        self.backToMainMenu(temp)
        print("test", self.validateInstance.checkLetterInput(para,temp))
        if self.validateInstance.detectNullInput(para,temp) == False or self.validateInstance.detectSpaceInput(para,temp) == False or self.validateInstance.checkLetterInput(para,temp) == False:
            self.inputName(para)
        return temp

    def inputEmail(self):
        email = input("Please enter the new user's email address (Back to main menu->'-'): ")
        
        self.backToMainMenu(email)
        if self.validateInstance.detectNullInput("Email Address",email) == False or self.validateInstance.detectSpaceInput("Email Address",email) == False or self.validateInstance.verifyEmail("Email Address",email) == False:
               self.inputEmail()
        return email

    def hashPassword(self, pwd):
        
        hashedPassword = sha256_crypt.hash(pwd)
        
        return hashedPassword

    def backToMainMenu(self,index):
        if(index == "-"):
            self.displayMenu()

    def login(self):
        print("**** Login ****")
        username=self.inputUsername("Please enter the username")
        password=self.inputPassword("Please enter the password")
       
        #save all input data into a tuple
        inputData = (username)
        
        with DatabaseScheme() as db:
            hashedPassword=db.searchUser(inputData)
            if(hashedPassword !=None):        
                hashPassword=hashedPassword[0]
                if(sha256_crypt.verify(password, hashPassword)):
                    print("Logined as {} sucessfully.".format(username))               
                else:
                    print("{}'s password is incorrect, failed to login".format(username))
            else:
                print("{} does not exist.Failed to login".format(username))

if __name__ == "__main__":
Menu().main()