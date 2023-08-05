# __author__ = 'sadaqatullah'
from datetime import datetime
from json import loads, dumps
from requests import post
from bSecure.authentication.exceptions import AuthenticationFailedException
from bSecure.helpers.constants import constants
from bSecure.helpers.utils import dict_to_object_properties


class Authentication:

    def set_credentials(self, client_id=None, client_secret=None, auth_id=None, **kwargs):
        setattr(self, constants.get_key_client_id(), client_id)
        setattr(self, constants.get_key_client_secret(), client_secret)
        setattr(self, constants.get_key_extra_args(), kwargs)

    def is_valid(self):
        _id = getattr(self, constants.get_key_client_id())
        _secret = getattr(self, constants.get_key_client_secret())

        if _id and _secret and \
                type(_id) is str and \
                type(_secret) is str:
            return True
        raise

    def authenticate(self):
        data = {
            constants.get_key_grant_type(): constants.get_value_default_grant_type(),
            constants.get_key_client_id(): getattr(self, constants.get_key_client_id()),
            constants.get_key_client_secret(): getattr(self, constants.get_key_client_secret())
        }
        url = constants.get_authentication_url()
        _request = post(
            url=url,
            data=dumps(data),
            headers={
                'content-type': 'application/json'
            }
        )
        response_body = loads(_request.content)

        if response_body.get(constants.key_status, 0) == 200 \
                and not response_body.get(constants.key_exception, True):
            print(response_body)
            dict_to_object_properties(self, response_body)
        else:
            raise AuthenticationFailedException(msg="")

    def is_authenticated(self):
        if hasattr(self, constants.key_token_type) and getattr(self, constants.key_token_type) == \
                constants.get_value_token_type() and getattr(self, constants.key_expires_in) > datetime.now():
            return True
        return False

    def set_header(self):
        access_token = '{token_type} {access_token}'.format(
            token_type=getattr(self, constants.key_token_type),
            access_token=getattr(self, constants.get_key_access_token())
        )
        header = {
            "Authorization": access_token,
            'content-type': 'application/json',
        }
        setattr(self, constants.get_key_header(), header)

    def get_header(self):
        if hasattr(self, constants.get_key_header()):
            return getattr(self, constants.get_key_header())
        return 'No header key determined'
