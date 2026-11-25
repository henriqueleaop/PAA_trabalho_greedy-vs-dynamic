"""Validação de árvores, de emparelhamentos e dos casos em data/cases.json."""
import unittest
from pathlib import Path

from paa.models import Instance, Solution
from paa.problem import build_adjacency, load_cases, normalize_edge, validate_instance, validate_matching

CASES_PATH = Path(__file__).resolve().parents[1] / "data" / "cases.json"
PATH_4 = Instance(4, ((0, 1), (1, 2), (2, 3)))


class AdjacencyTests(unittest.TestCase):
    def test_build_adjacency(self):
        adjacency = build_adjacency(Instance(4, ((0, 1), (2, 1), (1, 3))))
        self.assertEqual([sorted(neighbors) for neighbors in adjacency], [[1], [0, 2, 3], [1], [1]])

    def test_single_vertex(self):
        self.assertEqual(build_adjacency(Instance(1)), [[]])

    def test_normalize_edge(self):
        self.assertEqual(normalize_edge(3, 1), (1, 3))
        self.assertEqual(normalize_edge(1, 3), (1, 3))


class InstanceValidationTests(unittest.TestCase):
    def test_valid_trees(self):
        for instance in (Instance(1), Instance(2, ((1, 0),)), PATH_4, Instance(4, ((0, 1), (0, 2), (0, 3)))):
            with self.subTest(instance=instance):
                validate_instance(instance)

    def test_invalid_instances(self):
        invalid = {
            "n zero": Instance(0),
            "n negativo": Instance(-3),
            "n booleano": Instance(True),
            "n não inteiro": Instance(2.0, ((0, 1),)),
            "arestas a menos": Instance(3, ((0, 1),)),
            "arestas a mais": Instance(2, ((0, 1), (1, 0))),
            "laço": Instance(2, ((1, 1),)),
            "vértice fora do intervalo": Instance(2, ((0, 2),)),
            "vértice negativo": Instance(2, ((-1, 0),)),
            "vértice não inteiro": Instance(2, ((0, "1"),)),
            "vértice booleano": Instance(2, ((False, True),)),
            "aresta não é par": Instance(2, ((0, 1, 1),)),
            "aresta repetida": Instance(3, ((0, 1), (1, 0))),
            "ciclo e vértice isolado": Instance(4, ((0, 1), (1, 2), (2, 0))),
            "edges não é sequência": Instance(2, None),
        }
        for label, instance in invalid.items():
            with self.subTest(label), self.assertRaises(ValueError):
                validate_instance(instance)


class MatchingValidationTests(unittest.TestCase):
    def test_valid_matchings(self):
        for matching in ((), ((0, 1),), ((1, 0), (3, 2)), [(1, 2)]):
            with self.subTest(matching=matching):
                validate_matching(PATH_4, Solution(matching))

    def test_size_is_cardinality(self):
        self.assertEqual(Solution(((0, 1), (2, 3))).size, 2)

    def test_invalid_matchings(self):
        invalid = {
            "aresta fora da árvore": ((0, 2),),
            "vértice compartilhado": ((0, 1), (1, 2)),
            "aresta repetida": ((0, 1), (0, 1)),
            "aresta repetida invertida": ((0, 1), (1, 0)),
            "laço": ((1, 1),),
            "vértice fora do intervalo": ((3, 4),),
            "item não é par": ((0, 1, 2),),
            "vértice não inteiro": (("0", 1),),
            "matching não é sequência": None,
        }
        for label, matching in invalid.items():
            with self.subTest(label), self.assertRaises(ValueError):
                validate_matching(PATH_4, Solution(matching))

    def test_rejects_non_solution(self):
        with self.assertRaises(ValueError):
            validate_matching(PATH_4, ((0, 1),))


class CaseFileTests(unittest.TestCase):
    def test_cases_are_valid_trees(self):
        cases = load_cases(CASES_PATH)
        self.assertTrue(cases)
        self.assertEqual(len({case.name for case in cases}), len(cases), "nomes repetidos")
        for case in cases:
            with self.subTest(case=case.name):
                self.assertIsInstance(case.expected_size, int)
                # Limite trivial: cada aresta emparelhada consome dois vértices.
                self.assertLessEqual(case.expected_size, case.instance.n // 2)


if __name__ == "__main__":
    unittest.main()
