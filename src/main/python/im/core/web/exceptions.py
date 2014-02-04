from im.core.exceptions import GenericException

class WebException(GenericException):
     def __init__(self, message, code=None, loglevel=None):
        GenericException.__init__(self, message, code, loglevel)

class Error400(WebException):
    def __init__(self, message="Bad Request, The request had bad syntax or was impossible to be satisified.", code=400, loglevel="error"):
        WebException.__init__(self, message, code, loglevel)

class Error401(WebException):
    def __init__(self, message="Unauthorized, User failed to provide a valid user name / password required for access to file / directory.", code=401, loglevel="error"):
        WebException.__init__(self, message, code, loglevel)

class Error403(WebException):
    def __init__(self, message="Forbidden, The request does not specify the file name. Or the directory or the file does not have the permission that allows the pages to be viewed from the web.", code=403, loglevel="error"):
        WebException.__init__(self, message, code, loglevel)

class Error404(WebException):
    def __init__(self, message="Not Found, The requested file was not found.", code=404, loglevel="error"):
        WebException.__init__(self, message, code, loglevel)
        
class Error500(WebException):
    def __init__(self, message="Server Error, In most cases, this error is a result of a problem with the code or program you are calling rather than with the web server itself.", code=500, loglevel="error"):
        WebException.__init__(self, message, code, loglevel)

class Error501(WebException):
    def __init__(self, message="Not Implemented The server does not support the facility required.", code=501, loglevel="error"):
        WebException.__init__(self, message, code, loglevel)

