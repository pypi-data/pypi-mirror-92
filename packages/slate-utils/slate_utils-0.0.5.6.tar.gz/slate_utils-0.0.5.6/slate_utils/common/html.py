from bs4 import BeautifulSoup, Tag


def parse_form(form: Tag):
    nodes = form.findAll(["input", "select"])
    form_values = {}
    for node in nodes:
        key = node.get("name")
        if key is None:
            continue
        if node.has_attr("disabled"):
            continue
        if node.name == "input":
            if node["type"] == "checkbox":
                if node.has_attr("checked"):
                    value = node.get("value", "")
                else:
                    continue
            else:
                value = node.get("value", "")
        if node.name == "select":
            value = [
                opt.get("value")
                for opt in node.findAll("option")
                if opt.has_attr("selected")
            ]
        if not isinstance(value, list):
            value = [value]
        if key in form_values:
            form_values[key].extend(value)
        else:
            form_values[key] = value
    return form_values


def parse_query_config(config_response: str):
    soup = BeautifulSoup(config_response, "lxml")
    nodes = soup.find_all(["input", "select"])
    form_values = {}
    for node in nodes:
        key = node.get("name")
        if key is None:
            continue
        if node.name == "input":
            if node["type"] == "checkbox":
                if node.has_attr("checked"):
                    value = node.get("value", "")
                else:
                    continue
            else:
                value = node.get("value", "")
        if node.name == "select":
            value = [
                opt.get("value")
                for opt in node.find_all("option")
                if opt.has_attr("selected")
            ]
        if not isinstance(value, list):
            value = [value]
        if key in form_values:
            form_values[key].extend(value)
        else:
            form_values[key] = value
    return form_values
