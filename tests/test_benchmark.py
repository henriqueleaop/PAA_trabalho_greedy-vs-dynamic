"""Testa a infraestrutura de benchmark com solvers fictícios, não os algoritmos."""
import unittest

from paa.benchmark import compare, measure
from paa.models import Instance, Solution
from paa.problem import validate_matching

TREE = Instance(3, ((0, 1), (1, 2)))


def empty_solver(instance):
    return Solution(())


def first_edge_solver(instance):
    return Solution(instance.edges[:1])


class BenchmarkTests(unittest.TestCase):
    def test_measure(self):
        result = measure("fake", first_edge_solver, TREE, validate_matching, 3, expected_size=1)
        self.assertEqual((result.algorithm, result.size, result.repetitions), ("fake", 1, 3))
        self.assertGreaterEqual(result.median_ms, result.min_ms)
        self.assertGreaterEqual(result.min_ms, 0)

    def test_compare_same_size(self):
        results = compare({"a": first_edge_solver, "b": first_edge_solver}, TREE, validate_matching, 2)
        self.assertEqual([m.size for m in results], [1, 1])

    def test_compare_single_solver(self):
        self.assertEqual(len(compare({"a": empty_solver}, TREE, validate_matching, 1)), 1)

    def test_invalid_repetitions(self):
        with self.assertRaises(ValueError):
            measure("fake", empty_solver, TREE, validate_matching, 0)

    def test_wrong_expected_size(self):
        with self.assertRaises(AssertionError):
            measure("fake", empty_solver, TREE, validate_matching, 1, expected_size=1)

    def test_different_sizes(self):
        with self.assertRaises(AssertionError):
            compare({"a": empty_solver, "b": first_edge_solver}, TREE, validate_matching, 1)

    def test_invalid_matching_is_rejected(self):
        with self.assertRaises(ValueError):
            measure("fake", lambda _: Solution(((0, 1), (1, 2))), TREE, validate_matching, 1)

    def test_inconsistent_repetitions(self):
        answers = iter([Solution(()), Solution(((0, 1),))])
        with self.assertRaises(AssertionError):
            measure("fake", lambda _: next(answers), TREE, validate_matching, 2)


if __name__ == "__main__":
    unittest.main()
