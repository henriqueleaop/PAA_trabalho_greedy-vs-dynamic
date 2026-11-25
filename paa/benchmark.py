"""Mede somente solve(), sem I/O, cópia da entrada ou validação."""
from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass
from math import isclose, isfinite
from statistics import median
from time import perf_counter_ns

from paa.models import Case, Instance, Solution

Solver = Callable[[Instance], Solution]
Validator = Callable[[Instance, Solution], None]


@dataclass(frozen=True)
class Measurement:
    objective: int | float
    median_ms: float
    min_ms: float
    repetitions: int


def same_objective(a: int | float, b: int | float) -> bool:
    if isinstance(a, int) and isinstance(b, int):
        return a == b
    return isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)


def measure(solver: Solver, case: Case, validate: Validator, repetitions: int = 10) -> Measurement:
    if repetitions < 1:
        raise ValueError("O número de repetições deve ser positivo.")
    durations = []
    objectives = []
    for _ in range(repetitions):
        instance = deepcopy(case.instance)
        start = perf_counter_ns()
        solution = solver(instance)
        elapsed = perf_counter_ns() - start
        # Validação usa a entrada original, inclusive se o solver alterar sua cópia.
        validate(deepcopy(case.instance), solution)
        if isinstance(solution.objective, bool) or not isinstance(solution.objective, (int, float)):
            raise ValueError("Objetivo deve ser numérico.")
        if isinstance(solution.objective, float) and not isfinite(solution.objective):
            raise ValueError("Objetivo deve ser finito.")
        if case.expected_objective is not None and not same_objective(solution.objective, case.expected_objective):
            raise AssertionError(f"{case.name}: objetivo diferente do ótimo esperado.")
        if objectives and not same_objective(solution.objective, objectives[0]):
            raise AssertionError(f"{case.name}: objetivos inconsistentes entre repetições.")
        objectives.append(solution.objective)
        durations.append(elapsed / 1_000_000)
    return Measurement(objectives[0], median(durations), min(durations), repetitions)


def compare(dp: Solver, greedy: Solver, case: Case, validate: Validator, repetitions: int = 10) -> tuple[Measurement, Measurement]:
    left = measure(dp, case, validate, repetitions)
    right = measure(greedy, case, validate, repetitions)
    if not same_objective(left.objective, right.objective):
        raise AssertionError(f"{case.name}: os algoritmos retornaram objetivos diferentes.")
    return left, right
