GRAMMAR = r"""
start: statement*

statement: NAME ":=" value ";"           -> const_stmt

?value: number
      | string
      | array
      | const_expr
      | name_ref

number: OCT_NUMBER                       -> number
string: "q(" STRING_BODY ")"             -> string
      | "q(" ")"                         -> empty_string
array: "{" [value ("." value)* "."?] "}" -> array
const_expr: "[" OP value+ "]"            -> const_expr
name_ref: NAME                           -> name_ref

OP: "+" | "-" | "*" | "/" | "print" | "print()"

COMMENT: "=begin" /(.|\n)*?/ "=cut"

OCT_NUMBER: "0" /[oO][0-7]+/
STRING_BODY: /(?s:[^)]+)/
NAME: /[_a-zA-Z][_a-zA-Z0-9]*(?!\()/

%import common.WS
%ignore WS
%ignore COMMENT
"""

