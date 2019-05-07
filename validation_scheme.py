import re

class ValidationScheme:

    def detectNullInput(self,formalPara,input):
        #detect whether the input is null
        if len(input) == 0:
            print("Input {} cannot be null.".format(formalPara))
            return False
        return True

    def detectSpaceInput(self,formalPara,input):
        #detect whether the input is blank space
        if input.isspace() == True:
            print("Input {} cannot be blank.".format(formalPara))
            return False
        return True

    def checkLetterNumberInput(self,formalPara,input):
        #check whether the input is any letter or number
        if input.isalnum() == False:
            print("Input {} is only allowed to be any letter or number.".format(formalPara))
            return False
        return True

    def checkLetterInput(self,formalPara,input):
        #check whether the input is any letter
        if input.isalpha() == False:
            print("{} can only be any letter.".format(formalPara))
            return False
        return True

    def verifyEmail(self,formalPara,input):
        #validate the format of email input
        reEmail = re.compile(r'^[a-zA-Z\.]+@[a-zA-Z0-9]+\.[a-zA-Z]{3}$')
        if reEmail.match(input) == None:
            print("{} format is invalid.".format(formalPara))
            return False
        return True
        