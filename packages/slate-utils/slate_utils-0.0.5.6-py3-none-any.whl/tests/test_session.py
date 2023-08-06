import pytest

from slate_utils.session import parse_hostname


def test_parse_hostname():
    hostnames = [
        ('https://myuniversity.net', 'https://myuniversity.net'),
        ('myuniversity.net', 'https://myuniversity.net'),
        ('myuniversity.net/', 'https://myuniversity.net'),
        ('https://myuniversity.net/', 'https://myuniversity.net')]
    for (value, expected) in hostnames:
        assert parse_hostname(value) == expected