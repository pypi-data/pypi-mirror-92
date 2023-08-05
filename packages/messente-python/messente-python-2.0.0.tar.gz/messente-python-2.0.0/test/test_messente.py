# -*- coding: utf-8 -*-

import unittest

from messente.api.sms import Messente
from messente.api.sms.api.api import API
from messente.api.sms.api.credit import CreditAPI
from messente.api.sms.api.delivery import DeliveryAPI
from messente.api.sms.api.error import ConfigurationError, ERROR_CODES
from messente.api.sms.api.pricing import PricingAPI
from messente.api.sms.api.sms import SmsAPI


class TestMessenteLibrary(unittest.TestCase):
    def test_invalid_config_path(self):
        with self.assertRaises(ConfigurationError):
            Messente(
                ini_path="invalid-path.ini",
                urls="https://test-messente.example.com"
            )

    def test_modules_init(self):
        api = Messente(urls="https://test.example.com")
        self.assertIsInstance(api.sms, SmsAPI)
        self.assertIsInstance(api.credit, CreditAPI)
        self.assertIsInstance(api.delivery, DeliveryAPI)
        self.assertIsInstance(api.pricing, PricingAPI)
        apis = [api.sms, api.credit, api.delivery, api.pricing]
        for item in apis:
            self.assertIsInstance(item, API)
        del api

    def test_error_messages(self):
        codes = ERROR_CODES
        self.assertGreater(len(codes), 0)
        for c in codes:
            self.assertGreater(len(codes[c]), 0)
