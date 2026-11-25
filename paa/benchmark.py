"""Mede somente solve(); geração, validação e I/O ficam fora da região cronometrada."""
import gc
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from statistics import median
from time import perf_counter_ns

from paa.models import Instance, Solution

Solver = Callable[[Instance], Solution]
Validator = Callable[[Instance, Solution], None]


@dataclass(frozen=True)
class Measurement:
    algorithm: str
    size: int
    median_ms: float
    min_ms: float
    repetitions: int


def measure(
    name: str,
    solver: Solver,
    instance: Instance,
    validate: Validator,
    repetitions: int = 5,
    expected_size: int | None = None,
) -> Measurement:
    """Executa o solver várias vezes, valida cada resposta e resume os tempos em ms."""
    if repetitions < 1:
        raise ValueError("O número de repetições deve ser positivo.")
    durations: list[float] = []
    sizes: set[int] = set()
    for _ in range(repetitions):
        gc.collect()
        gc.disable()
        try:
            start = perf_counter_ns()
            solution = solver(instance)
            elapsed = perf_counter_ns() - start
        finally:
            gc.enable()
        validate(instance, solution)
        sizes.add(solution.size)
        durations.append(elapsed / 1_000_000)
    if len(sizes) != 1:
        raise AssertionError(f"{name}: cardinalidades inconsistentes entre repetições: {sorted(sizes)}.")
    size = sizes.pop()
    if expected_size is not None and size != expected_size:
        raise AssertionError(f"{name}: cardinalidade {size}, ótimo esperado {expected_size}.")
    return Measurement(name, size, median(durations), min(durations), repetitions)


def compare(
    solvers: Mapping[str, Solver],
    instance: Instance,
    validate: Validator,
    repetitions: int = 5,
    expected_size: int | None = None,
) -> list[Measurement]:
    """Mede cada solver na mesma instância e exige cardinalidades iguais entre eles.

    Compara somente a cardinalidade: com múltiplos ótimos, as arestas podem diferir.
    """
    results = [measure(name, solver, instance, validate, repetitions, expected_size) for name, solver in solvers.items()]
    if len({m.size for m in results}) > 1:
        detail = ", ".join(f"{m.algorithm}={m.size}" for m in results)
        raise AssertionError(f"Cardinalidades diferentes entre algoritmos: {detail}.")
    return results
