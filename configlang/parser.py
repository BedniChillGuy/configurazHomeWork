from __future__ import annotations

from lark import Lark, Transformer, v_args
from lark.exceptions import UnexpectedInput

from .ast import ArrayLiteral, ConstDecl, ConstExpr, NameRef, NumberLiteral, StringLiteral, ValueNode
from .errors import ParseError
from .grammar import GRAMMAR


class _AstBuilder(Transformer):
    @v_args(inline=True)
    def const_stmt(self, name_token, value):
        return ConstDecl(name=str(name_token), value=value)

    @v_args(inline=True)
    def number(self, token):
        raw = str(token)
        # Strip leading 0o/0O and interpret as octal
        value = int(raw[2:], 8)
        return NumberLiteral(raw=raw, value=value)

    @v_args(inline=True)
    def string(self, body_token):
        return StringLiteral(value=str(body_token))

    def empty_string(self, _children):
        return StringLiteral(value="")

    def array(self, children):
        return ArrayLiteral(items=list(children))

    @v_args(inline=True)
    def const_expr(self, op_token, *args):
        op = str(op_token)
        if op == "print()":
            op = "print"
        return ConstExpr(op=op, args=list(args))

    @v_args(inline=True)
    def name_ref(self, name_token):
        return NameRef(name=str(name_token))

    def start(self, children):
        return list(children)


class ConfigParser:
    def __init__(self):
        self._parser = Lark(
            GRAMMAR,
            parser="lalr",
            propagate_positions=True,
            maybe_placeholders=False,
        )
        self._builder = _AstBuilder()

    def parse(self, text: str) -> list[ConstDecl]:
        try:
            tree = self._parser.parse(text)
            return self._builder.transform(tree)
        except UnexpectedInput as exc:  # pragma: no cover - exercised via CLI
            raise ParseError(self._format_error(exc)) from exc

    @staticmethod
    def _format_error(exc: UnexpectedInput) -> str:
        line = exc.line or "?"
        column = exc.column or "?"
        return f"Синтаксическая ошибка в строке {line}, столбце {column}: {exc}"

