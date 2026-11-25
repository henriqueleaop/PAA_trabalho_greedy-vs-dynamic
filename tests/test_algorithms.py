"""Testes dos algoritmos; ignorados explicitamente enquanto solve() lançar NotImplementedError."""
import inspect
import unittest
from pathlib import Path

from paa.algorithms import ALGORITHMS, dynamic_programming, greedy
from paa.generators import TOPOLOGIES, generate
from paa.models import Instance
from paa.problem import load_cases, validate_matching

CASES = load_cases(Path(__file__).resolve().parents[1] / "data" / "cases.json")


def is_implemented(solver) -> bool:
    try:
        solver(Instance(1))
    except NotImplementedError:
        return False
    return True


class ContractTests(unittest.TestCase):
    def test_same_public_signature(self):
        self.assertEqual(inspect.signature(dynamic_programming.solve), inspect.signature(greedy.solve))


class SolverTests:
    """Bateria comum; subclasses definem `solver`. Não herda de TestCase para não rodar sozinha."""

    solver = None

    @classmethod
    def setUpClass(cls):
        if not is_implemented(cls.solver):
            raise unittest.SkipTest(f"{cls.__name__}: solve() ainda não implementado.")

    def check(self, instance: Instance, expected: int):
        solution = type(self).solver(instance)
        validate_matching(instance, solution)
        self.assertEqual(solution.size, expected)

    def test_known_optima(self):
        for case in CASES:
            with self.subTest(case=case.name):
                self.check(case.instance, case.expected_size)

    def test_generated_known_optima(self):
        # Ótimos por fórmula fechada, independentes dos algoritmos.
        for n in (1, 2, 3, 10, 11, 500):
            with self.subTest(n=n):
                self.check(generate("path", n, seed=n), n // 2)
                self.check(generate("star", n, seed=n), min(1, n - 1))
                # Vassoura: cabo de h = ⌈n/2⌉ vértices; se houver folhas extras, equivale
                # a um caminho de h + 1 vértices (as folhas da ponta são intercambiáveis).
                h = (n + 1) // 2
                self.check(generate("broom", n, seed=n), (h + 1) // 2 if n > h else h // 2)
        for n in (2, 10, 500):
            with self.subTest(caterpillar=n):
                # Lagarta com n par: cada vértice da espinha tem exatamente uma folha.
                self.check(generate("caterpillar", n, seed=n), n // 2)

    def test_does_not_mutate_input(self):
        instance = generate("random", 300, seed=3)
        snapshot = (instance.n, tuple(instance.edges))
        type(self).solver(instance)
        self.assertEqual((instance.n, instance.edges), snapshot)

    def test_deep_tree(self):
        # Caminho longo: falha se a implementação estourar o limite de recursão.
        n = 200_000
        self.check(generate("path", n, seed=0), n // 2)


class DynamicProgrammingTests(SolverTests, unittest.TestCase):
    solver = staticmethod(dynamic_programming.solve)


class GreedyTests(SolverTests, unittest.TestCase):
    solver = staticmethod(greedy.solve)


class AgreementTests(unittest.TestCase):
    """Compara apenas cardinalidades: pode haver vários emparelhamentos máximos."""

    @classmethod
    def setUpClass(cls):
        missing = [name for name, solver in ALGORITHMS.items() if not is_implemented(solver)]
        if missing:
            raise unittest.SkipTest(f"Algoritmos pendentes: {', '.join(missing)}.")

    def test_same_cardinality_on_generated_trees(self):
        for topology in TOPOLOGIES:
            for n in (1, 2, 7, 64, 1000):
                for seed in range(3):
                    instance = generate(topology, n, seed)
                    with self.subTest(topology=topology, n=n, seed=seed):
                        dp = dynamic_programming.solve(instance)
                        gr = greedy.solve(instance)
                        validate_matching(instance, dp)
                        validate_matching(instance, gr)
                        self.assertEqual(dp.size, gr.size)


if __name__ == "__main__":
    unittest.main()
