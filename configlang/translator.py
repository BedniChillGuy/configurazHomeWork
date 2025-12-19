from __future__ import annotations

from dataclasses import dataclass

from .evaluator import Evaluator
from .parser import ConfigParser
from .xml_builder import XmlBuilder


@dataclass
class TranslationResult:
    xml: str
    print_outputs: list[str]
    constants: list[tuple[str, object]]


class ConfigTranslator:
    def __init__(self):
        self._parser = ConfigParser()
        self._evaluator = Evaluator()
        self._xml_builder = XmlBuilder()

    def translate(self, text: str) -> TranslationResult:
        declarations = self._parser.parse(text)
        eval_result = self._evaluator.evaluate(declarations)
        xml = self._xml_builder.build(eval_result.constants)
        return TranslationResult(xml=xml, print_outputs=eval_result.print_outputs, constants=eval_result.constants)

