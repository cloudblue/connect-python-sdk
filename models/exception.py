from .schema import ServerError


class Message(Exception):
    def __init__(self, message='', code='', obj=None):
        self.message = message
        self.code = code
        self.obj = obj


class FulfillmentFail(Message):
    def __init__(self, *args, **kwargs):
        self.message = 'Request failed'
        self.code = 'fail'


class FulfillmentInquire(Message):
    def __init__(self, *args, **kwargs):
        self.message = kwargs.get('message') or 'Correct user input required'
        self.params = kwargs.get('params', [])
        self.code = 'inquire'


class Skip(Message):
    def __init__(self, *args, **kwargs):
        self.code = 'skip'


class ServerErrorException(Exception):
    def __init__(self, error=None, *args, **kwargs):
        super(ServerErrorException, self).__init__(*args, **kwargs)

        if error and isinstance(error, ServerError):
            self.message = str({
                "error_code": error.error_code,
                "params": error.params,
                "errors": error.errors,
            })
