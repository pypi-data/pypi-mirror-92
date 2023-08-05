# __author__ = Sadaqatullah Noonari

class Base:
    __base_url = 'https://api.bsecure.pk'
    __base_login_app_url = 'https://login.bsecure.pk'
    __key_grant_type = 'grant_type'
    __value_grant_type = 'client_credentials'

    key_extra_args = 'extra_args'
    value_extra_args = {}

    key_client_id = 'client_id'
    key_client_secret = 'client_secret'

    key_scope = 'scope'
    key_response_type = 'response_type'
    key_state = 'state'
    key_code = 'code'

    key_exception = 'exception'
    key_status = 'status'
    key_body = 'body'

    key_token_type = 'token_type'
    key_expires_in = 'expires_in'
    key_access_token = 'access_token'
    key_environment = 'environment'
    value_sandbox_environment = 'sandbox'
    value_live_environment = 'sandbox'
    value_token_type = 'Bearer'

    key_order_details = 'order_detials'
    key_header = 'header'

    @classmethod
    def get_key_access_token(cls):
        return cls.key_access_token

    @classmethod
    def get_base_url(cls):
        return cls.__base_url

    @classmethod
    def get_base_login_app_url(cls):
        return cls.__base_login_app_url

    @classmethod
    def get_key_client_id(cls):
        return cls.key_client_id

    @classmethod
    def get_key_client_secret(cls):
        return cls.key_client_secret

    @classmethod
    def get_key_extra_args(cls):
        return cls.key_extra_args

    @classmethod
    def get_value_default_extra_args(cls):
        return cls.value_extra_args

    @classmethod
    def get_key_grant_type(cls):
        return cls.__key_grant_type

    @classmethod
    def get_value_default_grant_type(cls):
        return cls.__value_grant_type

    @classmethod
    def get_key_token_type(cls):
        return cls.key_token_type

    @classmethod
    def get_value_token_type(cls):
        return cls.value_token_type

    @classmethod
    def get_key_scope(cls):
        return cls.key_scope

    @classmethod
    def get_key_response_type(cls):
        return cls.key_response_type

    @classmethod
    def get_key_state(cls):
        return cls.key_state


class Constants(Base):
    __authenticate_endpoint__ = '/v1/oauth/token'
    __authenticate_single_signon = '/v1/'
    __create_order_endpoint__ = '/v1/order/create'
    __update_order_endpoint__ = '/v1/order/update'
    __sso_login_endpoint = '/auth/sso'
    __sso_customer_profile = '/v1/sso/customer/profile'

    __checkout_button_url = 'http://bsecure-dev.s3-eu-west-1.amazonaws.com/dev/react_app/plugin/bsecure-checkout-img.svg'
    __sso_login_button_url = 'http://bsecure-dev.s3-eu-west-1.amazonaws.com/dev/react_app/plugin/login-with-bsecure.jpg'

    @classmethod
    def get_checkout_button_url(cls):
        return cls.__checkout_button_url

    @classmethod
    def get_key_code(cls):
        return cls.key_code

    @classmethod
    def get_sso_button_url(cls):
        return cls.__sso_login_button_url

    @classmethod
    def get_authentication_url(cls):
        return cls.get_base_url() + cls.__authenticate_endpoint__

    @classmethod
    def get_customer_profile_url(cls):
        return cls.get_base_url() + cls.__sso_customer_profile

    @classmethod
    def get_authenticate_single_signon_url(cls):
        return cls.get_base_login_app_url() + cls.__sso_login_endpoint

    @classmethod
    def get_create_order_url(cls):
        return cls.get_base_url() + cls.__create_order_endpoint__

    @classmethod
    def get_update_order_url(cls):
        return cls.get_base_url() + cls.__update_order_endpoint__

    @classmethod
    def get_key_header(cls):
        return cls.key_header

    @classmethod
    def get_key_order_details(cls):
        return cls.key_order_details


constants = Constants()
