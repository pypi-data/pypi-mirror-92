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

"""Working with errors"""

from . import utils, models

_builtin_errors = {
    "INTERNAL_SERVER_ERROR": (-32500, "Internal server error"),
    "TRANSACTION_PARSE_ERROR": (-32408, "Parse error")
}

INTERNAL_SERVER_ERROR = _builtin_errors["INTERNAL_SERVER_ERROR"]
TRANSACTION_PARSE_ERROR = _builtin_errors["TRANSACTION_PARSE_ERROR"]


class BionicError(BaseException):
    """Base class for Bionic errors"""
    ...


class InternalServerError(BionicError):
    """Internal server error. Similiar to HTTP 500"""

    def __init__(self):
        super().__init__(
            "An internal error occurred while processing a request\
             on the server that cannot be handled on the server or client")


class TransactionParseError(BionicError):
    """Data parsing error"""

    def __init__(self):
        super().__init__(
            "A transaction parsing error occurred on the server while processing a request")


class GenericBionicError(BionicError):
    """Any other error"""

    def __init__(self, error):
        self.error_code, self.error_message = None, None
        if isinstance(error, int):
            super().__init__("Error %i occured with no description" % (error))
            self.error_code = error
        elif isinstance(error, (tuple, list)):
            super().__init__("[Error %i]: %s" % error)
            self.error_code, self.error_message = error


getobj = utils.make_getobj(__name__)


def recognize_error(error):
    """Generate error object from tuple or int"""
    if isinstance(error, models.Error):
        error = (error.error_code, error.error_message)
    cls_ = getobj(utils.convert_builtin_to_class(utils.reverse_get(
        _builtin_errors, error) or utils.deep_err_search(_builtin_errors, error)))
    if cls_:
        return cls_
    return GenericBionicError(error)
