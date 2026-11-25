"""Contrato compartilhado de entrada e saída do emparelhamento máximo em árvores."""
from dataclasses import dataclass

Edge = tuple[int, int]
"""Aresta não direcionada entre dois vértices; a orientação (u, v) ou (v, u) é irrelevante."""


@dataclass(frozen=True)
class Instance:
    """Árvore não ponderada com vértices 0..n-1 e exatamente n-1 arestas."""

    n: int
    edges: tuple[Edge, ...] = ()


@dataclass(frozen=True)
class Solution:
    """Emparelhamento: arestas da árvore sem vértices em comum."""

    matching: tuple[Edge, ...]

    @property
    def size(self) -> int:
        """Cardinalidade do emparelhamento (valor da função objetivo)."""
        return len(self.matching)


@dataclass(frozen=True)
class Case:
    """Instância nomeada com cardinalidade ótima conhecida (ou None se desconhecida)."""

    name: str
    instance: Instance
    expected_size: int | None = None
