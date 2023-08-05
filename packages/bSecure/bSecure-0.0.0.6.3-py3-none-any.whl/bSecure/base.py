# __author__ = 'sadaqatullah'

from bSecure.helpers.constants import constants
from bSecure.authentication.builder_authentication import Authentication
from bSecure.authentication.single_sign_on import SingleSignOn
from bSecure.buttons.buttons import Button
from bSecure.order_management.order_management import Order


class CustomIntegration:
    """

    """

    def __init__(self):
        self.authenticator = Authentication()
        self.sso = SingleSignOn()
        self.order = Order()
        self.buttons = Button()

    def authenticate_builder(self, client_id, client_secret):
        credentials = {
            constants.get_key_client_id(): client_id,
            constants.get_key_client_secret(): client_secret,
            "extra_args": {

            }
        }
        self.authenticator.set_credentials(**credentials)
        if self.authenticator.is_valid():
            if not self.authenticator.is_authenticated():
                self.authenticator.authenticate()
                if self.authenticator.is_authenticated():
                    return "Login Successful"
            else:
                return 'Already LoggedIn'
        return "Invalid Credentials"

    def single_sign_on_set_values(self, **kwargs):
        self.sso.set_credentials(**kwargs)
        return self.sso.is_valid()

    def single_sign_on(self):
        return self.sso.sso_redirect_url()

    def get_sso_customer_profile(self, state='', code=''):
        self.authenticator.set_header()
        self.sso.set_sso_credentials_for_customer_profile(code=code, state=state,
                                                          header=self.authenticator.get_header())
        return self.sso.get_customer_profile()

    def get_sso_login_button(self):
        return self.buttons.get_sso_button_image_url()

    def set_order(self, order_details):

        self.authenticator.set_header()
        return self.order.set_order(
            order_details=order_details,
            header=getattr(self.authenticator, constants.get_key_header())
        )

    def create_order(self):
        return self.order.create_order()

    def status_order(self, order_reference=''):
        if not order_reference or len(order_reference) == 0:
            return "reference_id is required field"
        return self.order.status_order(order_reference=order_reference)

    def get_checkout_button(self):
        return self.buttons.get_checkout_button_image_url()


# Instantiate a Singleton
custom_integration = CustomIntegration()

# Assigning values of Singleton to variables
authenticate = custom_integration.authenticate_builder
set_order = custom_integration.set_order
create_order = custom_integration.create_order
order_status = custom_integration.status_order

customer_authenticator = custom_integration.single_sign_on
single_sign_on_set_values = custom_integration.single_sign_on_set_values
get_customer_profile = custom_integration.get_sso_customer_profile

checkout_button_image = custom_integration.get_checkout_button
sso_login_button_image = custom_integration.get_sso_login_button
