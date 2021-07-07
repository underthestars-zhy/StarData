class Error:
    _type = 'error'

    def __init__(self, message):
        self.message = message
        self.type = self._type


class ValidationError(Error):
    _type = 'validation error'


class InsertError(Error):
    _type = 'insert error'


class UpdateError(Error):
    _type = "update error"

class CreatDBError(Error):
    _type = "creat db error"
