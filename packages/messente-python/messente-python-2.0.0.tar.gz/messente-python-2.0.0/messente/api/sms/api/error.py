# -*- coding: utf-8 -*-

# Copyright 2016 Messente Communications OÜ
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


class MessenteError(Exception):
    pass


class ConfigurationError(MessenteError):
    pass


class ApiError(MessenteError):
    pass


class InvalidMessageError(MessenteError):
    pass


ERROR_CODES = {
    "ERROR 101": " ".join([
        "Access is restricted, wrong credentials.",
        "Check the username and password values.",
    ]),
    "ERROR 102": " ".join([
        "Parameters are wrong or missing.",
        "Check that all the required parameters are present.",
    ]),
    "ERROR 103": " ".join([
        "Invalid IP address.",
        "The IP address you made the request from,",
        "is not in the API whitelist settings.",
    ]),
    "FAILED 209": " ".join([
        "Server failure, try again after a few seconds or",
        "try the backup server.",
    ]),
}
