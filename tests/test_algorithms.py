"""Testes dos algoritmos; ignorados explicitamente enquanto solve() lançar NotImplementedError."""
import inspect
import unittest
from itertools import product
from pathlib import Path

from paa.algorithms import ALGORITHMS, dynamic_programming, greedy
from paa.generators import TOPOLOGIES, generate
from paa.models import Instance
from paa.problem import load_cases, validate_instance, validate_matching

CASES = load_cases(Path(__file__).resolve().parents[1] / "data" / "cases.json")


def prufer_tree(sequence: tuple[int, ...]) -> Instance:
    """Decodifica uma sequência de Prüfer (O(n²), suficiente para n pequeno)."""
    n = len(sequence) + 2
    degree = [1] * n
    for v in sequence:
        degree[v] += 1
    edges = []
    for v in sequence:
        leaf = min(u for u in range(n) if degree[u] == 1)
        edges.append((leaf, v))
        degree[leaf] -= 1
        degree[v] -= 1
    u, w = (x for x in range(n) if degree[x] == 1)
    edges.append((u, w))
    return Instance(n, tuple(edges))


def brute_force_size(instance: Instance) -> int:
    """Oráculo exponencial: testa todos os subconjuntos de arestas (só para n pequeno)."""
    edges = instance.edges
    best = 0
    for mask in range(1 << len(edges)):
        chosen = [edges[i] for i in range(len(edges)) if mask >> i & 1]
        vertices = [x for edge in chosen for x in edge]
        if len(chosen) > best and len(vertices) == len(set(vertices)):
            best = len(chosen)
    return best


def small_trees():
    """Todas as árvores rotuladas com n ≤ 6 e árvores aleatórias com 7 ≤ n ≤ 10."""
    yield Instance(1)
    yield Instance(2, ((0, 1),))
    for n in range(3, 7):
        yield from (prufer_tree(seq) for seq in product(range(n), repeat=n - 2))
    for n in range(7, 11):
        for seed in range(10):
            yield generate("random", n, seed)


def is_implemented(solver) -> bool:
    try:
        solver(Instance(1))
    except NotImplementedError:
        return False
    return True


class ContractTests(unittest.TestCase):
    def test_same_public_signature(self):
        self.assertEqual(inspect.signature(dynamic_programming.solve), inspect.signature(greedy.solve))


class OracleTests(unittest.TestCase):
    """Confere os oráculos de teste, independentemente dos algoritmos."""

    def test_prufer_enumerates_all_labeled_trees(self):
        n = 5
        trees = [prufer_tree(seq) for seq in product(range(n), repeat=n - 2)]
        for tree in trees:
            validate_instance(tree)
        distinct = {frozenset(frozenset(edge) for edge in tree.edges) for tree in trees}
        self.assertEqual(len(distinct), n ** (n - 2))  # Fórmula de Cayley

    def test_brute_force_matches_known_cases(self):
        for case in CASES:
            with self.subTest(case=case.name):
                self.assertEqual(brute_force_size(case.instance), case.expected_size)


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

    def test_matches_brute_force_on_small_trees(self):
        for instance in small_trees():
            with self.subTest(instance=instance):
                self.check(instance, brute_force_size(instance))

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
