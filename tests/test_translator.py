from __future__ import annotations

import xml.etree.ElementTree as ET

import pytest

from configlang.errors import EvaluationError
from configlang.translator import ConfigTranslator


def _get_const(root: ET.Element, name: str) -> ET.Element:
    found = root.find(f"./const[@name='{name}']")
    assert found is not None, f"const {name} not found"
    return found


def test_numbers_and_strings():
    text = """
    port := 0o12;
    host := q(localhost);
    """
    result = ConfigTranslator().translate(text)
    root = ET.fromstring(result.xml)

    port_node = _get_const(root, "port").find("./number")
    host_node = _get_const(root, "host").find("./string")

    assert port_node is not None and port_node.text == "10"
    assert host_node is not None and host_node.text == "localhost"


def test_array_and_nested_expression():
    text = """
    base := 0o10;
    servers := { q(api). q(db). };
    limits := { [+ base 0o1]. { 0o2. 0o3. }. };
    """
    result = ConfigTranslator().translate(text)
    root = ET.fromstring(result.xml)

    limits = _get_const(root, "limits").find("./array")
    assert limits is not None

    first_item_number = limits.find("./item[1]/number")
    nested_second = limits.find("./item[2]/array/item[2]/number")

    assert first_item_number is not None and first_item_number.text == "9"
    assert nested_second is not None and nested_second.text == "3"


def test_const_expr_arithmetic_chain():
    text = """
    a := [+ 0o4 0o4];
    b := [- a 0o2];
    c := [* b 0o2];
    d := [/ c 0o2];
    """
    result = ConfigTranslator().translate(text)
    root = ET.fromstring(result.xml)

    assert _get_const(root, "a").find("./number").text == "8"
    assert _get_const(root, "b").find("./number").text == "6"
    assert _get_const(root, "c").find("./number").text == "12"
    assert float(_get_const(root, "d").find("./number").text) == 6


def test_name_reference_error():
    text = "value := unknown;"
    translator = ConfigTranslator()
    with pytest.raises(EvaluationError):
        translator.translate(text)


def test_comments_are_ignored():
    text = """
    =begin
    это комментарий
    =cut
    meaning := q(active);
    """
    result = ConfigTranslator().translate(text)
    root = ET.fromstring(result.xml)
    assert _get_const(root, "meaning").find("./string").text == "active"


def test_print_returns_value_and_collects_output(capsys):
    text = """
    value := [+ 0o2 0o3];
    shown := [print value];
    """
    result = ConfigTranslator().translate(text)
    root = ET.fromstring(result.xml)

    assert result.print_outputs == ["5"]
    assert _get_const(root, "shown").find("./number").text == "5"

