# Copyright 2020 h3xcode
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Misc utils"""

import sys


def _after_proxy_getobj(r_name_, object_name):
    """Get object from module"""
    return getattr(sys.modules[r_name_], object_name) if object_name else None


def convert_builtin_to_class(builtin_name):
    """Converts SOMETHING_SHITTY_TEXT to SomethingShittyText"""
    return "".join(
        map(lambda x: x.capitalize(), builtin_name.lower().split("_"))) if builtin_name else None


def make_getobj(r_name_):
    """Proxy for getobj"""
    return lambda object_name: _after_proxy_getobj(r_name_, object_name)


def reverse_get(dict_, value):
    """Get key by value from dict"""
    try:
        return list(dict_.keys())[list(dict_.values()).index(value)]
    except ValueError:
        return None
    return None


def deep_err_search(dict_, value):
    """Deeper error search. Should be used if reverse_get fails"""
    if isinstance(value, (tuple, list)):
        for key, val in dict_.items():
            if val[0] == value[0]:
                return key
    if isinstance(value, int):
        for key, val in dict_.items():
            if val[0] == value:
                return key
    return None


def raise_if_flag(exc, flag):
    """Raise exception if exc is not None or False and if flag is True"""
    if exc and flag:
        raise exc
