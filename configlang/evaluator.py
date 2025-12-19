from __future__ import annotations

import operator
from typing import Any, Dict, Iterable, List, Tuple

from .ast import ArrayLiteral, ConstDecl, ConstExpr, NameRef, NumberLiteral, StringLiteral, ValueNode
from .errors import EvaluationError


class EvaluationResult:
    def __init__(self, constants: List[Tuple[str, Any]], print_outputs: List[str]):
        self.constants = constants
        self.print_outputs = print_outputs


class Evaluator:
    def __init__(self):
        self._print_outputs: List[str] = []

    def evaluate(self, declarations: Iterable[ConstDecl]) -> EvaluationResult:
        env: Dict[str, Any] = {}
        ordered: List[Tuple[str, Any]] = []

        for decl in declarations:
            value = self._eval_value(decl.value, env)
            env[decl.name] = value
            ordered.append((decl.name, value))

        return EvaluationResult(constants=ordered, print_outputs=list(self._print_outputs))

    def _eval_value(self, node: ValueNode, env: Dict[str, Any]) -> Any:
        if isinstance(node, NumberLiteral):
            return node.value
        if isinstance(node, StringLiteral):
            return node.value
        if isinstance(node, ArrayLiteral):
            return [self._eval_value(item, env) for item in node.items]
        if isinstance(node, NameRef):
            if node.name not in env:
                raise EvaluationError(f"Идентификатор {node.name} не объявлен")
            return env[node.name]
        if isinstance(node, ConstExpr):
            return self._eval_const_expr(node, env)

        raise EvaluationError(f"Неизвестный узел {type(node).__name__}")

    def _eval_const_expr(self, expr: ConstExpr, env: Dict[str, Any]) -> Any:
        args = [self._eval_value(arg, env) for arg in expr.args]
        op = expr.op

        if op in {"+", "-", "*", "/"}:
            return self._eval_arithmetic(op, args)

        if op == "print":
            if len(args) != 1:
                raise EvaluationError("print ожидает ровно один аргумент")
            value = args[0]
            self._print_outputs.append(str(value))
            return value

        raise EvaluationError(f"Неизвестная операция {op}")

    @staticmethod
    def _eval_arithmetic(op: str, args: List[Any]) -> Any:
        if len(args) < 2:
            raise EvaluationError(f"Операция {op} требует минимум два аргумента")
        if not all(isinstance(v, (int, float)) for v in args):
            raise EvaluationError(f"Операция {op} поддерживает только числовые аргументы")

        operations = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
        }
        func = operations[op]
        result = args[0]
        for value in args[1:]:
            if op == "/" and value == 0:
                raise EvaluationError("Деление на ноль")
            result = func(result, value)
        return result

