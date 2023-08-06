#!/usr/bin/env python
"""Tests for `broadworks_ocip` package."""
from collections import namedtuple

import pytest  # noqa: F401
from lxml import etree

from broadworks_ocip import BroadworksAPI

BASIC_API_PARAMS = {
    "host": "localhost",
    "username": "username@example.com",
    "password": "password",
    "session_id": "00000000-1111-2222-3333-444444444444",
}

api = BroadworksAPI(**BASIC_API_PARAMS)


def canon_xml(inxml):
    """
    we XML canonicalise/pretty print this to prevent whitespace/quote ordering
    issues and to make any diffs easier to read.
    Returned XML is as a decoded string - prettier for diffs
    """
    return etree.tostring(etree.fromstring(inxml), pretty_print=True).decode()


def check_command_xml(wanted, cmd):
    """Create a Broadworks XML command fragment from the arguments"""
    generated = cmd.build_xml_()
    assert canon_xml(generated) == canon_xml(wanted)


def compare_command_xml(wanted, command, **kwargs):
    """Create a Broadworks XML command fragment from the arguments"""
    cmd = api.get_command_object(command, **kwargs)
    check_command_xml(wanted, cmd)


def test_authentication_request_xml():
    compare_command_xml(
        (
            b'<?xml version="1.0" encoding="ISO-8859-1"?>\n'
            b'<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            b'<sessionId xmlns="">00000000-1111-2222-3333-444444444444</sessionId>'
            b'<command xmlns="" xsi:type="AuthenticationRequest">'
            b"<userId>username@example.com</userId></command></BroadsoftDocument>"
        ),
        "AuthenticationRequest",
        user_id="username@example.com",
    )


def test_error_response_xml():
    compare_command_xml(
        (
            b'<?xml version="1.0" encoding="ISO-8859-1"?>\n'
            b'<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            b'<sessionId xmlns="">00000000-1111-2222-3333-444444444444</sessionId>'
            b'<command type="Error" echo="" xsi:type="c:ErrorResponse" xmlns:c="C" xmlns="">'
            b"<summary>[Error 4962] Invalid password</summary>"
            b"<summaryEnglish>[Error 4962] Invalid password</summaryEnglish>"
            b"</command></BroadsoftDocument>"
        ),
        "ErrorResponse",
        summary="[Error 4962] Invalid password",
        summary_english="[Error 4962] Invalid password",
    )


def test_group_authorization_modify_xml():
    cmd = api.get_command_object(
        "GroupServiceModifyAuthorizationListRequest",
        service_provider_id="some_enterprise",
        group_id="somegroup",
        service_pack_authorization=[
            api.get_type_object(
                "ServicePackAuthorization",
                service_pack_name="Voicemail",
                authorized_quantity=api.get_type_object(
                    "UnboundedPositiveInt",
                    unlimited=True,
                ),
            ),
            api.get_type_object(
                "ServicePackAuthorization",
                service_pack_name="Hushmail",
                authorized_quantity=api.get_type_object(
                    "UnboundedPositiveInt",
                    quantity=32,
                ),
            ),
            api.get_type_object(
                "ServicePackAuthorization",
                service_pack_name="Phone",
                unauthorized=True,
            ),
        ],
    )
    check_command_xml(
        (
            b'<?xml version="1.0" encoding="ISO-8859-1"?>\n'
            b'<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            b'<sessionId xmlns="">00000000-1111-2222-3333-444444444444</sessionId>'
            b'<command xmlns="" xsi:type="GroupServiceModifyAuthorizationListRequest">'
            b"<serviceProviderId>some_enterprise</serviceProviderId>"
            b"<groupId>somegroup</groupId>"
            b"<servicePackAuthorization>"
            b"<servicePackName>Voicemail</servicePackName>"
            b"<authorizedQuantity><unlimited>true</unlimited></authorizedQuantity>"
            b"</servicePackAuthorization>"
            b"<servicePackAuthorization>"
            b"<servicePackName>Hushmail</servicePackName>"
            b"<authorizedQuantity><quantity>32</quantity></authorizedQuantity>"
            b"</servicePackAuthorization>"
            b"<servicePackAuthorization>"
            b"<servicePackName>Phone</servicePackName>"
            b"<unauthorized>true</unauthorized>"
            b"</servicePackAuthorization>"
            b"</command></BroadsoftDocument>"
        ),
        cmd,
    )


def test_service_provider_service_pack_get_detail_list_response_xml():
    type = namedtuple(
        "userServiceTable",
        ["service", "authorized", "allocated", "available"],
    )
    cmd = api.get_command_object(
        "ServiceProviderServicePackGetDetailListResponse",
        service_pack_name="Service-Pack-Standard",
        service_pack_description="Service Pack - Standard",
        is_available_for_use=True,
        service_pack_quantity=api.get_type_object(
            "UnboundedPositiveInt",
            unlimited=True,
        ),
        assigned_quantity=api.get_type_object(
            "UnboundedNonNegativeInt",
            unlimited=True,
        ),
        allowed_quantity=api.get_type_object("UnboundedPositiveInt", unlimited=True),
        user_service_table=[
            type(
                service="Call Center - Standard",
                authorized="Unlimited",
                allocated="Unlimited",
                available="Unlimited",
            ),
        ],
    )
    check_command_xml(
        (
            b'<?xml version="1.0" encoding="ISO-8859-1"?>\n'
            b'<BroadsoftDocument protocol="OCI" xmlns="C" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            b'<sessionId xmlns="">00000000-1111-2222-3333-444444444444</sessionId>'
            b'<command echo="" xsi:type="ServiceProviderServicePackGetDetailListResponse" xmlns="">'
            b"<servicePackName>Service-Pack-Standard</servicePackName>"
            b"<servicePackDescription>Service Pack - Standard</servicePackDescription>"
            b"<isAvailableForUse>true</isAvailableForUse>"
            b"<servicePackQuantity><unlimited>true</unlimited></servicePackQuantity>"
            b"<assignedQuantity><unlimited>true</unlimited></assignedQuantity>"
            b"<allowedQuantity><unlimited>true</unlimited></allowedQuantity>"
            b"<userServiceTable>"
            b"<colHeading>Service</colHeading>"
            b"<colHeading>Authorized</colHeading>"
            b"<colHeading>Allocated</colHeading>"
            b"<colHeading>Available</colHeading>"
            b"<row>"
            b"<col>Call Center - Standard</col>"
            b"<col>Unlimited</col>"
            b"<col>Unlimited</col>"
            b"<col>Unlimited</col>"
            b"</row>"
            b"</userServiceTable>"
            b"</command></BroadsoftDocument>"
        ),
        cmd,
    )


# end
