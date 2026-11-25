"""Testa somente a infraestrutura com funções fictícias, não os algoritmos."""
import unittest

from paa.benchmark import compare, measure
from paa.models import Case, Instance, Solution


def fake_solver(instance):
    return Solution(instance.data["value"], [])


def fake_validate(instance, solution):
    if solution.objective != instance.data["value"]:
        raise ValueError("Objetivo inválido")


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.case = Case("infraestrutura", Instance({"value": 42}), 42)

    def test_compare(self):
        left, right = compare(fake_solver, fake_solver, self.case, fake_validate, 2)
        self.assertEqual(left.objective, right.objective)
        self.assertEqual(left.repetitions, 2)
        self.assertGreaterEqual(left.median_ms, 0)

    def test_invalid_repetitions(self):
        with self.assertRaises(ValueError):
            measure(fake_solver, self.case, fake_validate, 0)

    def test_wrong_expected_objective(self):
        case = Case("incorreto", self.case.instance, 99)
        with self.assertRaises(AssertionError):
            measure(fake_solver, case, fake_validate, 1)

    def test_different_objectives(self):
        case = Case("divergencia", self.case.instance)
        with self.assertRaises(AssertionError):
            compare(fake_solver, lambda _: Solution(99, []), case, lambda *_: None, 1)

    def test_isolated_input(self):
        def mutating_solver(instance):
            value = instance.data.pop("value")
            return Solution(value, [])
        measure(mutating_solver, self.case, fake_validate, 2)
        self.assertEqual(self.case.instance.data, {"value": 42})
