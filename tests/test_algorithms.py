"""Testes de integração; deixam pendências explícitas enquanto não houver casos."""
import json
import unittest
from copy import deepcopy
from pathlib import Path

from paa.algorithms import dynamic_programming, greedy
from paa.benchmark import same_objective
from paa.models import Instance
from paa.problem import validate_instance, validate_solution


class AlgorithmTests(unittest.TestCase):
    def test_known_optima(self):
        path = Path(__file__).resolve().parents[1] / "data" / "cases.json"
        cases = json.loads(path.read_text(encoding="utf-8"))
        known = [case for case in cases if case.get("expected_objective") is not None]
        if not known:
            self.skipTest("TODO: adicionar casos com ótimos verificados independentemente.")
        for case in known:
            for name, solver in (("PD", dynamic_programming.solve), ("Guloso", greedy.solve)):
                with self.subTest(case=case["name"], algorithm=name):
                    instance = Instance(deepcopy(case["data"]))
                    validate_instance(instance)
                    solution = solver(deepcopy(instance))
                    validate_solution(instance, solution)
                    self.assertTrue(same_objective(solution.objective, case["expected_objective"]))
