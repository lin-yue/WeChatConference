# -*- coding: utf-8 -*-
#



__author__ = "Epsirom"


class BaseError(Exception):

    def __init__(self, code, msg):
        super(BaseError, self).__init__(msg)
        self.code = code
        self.msg = msg

    def __repr__(self):
        return '[ERRCODE=%d] %s' % (self.code, self.msg)


class InputError(BaseError):

    def __init__(self, msg):
        super(InputError, self).__init__(1, msg)


class LogicError(BaseError):

    def __init__(self, msg):
        super(LogicError, self).__init__(2, msg)


class ValidateError(BaseError):

    def __init__(self, msg):
        super(ValidateError, self).__init__(3, msg)

class InterfaceError(BaseError):

    def __init__(self, msg):
        super(InterfaceError, self).__init__(4, msg)

class ModuleListIsNullError(BaseError):
    def __init__(self, msg):
        super(ModuleListIsNullError, self).__init__(5, msg)

class SignedUpError(BaseError):
    def __init__(self, msg):
        super(SignedUpError, self).__init__(6, msg)

class LoginError(BaseError):
    def __init__(self, msg):
        super(LoginError, self).__init__(7, msg)

class LogoutError(BaseError):
    def __init__(self, msg):
        super(LogoutError, self).__init__(8, msg)