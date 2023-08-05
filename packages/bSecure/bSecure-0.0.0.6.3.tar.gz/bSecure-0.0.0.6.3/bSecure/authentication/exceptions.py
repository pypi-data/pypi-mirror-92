# __author__ = 'sadaqatullah'

from bSecure.exceptions.base import BaseBSecureException


class BaseAuthenticationException(BaseBSecureException):
    """
    This works as base to all exceptions related to Authentications. This can be overwritten
    to allow for new type for exceptions related to authentications. Furthermore, this exception
    shall only be called when no other exception is present to maintain verbosity.
    """
    ...


class ValidationError(BaseAuthenticationException):
    """

    """
    ...


class AuthenticationFailedException(BaseAuthenticationException):
    """
    Raised only when Authentication API returns
    """
    ...


class WrongStatusValueException(BaseAuthenticationException):
    ...
