class YextException(Exception):
    pass

class RequestException(YextException):

    def __init__(self, message, status, codes):
        super(YextException, self).__init__(message)
        self.status = status
        self.codes = codes
