import re
from enum import Enum

class AuthStatus(Enum):
    Valid = 1
    BadUsername = 2
    PasswordTooWeak = 3
    PasswordsNotMatch = 4
    EmailNotValid = 5
    EmptyLogin = 6
    EmptyPassword = 7
    EmptyConfirmed = 8
    EmptyEmail = 9

class LocalAuth:
    MAX_LOGIN_LEN = 16
    MAX_PASSWD_LED = 16
    MAX_EMAIL_LEN = 22

    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    LOGIN_PATTERN = "^(?=.{3,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"
    PASSWD_PATTERN = "[A-Za-z0-9@#$%^&+=]{6,}"

    @staticmethod
    def validate_signup_form(username: str, password: str, confirmed: str, email: str) -> AuthStatus:
        #if username == "":
        #    return AuthStatus.EmptyLogin
        #elif password == "":
        #    return AuthStatus.EmptyPassword
        #elif confirmed == "":
        #    return AuthStatus.EmptyConfirmed
        #elif email == "":
        #    return AuthStatus.EmptyEmail
        if not LocalAuth._test_login(username):
            return AuthStatus.BadUsername
        elif not LocalAuth._test_password(password):
            return AuthStatus.PasswordTooWeak
        elif not LocalAuth._test_confirmed_passsword(password,confirmed):
            return AuthStatus.PasswordsNotMatch
        elif not LocalAuth._test_email(email):
            return AuthStatus.EmailNotValid
        else:
            return AuthStatus.Valid

    @staticmethod
    def _test_login(login: str) -> bool:
        pattern = re.compile(LocalAuth.LOGIN_PATTERN)
        if not re.match(pattern, login):
            return False
        else:
            return True

    @staticmethod
    def _test_email(email: str) -> bool:
        pattern = re.compile(LocalAuth.EMAIL_PATTERN)
        if not re.match(pattern, email):
            return False
        else:
            return True

    @staticmethod
    def _test_password(password: str) -> bool:
        pattern = re.compile(LocalAuth.PASSWD_PATTERN)
        if not re.match(pattern, password):
            return False
        else:
            return True

    @staticmethod
    def _test_confirmed_passsword(password: str, confirmed: str) -> bool:
        return password == confirmed

