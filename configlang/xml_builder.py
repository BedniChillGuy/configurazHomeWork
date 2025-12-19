from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any, Iterable, Tuple


class XmlBuilder:
    def build(self, constants: Iterable[Tuple[str, Any]]) -> str:
        root = ET.Element("config")

        for name, value in constants:
            const_el = ET.SubElement(root, "const", {"name": str(name)})
            const_el.append(self._build_value(value))

        self._indent(root)
        return ET.tostring(root, encoding="unicode")

    def _build_value(self, value: Any):
        if isinstance(value, bool):
            # Bool is subclass of int, keep explicit tag for clarity
            elem = ET.Element("boolean")
            elem.text = "true" if value else "false"
            return elem

        if isinstance(value, int):
            elem = ET.Element("number", {"format": "decimal"})
            elem.text = str(value)
            return elem

        if isinstance(value, float):
            elem = ET.Element("number", {"format": "float"})
            elem.text = str(value)
            return elem

        if isinstance(value, str):
            elem = ET.Element("string")
            elem.text = value
            return elem

        if isinstance(value, list):
            array_el = ET.Element("array")
            for item in value:
                item_el = ET.SubElement(array_el, "item")
                item_el.append(self._build_value(item))
            return array_el

        raise TypeError(f"Неподдерживаемый тип значения {type(value)}")

    def _indent(self, elem: ET.Element, level: int = 0):
        # Pretty-print XML with indentation
        indent_str = "\n" + "  " * level
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = indent_str + "  "
            for child in elem:
                self._indent(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = indent_str
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent_str

