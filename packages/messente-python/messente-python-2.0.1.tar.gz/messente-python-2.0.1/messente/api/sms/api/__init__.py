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

from messente.api.sms.api import error
from messente.api.sms.api.response import Response

# api modules
from messente.api.sms.api import sms
from messente.api.sms.api import credit
from messente.api.sms.api import delivery
from messente.api.sms.api import pricing
from messente.api.sms.api import number_verification
from messente.api.sms.api import verification_widget

__all__ = [
    "error",
    "Response",
    "sms",
    "credit",
    "delivery",
    "pricing",
    "number_verification",
    "verification_widget",
]
