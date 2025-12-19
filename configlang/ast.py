from __future__ import annotations

from dataclasses import dataclass
from typing import List, Union


@dataclass
class NumberLiteral:
    raw: str
    value: int


@dataclass
class StringLiteral:
    value: str


@dataclass
class ArrayLiteral:
    items: List["ValueNode"]


@dataclass
class NameRef:
    name: str


@dataclass
class ConstExpr:
    op: str
    args: List["ValueNode"]


@dataclass
class ConstDecl:
    name: str
    value: "ValueNode"


ValueNode = Union[NumberLiteral, StringLiteral, ArrayLiteral, NameRef, ConstExpr]

