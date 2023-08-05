# __author__ = 'sadaqatullah'

from json import dumps, loads
from requests import post
from bSecure.helpers.constants import constants


class SingleSignOn:
    def set_credentials(self, client_id=None, scope='profile', response_type='code', state=None, header=None):
        setattr(self, constants.get_key_client_id(), client_id)
        setattr(self, constants.get_key_scope(), scope)
        setattr(self, constants.get_key_response_type(), response_type)
        setattr(self, constants.get_key_state(), state)

        setattr(self, constants.get_key_header(), header)

    def is_valid(self):
        _id = getattr(self, constants.get_key_client_id())
        _scope = getattr(self, constants.get_key_scope())
        _response_type = getattr(self, constants.get_key_response_type())
        _state = getattr(self, constants.get_key_state())

        if _id \
                and _scope \
                and _response_type \
                and _state \
                and type(_id) is str and \
                type(_state) is str:
            return True
        return False

    def sso_redirect_url(self):
        url = constants.get_authenticate_single_signon_url()
        url += "?{client_id_key}={client_id_value}".format(
            client_id_key=constants.get_key_client_id(),
            client_id_value=getattr(self, constants.get_key_client_id()),
        )
        url += "&{scope_key}={scope_value}".format(
            scope_key=constants.get_key_scope(),
            scope_value=getattr(self, constants.get_key_scope()),
        )
        url += "&{response_type_key}={response_type_value}".format(
            response_type_key=constants.get_key_response_type(),
            response_type_value=getattr(self, constants.get_key_response_type()),
        )
        url += "&{state_key}={state_value}"
        redirect_url = url.format(
            state_key=constants.get_key_state(),
            state_value=getattr(self, constants.get_key_state()),
        )
        return redirect_url

    def set_sso_credentials_for_customer_profile(self, header={}, state=None, code=None):
        if not header or not state or not code:
            return 'header and state are required fields'

        if type(header) is not dict:
            return 'header type should be dictionary'

        setattr(self, constants.get_key_header(), header)
        setattr(self, constants.get_key_state(), state)
        setattr(self, constants.get_key_code(), code)

    def get_customer_profile(self):
        url = constants.get_customer_profile_url()
        data = {
            constants.get_key_code(): getattr(self, constants.get_key_code())
        }
        response = post(url=url,
                        data=dumps(data),
                        headers=getattr(self, constants.get_key_header()))
        content = response.content
        return loads(content).get('body')
