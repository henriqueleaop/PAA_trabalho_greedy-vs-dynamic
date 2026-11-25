"""CLI.

    python -m paa solve --algorithm both --cases data/cases.json
    python -m paa benchmark --algorithm both --sizes 1000 10000 --repeat 5 --csv resultados.csv
"""
import argparse
import csv
import sys
from pathlib import Path

from paa.algorithms import ALGORITHMS, Solver
from paa.benchmark import compare
from paa.generators import TOPOLOGIES, generate
from paa.problem import load_cases, validate_instance, validate_matching


def selected(algorithm: str) -> dict[str, Solver]:
    return dict(ALGORITHMS) if algorithm == "both" else {algorithm: ALGORITHMS[algorithm]}


def run_solve(args: argparse.Namespace) -> None:
    cases = load_cases(args.cases)
    if not cases:
        raise ValueError(f"Nenhum caso em {args.cases}.")
    solvers = selected(args.algorithm)
    print(f"{'caso':<32} {'n':>7} {'esperado':>8}  " + "  ".join(f"{name:>8}" for name in solvers))
    for case in cases:
        sizes = []
        for name, solver in solvers.items():
            solution = solver(case.instance)
            validate_matching(case.instance, solution)
            if case.expected_size is not None and solution.size != case.expected_size:
                raise AssertionError(f"{case.name}: {name} retornou {solution.size}, ótimo esperado {case.expected_size}.")
            sizes.append(solution.size)
        if len(set(sizes)) > 1:
            raise AssertionError(f"{case.name}: cardinalidades diferentes entre algoritmos: {sizes}.")
        expected = "-" if case.expected_size is None else case.expected_size
        print(f"{case.name:<32} {case.instance.n:>7} {expected:>8}  " + "  ".join(f"{s:>8}" for s in sizes))


def run_benchmark(args: argparse.Namespace) -> None:
    solvers = selected(args.algorithm)
    rows = []
    print(f"{'topologia':<12} {'n':>9} {'algoritmo':<8} {'|M|':>8} {'mediana ms':>12} {'mínimo ms':>12}")
    for topology in args.topologies:
        for n in args.sizes:
            instance = generate(topology, n, args.seed)
            validate_instance(instance)
            for m in compare(solvers, instance, validate_matching, args.repeat):
                print(f"{topology:<12} {n:>9} {m.algorithm:<8} {m.size:>8} {m.median_ms:>12.3f} {m.min_ms:>12.3f}")
                rows.append({
                    "topology": topology, "n": n, "seed": args.seed, "algorithm": m.algorithm,
                    "size": m.size, "median_ms": f"{m.median_ms:.6f}", "min_ms": f"{m.min_ms:.6f}",
                    "repetitions": m.repetitions,
                })
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        print(f"Resultados gravados em {args.csv}")


def positive_int(text: str) -> int:
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError("deve ser um inteiro positivo")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m paa", description="Emparelhamento máximo em árvores: PD × guloso.")
    sub = parser.add_subparsers(dest="command", required=True)
    algorithm = argparse.ArgumentParser(add_help=False)
    algorithm.add_argument("--algorithm", choices=[*ALGORITHMS, "both"], default="both")

    solve = sub.add_parser("solve", parents=[algorithm], help="resolver e validar os casos com ótimo conhecido")
    solve.add_argument("--cases", type=Path, default=Path("data/cases.json"))
    solve.set_defaults(run=run_solve)

    bench = sub.add_parser("benchmark", parents=[algorithm], help="medir tempo em árvores geradas")
    bench.add_argument("--topologies", nargs="+", choices=TOPOLOGIES, default=list(TOPOLOGIES))
    bench.add_argument("--sizes", nargs="+", type=positive_int, default=[1_000, 10_000, 100_000])
    bench.add_argument("--seed", type=int, default=42)
    bench.add_argument("--repeat", type=positive_int, default=5)
    bench.add_argument("--csv", type=Path, help="arquivo CSV de saída (opcional)")
    bench.set_defaults(run=run_benchmark)

    args = parser.parse_args(argv)
    try:
        args.run(args)
        return 0
    except NotImplementedError as exc:
        print(f"Pendente: {exc} Use --algorithm para executar apenas o outro método.", file=sys.stderr)
    except (ValueError, OSError, KeyError, TypeError, AssertionError, RecursionError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
