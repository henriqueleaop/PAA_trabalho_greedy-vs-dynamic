"""Implementações independentes, ambas com a assinatura solve(instance: Instance) -> Solution."""
from collections.abc import Callable

from paa.algorithms import dynamic_programming, greedy
from paa.models import Instance, Solution

Solver = Callable[[Instance], Solution]

ALGORITHMS: dict[str, Solver] = {
    "dp": dynamic_programming.solve,
    "greedy": greedy.solve,
}
LABELS = {"dp": "Programação dinâmica", "greedy": "Guloso"}
