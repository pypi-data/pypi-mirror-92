from slate_utils.common.pkv import dict_to_pkv, pkv_to_dict


def test_pkv_to_dict():
    pkv_xml = "<p><k>foo</k><v>bar</v></p><p><k>fizz</k><v>buzz</v><v>bizz</v></p>"
    expected = {"foo": "bar", "fizz": ["buzz", "bizz"]}
    actual = pkv_to_dict(pkv_xml)
    assert actual == expected


def test_dict_to_pkv_nest_values():
    obj = {"foo": "bar", "fizz": ["buzz", "bizz"]}
    expected = "<p><k>foo</k><v>bar</v></p><p><k>fizz</k><v>buzz</v><v>bizz</v></p>"
    actual = dict_to_pkv(obj, duplicate_keys=False)
    assert actual == expected


def test_dict_to_pkv_duplicate_keys():
    obj = {"foo": "bar", "fizz": ["buzz", "bizz"]}
    expected = "<p><k>foo</k><v>bar</v></p><p><k>fizz</k><v>buzz</v></p><p><k>fizz</k><v>bizz</v></p>"
    actual = dict_to_pkv(obj, duplicate_keys=True)
    assert actual == expected
