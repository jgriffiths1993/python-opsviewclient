#!/usr/bin/env python
# coding: utf-8

import copy
import six
from opsviewclient.fields import FieldAttributes as FA
from opsviewclient.conv import field_encodings


def get_id(obj):
    try:
        return obj.id
    except AttributeError:
        return obj


def id_from_ref(obj):
    if isinstance(obj, dict):
        obj = obj['ref']

    return obj.rsplit('/', 1)[-1]


def nameref(name):
    """Returns a reference to a name as {'name': name}"""
    if name is None:
        return None

    if isinstance(name, Resource) and hasattr(name, 'name'):
        return {'name': getattr(name, 'name')}

    if isinstance(name, dict) and 'name' in name:
        return name

    return {'name': name}


def fmt_str(val):
    """Returns the peculiar formats of data expected by most of the Opsview
    API
    """
    if isinstance(val, bool):
        return "%d" % val
    elif isinstance(val, int):
        return "%d" % val
    elif isinstance(val, str):
        return val
    elif val:
        return "%s" % val

    return None


class Resource(object):

    def __init__(self, manager, info, loaded=False):
        self.manager = manager
        self._info = info
        self._add_details(info)
        self._loaded = loaded

    def __repr__(self):
        reprkeys = sorted(k for k in self.__dict__.keys()
                          if k[0] != '_' and k not in ['manager'])

        info = ", ".join("%s=%s" % (k, getattr(self, k)) for k in reprkeys)
        return "<%s %s>" % (self.__class__.__name__, info)

    def is_loaded(self):
        return self._loaded

    def set_loaded(self, val):
        self._loaded = val

    def as_dict(self):
        return copy.deepcopy(self._info)

    def __eq__(self, other):
        if not isinstance(other, Resource):
            return NotImplemented

        if not isinstance(other, self.__class__):
            return False

        if hasattr(self, 'id') and hasattr(other, 'id'):
            return self.id == other.id

        return self._info == other._info

    def _add_details(self, info):
        info = self._decode(info)
        for (k, v) in six.iteritems(info):
            try:
                # setattr(self, k, v)
                self._info[k] = v
            except AttributeError:
                pass

    def copy(self):
        cpy = self.as_dict()
        return self.__class__(self.manager, info=cpy, loaded=True)

    def encoded(self):
        return self._encode(self.as_dict())

    def decoded(self):
        return self._decode(self.as_dict())

    @classmethod
    def _encode(cls, obj):
        fields = getattr(cls, '_fields_', None)
        field_attrs = getattr(cls, '_field_attributes_', None)

        if not fields and not field_attrs:
            return obj

        for (k, v) in six.iteritems(dict(obj)):
            if fields:
                if k in fields and fields[k] in field_encodings:
                    obj[k] = field_encodings[fields[k]].encode(v)

            if field_attrs:
                attrs = field_attrs.get(k, None)
                if not attrs:
                    continue

                if attrs & FA.OMIT_NONE == FA.OMIT_NONE:
                    if v is None:
                        del obj[k]

                if attrs & FA.OMIT_EMPTY == FA.OMIT_EMPTY:
                    if not v:
                        del obj[k]

                if attrs & FA.READONLY == FA.READONLY:
                    del obj[k]

        return obj

    @classmethod
    def _decode(cls, obj):
        fields = getattr(cls, '_fields_', None)

        if not fields:
            return obj

        for (k, v) in six.iteritems(obj):
            if k in fields and fields[k] in field_encodings:
                obj[k] = field_encodings[fields[k]].decode(v)

        return obj

    def __getattr__(self, k):
        keymap = None

        if '_field_map_' in self.__dict__:
            keymap = self.__dict__['_field_map_']

        if k in self.__dict__:
            return self.__dict__[k]

        if not self.is_loaded():
            self.get()
            return self.__getattr__(k)

        if k in self._info:
            return self._info[k]

        # Maybe we use a different name for the field than the Opsview API does
        # (e.g. to mask the API's inconsistent use of underscores)
        if keymap and k in keymap and keymap[k] in self._info:
            api_key = keymap[k]
            return self._info[api_key]

        raise AttributeError(k)

    def get(self):
        self.set_loaded(True)
        if not hasattr(self.manager, 'get'):
            return

        new = self.manager.get(self.id)
        if new:
            self._add_details(new._info)

    def delete(self):
        if not hasattr(self.manager, 'delete'):
            raise NotImplemented('Delete not implemented for type: %s' %
                                 self.__class__.__name__)

        return self.manager.delete(self)


class Manager(object):

    resource_class = None

    def __init__(self, api):
        self.api = api

    @property
    def client(self):
        return self.api

    def _list(self, url, obj_class=None):
        body = self.api.get(url)

        if obj_class is None:
            obj_class = self.resource_class

        data = body["list"]

        items = [obj_class(self, res, loaded=True) for res in data if res]

        return items

    def _get(self, url, params=None):
        body = self.api.get(url, params=params)

        return self.resource_class(self, body['object'], loaded=True)

    def _create(self, url, body, return_raw=False, params=None, **kwargs):
        body = self.api.post(url, data=body, params=params)

        if 'object' in body:
            body = body['object']
        elif 'list' in body:
            body = body['list']

        if return_raw:
            return body

        if isinstance(body, list):
            return [self.resource_class(self, o) for o in body]

        return self.resource_class(self, body)

    def _update(self, url, body, params=None, **kwargs):
        body = self.api.put(url, data=body, params=params)

        if 'object' in body:
            body = body['object']
        elif 'list' in body:
            body = body['list']

        if body:
            return self.resource_class(self, body)
        else:
            return body

    def _delete(self, url):
        body = self.api.delete(url)
        return body
