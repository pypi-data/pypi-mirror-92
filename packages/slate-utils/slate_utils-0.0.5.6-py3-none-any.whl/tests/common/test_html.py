from bs4 import BeautifulSoup
from slate_utils.common.html import parse_form


def test_parse_form_input():
    soup = BeautifulSoup("<input type='text' name='foo' value='bar'>")
    expected = {"foo": ["bar"]}
    assert parse_form(soup) == expected


def test_parse_form_checkbox():
    html = """
    <form>
        <input type='checkbox' name='foo' value='bar' checked>
        <input type='checkbox' name='foo' value='bizz' checked>
        <input type='checkbox' name='foo' value='buzz'>
    </form>
    """
    soup = BeautifulSoup(html)
    expected = {"foo": ["bar", "bizz"]}
    assert parse_form(soup) == expected


def test_parse_form_select():
    html = """
        <form>
            <select name='foo'>
                <option value='bar' selected>Bar</option>
                <option value='bizz'>Bizz</option>
                <option value='buzz'>Buzz</option>
            </select>
        </form>"""
    soup = BeautifulSoup(html)
    expected = {"foo": ["bar"]}
    assert parse_form(soup) == expected


def test_parse_form_multiselect():
    html = """
        <form>
            <select name='foo'>
                <option value='bar' selected>Bar</option>
                <option value='bizz'>Bizz</option>
                <option value='buzz' selected>Buzz</option>
            </select>
        </form>"""
    soup = BeautifulSoup(html)
    expected = {"foo": ["bar", "buzz"]}
    assert parse_form(soup) == expected


def test_parse_form_disabled_input():
    html = """
    <form>
    <input type='text' name='foo' value='bar'>
    <input type='text' name='bizz' value='buzz' disabled>
    </form>"""
    soup = BeautifulSoup(html)
    expected = {"foo": ["bar"]}
    assert parse_form(soup) == expected
