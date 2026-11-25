"""Contrato compartilhado; especializar após a escolha do problema."""
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Instance:
    data: dict[str, Any]


@dataclass(frozen=True)
class Solution:
    objective: int | float
    decisions: Any  # TODO: definir representação de uma solução viável.


@dataclass(frozen=True)
class Case:
    name: str
    instance: Instance
    expected_objective: int | float | None = None
