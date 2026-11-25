"""Execução: python -m paa --cases data/cases.json --repeat 10."""
import argparse
import json
import sys
from pathlib import Path

from paa.algorithms import dynamic_programming, greedy
from paa.benchmark import compare
from paa.models import Case, Instance
from paa.problem import validate_instance, validate_solution


def main() -> int:
    parser = argparse.ArgumentParser(description="Comparar PD e guloso no mesmo conjunto de casos.")
    parser.add_argument("--cases", type=Path, default=Path("data/cases.json"))
    parser.add_argument("--repeat", type=int, default=10)
    args = parser.parse_args()
    if args.repeat < 1:
        parser.error("--repeat deve ser positivo")
    try:
        rows = json.loads(args.cases.read_text(encoding="utf-8"))
        if not isinstance(rows, list) or not rows:
            raise ValueError("Nenhum caso definido; preencha data/cases.json após escolher o problema.")
        for row in rows:
            case = Case(row["name"], Instance(row["data"]), row.get("expected_objective"))
            validate_instance(case.instance)
            dp, gr = compare(dynamic_programming.solve, greedy.solve, case, validate_solution, args.repeat)
            print(f"{case.name}: objetivo={dp.objective} | PD={dp.median_ms:.6f} ms | Guloso={gr.median_ms:.6f} ms")
        return 0
    except (NotImplementedError, ValueError, OSError, KeyError, TypeError, AssertionError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
