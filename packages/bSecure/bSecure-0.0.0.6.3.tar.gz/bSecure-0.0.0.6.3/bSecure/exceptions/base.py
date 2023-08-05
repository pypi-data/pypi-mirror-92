# __author__ = 'sadaqatullah'

class BaseBSecureException(Exception):
    """
    This exception will be treated as base to all exceptions required by bSecure
    Python SDK. This must not be raised directly to maintain verbosity of Exceptions.
    """

    def __init__(self, msg):
        # return msg
        ...
