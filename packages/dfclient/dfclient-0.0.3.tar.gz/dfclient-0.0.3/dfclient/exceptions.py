

class DataFinanceClientException(Exception):
    pass


class NotFound(DataFinanceClientException):
    pass


class ServerError(DataFinanceClientException):
    pass

