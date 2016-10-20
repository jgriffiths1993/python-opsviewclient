#!/usr/bin/env python
# coding: utf-8


import six
from opsviewclient.fields import(
    FieldAttributes as FA,
    FieldTypes as FT
)


def to_string(value):
    try:  # Python 2
        return unicode(value)
    except NameError:  # Python 3
        return str(value)


def to_bool(value):  # raises ValueError if not a valid bool value
    if isinstance(value, six.string_types):
        value = int(value)

    return bool(value)


def to_int(value):
    return int(value)


def to_bool_int_str(value):
    if isinstance(value, six.string_types):
        return value

    if value:
        return "1"

    return "0"


def do_nothing(value):
    return value


class FieldEncoding(object):

    def __init__(self, encode, decode):
        self._encode = encode
        self._decode = decode

    def encode(self, value):
        if value is None:
            return None

        return self._encode(value)

    def decode(self, value):
        if value is None:
            return None

        return self._decode(value)


field_encodings = {
    FT.NONE: FieldEncoding(encode=do_nothing, decode=do_nothing),
    FT.STR: FieldEncoding(encode=to_string, decode=to_string),
    FT.BOOL: FieldEncoding(encode=to_bool, decode=to_bool),
    FT.BOOL_INT_STR: FieldEncoding(encode=to_bool_int_str, decode=to_bool),
    FT.INT: FieldEncoding(encode=to_int, decode=to_int),
    FT.INT_STR: FieldEncoding(encode=to_string, decode=to_int),
    FT.REF: FieldEncoding(encode=do_nothing, decode=do_nothing),
    FT.REF_LIST: FieldEncoding(encode=do_nothing, decode=do_nothing),
}
