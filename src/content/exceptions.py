class BaseAppException(Exception):
    """Common base class for all app exception"""


class ValidationDataError(BaseAppException):
    pass


class InternalNetworkConnectionError(BaseAppException):
    pass
