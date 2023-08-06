import pytest

from wtfix.conf import settings
from wtfix.core import utils
from wtfix.core.exceptions import TagNotFound, ValidationError
from wtfix.core.utils import GroupTemplateMixin
from wtfix.protocol.contextlib import connection, connection_manager


def test_find_tag_start_of_message(simple_encoded_msg):
    assert utils.index_tag(8, simple_encoded_msg) == (b"FIX.4.4", 0, 9)


def test_find_tag(simple_encoded_msg):
    assert utils.index_tag(9, simple_encoded_msg) == (b"5", 9, 13)


def test_find_tag_not_found_raises_exception(simple_encoded_msg):
    with pytest.raises(TagNotFound):
        utils.index_tag(123, simple_encoded_msg)


def test_rfind(simple_encoded_msg):
    assert utils.rindex_tag(10, simple_encoded_msg) == (b"163", 19, 25)


def test_checksum():
    assert (
        utils.calculate_checksum(
            b"8=FIXT.1.1\x019=75\x0135=A\x0134=1\x0149=ROFX\x0152=20170417-18:29:09.599\x0156=eco\x0198=0\x01"
            + b"108=20\x01141=Y\x011137=9\x01"
        )
        == 79
    )


def test_encode_str():
    assert utils.encode("abc") == b"abc"


def test_encode_int():
    assert utils.encode(123) == b"123"


def test_encode_bytes():
    assert utils.encode(b"abc") == b"abc"


def test_encode_bytearray():
    assert utils.encode(bytearray("abc", encoding="utf-8")) == b"abc"


def test_encode_none():
    assert utils.encode(None) == utils.encode(utils.null)


def test_encode_float():
    assert utils.encode(1.23) == b"1.23"


def test_encode_bool():
    assert utils.encode(True) == b"Y"
    assert utils.encode(False) == b"N"


def test_decode_bytes():
    assert utils.decode(b"abc") == "abc"


def test_decode_bytearray():
    assert utils.decode(bytearray("abc", encoding="utf-8")) == "abc"


def test_decode_str():
    assert utils.decode("abc") == "abc"


def test_decode_str_null():
    assert utils.decode(str(utils.null)) is None


def test_decode_int():
    assert utils.decode(123) == 123


def test_decode_int_null():
    assert utils.decode(utils.null) is None


def test_decode_none():
    assert utils.decode(None) is None


def test_decode_float():
    assert utils.decode(1.23) == 1.23


def test_is_null_str():
    assert utils.is_null("-2147483648")


def test_is_null_int():
    assert utils.is_null(-2147483648)


def test_is_null_bytes():
    assert utils.is_null(b"-2147483648")


def test_is_null_bytearray():
    assert utils.is_null(bytearray("-2147483648", encoding="utf-8"))


class TestGroupTemplateMixin:
    def test_group_templates_getter_initializes_with_empty_template_group(self):
        settings.CONNECTIONS["another_session"] = {}

        with connection_manager(name="another_session"):
            assert GroupTemplateMixin().group_templates == {}

        del settings.CONNECTIONS["another_session"]

    def test_group_templates_getter_initializes_with_defaults_if_safe(self):
        assert (
            GroupTemplateMixin().group_templates
            == settings.CONNECTIONS[connection.name]["GROUP_TEMPLATES"]
        )

    def test_get_group_templates(self):
        gt = GroupTemplateMixin()

        gt.group_templates = {
            connection.protocol.Tag.NoSecurityAltID: {
                "a": [
                    connection.protocol.Tag.SecurityAltID,
                    connection.protocol.Tag.SecurityAltIDSource,
                ]
            },
            connection.protocol.Tag.NoRoutingIDs: {
                "*": [
                    connection.protocol.Tag.RoutingType,
                    connection.protocol.Tag.RoutingID,
                ]
            },
        }

        assert gt.get_group_templates(
            identifier_tag=connection.protocol.Tag.NoSecurityAltID
        ) == [
            [
                connection.protocol.Tag.SecurityAltID,
                connection.protocol.Tag.SecurityAltIDSource,
            ]
        ]
        assert gt.get_group_templates(
            identifier_tag=connection.protocol.Tag.NoSecurityAltID, message_type="a"
        ) == [
            [
                connection.protocol.Tag.SecurityAltID,
                connection.protocol.Tag.SecurityAltIDSource,
            ]
        ]

    def test_get_group_templates_not_found(self):
        gt = GroupTemplateMixin()
        gt.group_templates = {
            connection.protocol.Tag.NoSecurityAltID: {
                "a": [
                    connection.protocol.Tag.SecurityAltID,
                    connection.protocol.Tag.SecurityAltIDSource,
                ]
            },
            connection.protocol.Tag.NoRoutingIDs: {
                "*": [
                    connection.protocol.Tag.RoutingType,
                    connection.protocol.Tag.RoutingID,
                ]
            },
        }

        assert gt.get_group_templates(identifier_tag=999) == []
        assert gt.get_group_templates(identifier_tag=999, message_type="b") == []

    def test_get_group_templates_falls_back_to_wildcard(self):
        gt = GroupTemplateMixin()
        gt.group_templates = {
            connection.protocol.Tag.NoSecurityAltID: {
                "a": [
                    connection.protocol.Tag.SecurityAltID,
                    connection.protocol.Tag.SecurityAltIDSource,
                ]
            },
            connection.protocol.Tag.NoRoutingIDs: {
                "*": [
                    connection.protocol.Tag.RoutingType,
                    connection.protocol.Tag.RoutingID,
                ]
            },
        }

        assert gt.get_group_templates(
            identifier_tag=connection.protocol.Tag.NoRoutingIDs, message_type="a"
        ) == [[connection.protocol.Tag.RoutingType, connection.protocol.Tag.RoutingID]]

    def test_add_group_templates(self):
        gt = GroupTemplateMixin()
        gt.add_group_templates(
            {
                connection.protocol.Tag.NoSecurityAltID: {
                    "*": [
                        connection.protocol.Tag.SecurityAltID,
                        connection.protocol.Tag.SecurityAltIDSource,
                    ]
                }
            }
        )

        assert connection.protocol.Tag.NoRoutingIDs in gt.group_templates
        assert connection.protocol.Tag.NoSecurityAltID in gt.group_templates

        assert gt.group_templates[connection.protocol.Tag.NoSecurityAltID]["*"] == [
            connection.protocol.Tag.SecurityAltID,
            connection.protocol.Tag.SecurityAltIDSource,
        ]

    def test_add_group_template_empty_raises_exception(self):
        with pytest.raises(ValidationError):
            GroupTemplateMixin().add_group_templates({})

    def test_add_group_template_empty_instance_raises_exception(self):
        with pytest.raises(ValidationError):
            GroupTemplateMixin().add_group_templates({35: {"*": []}})

    def test_add_group_template_wrong_structure_raises_exception(self):
        with pytest.raises(AttributeError):
            GroupTemplateMixin().add_group_templates({35: [1, 2, 3]})

    def test_is_template_tag(self):
        gt = GroupTemplateMixin()
        gt.add_group_templates({215: {"*": [216, 217]}})

        assert gt.is_template_tag(215) is True
        assert gt.is_template_tag(216) is True
        assert gt.is_template_tag(217) is True

        assert gt.is_template_tag(218) is False
