"""Miscellaneous (catch all) tools Copyright 2020 Caliber Data Labs."""

#  Copyright (c) 2020 Caliber Data Labs.
#  All rights reserved.
#

import uuid


def decorate_all_inherited_methods(decorator):
    """Add a decorator to all methods which are not private.

    Usage:
        @decorate_all_inherited_methods(decorator)
        class C(object):
            def m1(self): pass
            def m2(self, x): pass
    ...
    """

    def decorate(cls):
        for attr in dir(cls):
            # Only callable methods and those that don't start with _ are
            # eligible
            if callable(getattr(cls, attr)) and not attr.startswith("_"):
                # Only inherited or overrided methods are eligible
                if attr not in cls.__dict__ or hasattr(super(cls), attr):
                    setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


def chunk_list(list_elements, chunk_size):
    """Chunks a list into chunk_size chunks, with last chunk the remaining
    elements.

    :param list_elements:
    :param chunk_size:
    :return:
    """
    chunks = []
    while True:
        if len(list_elements) > chunk_size:
            chunk = list_elements[0:chunk_size]
            list_elements = list_elements[chunk_size:]
            chunks.append(chunk)
        else:
            chunks.append(list_elements)
            break
    return chunks


def as_bool(s):
    if s is None:
        return False

    if isinstance(s, bool):
        return s
    else:
        s = str(s)  # In Python 2, handle case when s is unicode
        if s.lower() in {"t", "true"}:
            return True
        elif s.lower() in {"f", "false"}:
            return False
        else:
            raise ValueError(
                "Input of type ::: {} cannot be converted to bool ::: {}".format(
                    type(s), s))


def get_truncated_uid(n: int = 5):
    return get_guid()[0:n]


def get_guid():
    return str(uuid.uuid4())
