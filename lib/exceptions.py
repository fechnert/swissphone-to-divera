class BaseError(Exception):
    pass


class ValidationError(BaseError):
    pass


class ReadTimeout(BaseError):
    pass
