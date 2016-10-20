#!/usr/bin/env python
# coding: utf-8


class FieldTypes(object):
    # No type; just leave it
    NONE = 0

    # A standard string
    STR = 1

    # A standard integer
    INT = 2

    # A standard boolean
    BOOL = 3

    # An integer which is wrapped in quotes to/from the Opsview API
    INT_STR = 4

    # A boolean value represented as either '0' or '1' (quoted) to/from the API
    BOOL_INT_STR = 5

    # A single ref as a dict
    REF = 6

    # A list of references in the format {'name': ?, 'ref': /?}
    REF_LIST = 7


class FieldAttributes(object):
    # Remove fields with value 'None'
    OMIT_NONE = (
        int('000001', 2))

    # Remove empty strings. Implies OMIT_NONE.
    OMIT_EMPTY = (
        int('000010', 2))

    # Cannot be changed on creation or update; e.g. 'uncommitted' or 'id'
    READONLY = (
        int('000100', 2))

    # Can only be set during creation. Updates cannot change this value
    READONLY_UPDATE = (
        int('001000', 2))
