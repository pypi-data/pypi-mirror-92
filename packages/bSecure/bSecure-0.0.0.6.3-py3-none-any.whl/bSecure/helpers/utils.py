# __author__ = 'sadaqatullah'

import datetime
from bSecure.helpers.constants import constants


def dict_to_object_properties(obj, dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            dict_to_object_properties(obj, value)
        else:
            if key == constants.key_expires_in:
                t = datetime.datetime.now() + datetime.timedelta(seconds=value)
                setattr(obj, key, t)
            else:
                setattr(obj, key, value)
    return obj
