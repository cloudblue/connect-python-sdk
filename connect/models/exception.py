from .server_error import ServerError


class Message(Exception):
    def __init__(self, message='', code='', obj=None):
        self.message = message
        self.code = code
        self.obj = obj


class FulfillmentFail(Message):
    def __init__(self, *args, **kwargs):
        super(FulfillmentFail, self).__init__(*args, **kwargs)
        self.code = 'fail'
        self.message = self.message or 'Request failed'


class FulfillmentInquire(Message):
    def __init__(self, *args, **kwargs):
        super(FulfillmentInquire, self).__init__(*args, **kwargs)
        self.message = self.message or 'Correct user input required'
        self.params = kwargs.get('params', [])
        self.code = 'inquire'


class Skip(Message):
    def __init__(self, *args, **kwargs):
        self.code = 'skip'


class ServerErrorException(Exception):
    message = 'Server error'

    def __init__(self, error=None, *args, **kwargs):
        if error and isinstance(error, ServerError):
            self.message = str({
                "error_code": error.error_code,
                "params": kwargs.get('params', []),
                "errors": error.errors,
            })

        super(ServerErrorException, self).__init__(
            self.message, *args, **kwargs)
