"""
this module is customized error
"""
class PasswordsInconsistentError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Those passwords didn't match. Try again!"

class InvalidPasswordError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Your password must contain at least one \
uppercase letter, one lowercase letter, one number \
and one special character!"

class PasswordTooShortError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "The minimum password length is 6!"

class InvalidUsernameError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "The user name must start with letters, you can \
only use '_', letters, numbers for the user name!"

class UsernameLengthError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "The minimum length of a username  is 3 and the maximum is 100!"

class InvalidNameError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "The name must start with letters, you can \
only use '_', letters for creating a name!"

class NameLengthError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "The name field cannot be empty and the maximum length is 100!"

class InvalidEmailError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Please enter a valid email address!"

class DuplicatedUsernameError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "This username has already been registered!"

class UsernameError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Wrong username"

class PasswordError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Wrong password"

class InvalidOptionError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Invalid option, please select again!"
class UserNotFoundError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Cannot find the user, please type again!"

class InvalidInputFormatError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Your input is invalid, please type again!"
class BorrowedFailedError(Exception):
    def __init__(self,message):
        self.message = message
