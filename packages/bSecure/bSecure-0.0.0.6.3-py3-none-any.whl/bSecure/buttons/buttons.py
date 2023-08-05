"""
created by: Sadaqatullah Noonari
date: 12/30/20
"""

from bSecure.helpers.constants import constants


class Button:
    """
    This class holds buttons for bSecure.
    """

    @classmethod
    def get_checkout_button_image_url(cls):
        return constants.get_checkout_button_url()

    @classmethod
    def get_sso_button_image_url(cls):
        return constants.get_sso_button_url()

