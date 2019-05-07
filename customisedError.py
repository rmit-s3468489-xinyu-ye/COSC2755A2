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
        return "The user name must start with letters, you just \
can use '_', letters, numbers for creating the user name!"

class UsernameLengthError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "The minimum user name length is 3 and the maximum lenth is 100!"

class InvalidNameError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "The name must start with letters, you just \
can use '_', letters for creating a name!"

class NameLengthError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "The name can not be empty and the maximum length is 100!"

class InvalidEmailError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Please enter a valid email address!"

class DuplicatedUsernameError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "This user name has been already registered!"

class UsernameError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Wrong user name"

class PasswordError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Wrong password"