from lxml import html


def pkv_to_dict(xml: str) -> dict:
    """Parses PKV xml to a dictionary. If there are multiple entries for the
    same key, those values will be returned as a list. Otherwise a single
    string will be returned as a value.

    Parameters
    ----------
    xml : str (xml)
        The xml containing PKV values.
    """
    pkv_dict = {}
    for p in html.fromstring(xml).findall("p"):
        k = p.find("k").text
        vals = [v.text for v in p.findall("v")]
        if k in pkv_dict:
            pkv_dict[k] = pkv_dict[k] + vals
        else:
            pkv_dict[k] = vals

    for k, v in pkv_dict.items():
        if len(v) == 1:
            pkv_dict[k] = v[0]

    return pkv_dict


def dict_to_pkv(obj: dict, duplicate_keys=True) -> str:
    """
    Serialize a dictionary into an PKV xml string.

    Parameters
    ----------
    obj : dict
        The dictionary to serialize.
    duplicate_keys : bool
        Whether the returned xml should return duplicate pkv entries when a key has multiple values (True) or whether
        to nest all values under a single entry (False).

    Returns
    -------
    str
        A serialized representation of the dictionary in PKV format.
    """
    pkv = ""
    for k, v in obj.items():
        if isinstance(v, list):
            if duplicate_keys:
                for value in v:
                    pkv += f"<p><k>{k}</k><v>{value}</v></p>"
                continue
            else:
                v_node = "".join(f"<v>{value}</v>" for value in v)
        else:
            v_node = f"<v>{v}</v>"
        pkv += f"<p><k>{k}</k>{v_node}</p>"
    return pkv
