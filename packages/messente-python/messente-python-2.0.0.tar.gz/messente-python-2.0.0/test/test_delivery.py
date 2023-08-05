# -*- coding: utf-8 -*-

import responses

from messente.api.sms.api import Response
from messente.api.sms.api import delivery
from test import utils

api = delivery.DeliveryAPI(urls=utils.TEST_DLR_URL)


@responses.activate
def test_dlr():
    status = "DELIVERED"
    text = "OK %s" % status
    responses.add_callback(
        responses.GET, utils.TEST_DLR_ANY_URL,
        callback=utils.mock_response(200, text),
    )

    r = api.get_dlr_response("smsid")
    assert isinstance(r, Response)
    assert isinstance(r, delivery.DeliveryResponse)
    assert r.get_raw_text() == text
    assert r.get_result() == "DELIVERED"


@responses.activate
def test_dlr_failed():
    text = "FAILED 102"
    responses.add_callback(
        responses.GET, utils.TEST_DLR_ANY_URL,
        callback=utils.mock_response(200, text),
    )

    r = api.get_dlr_response("smsid")
    assert isinstance(r, Response)
    assert isinstance(r, delivery.DeliveryResponse)
    assert r.get_result() == ""
    assert not r.is_ok()
