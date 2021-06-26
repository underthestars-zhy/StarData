class Error:
    _type = 'error'

    def __init__(self, message):
        self.message = message
        self.type = self._type


class ValidationError(Error):
    _type = 'validation error'


class InsertError(Error):
    _type = 'insert error'
