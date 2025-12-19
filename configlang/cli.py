from __future__ import annotations

import sys

from .errors import EvaluationError, ParseError
from .translator import ConfigTranslator


def main() -> int:
    source = sys.stdin.read()
    translator = ConfigTranslator()
    try:
        result = translator.translate(source)
    except (ParseError, EvaluationError) as exc:  # pragma: no cover - CLI path
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 1

    for printed in result.print_outputs:
        print(printed, file=sys.stderr)

    sys.stdout.write(result.xml)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

