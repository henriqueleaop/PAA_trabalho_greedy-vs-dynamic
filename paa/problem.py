"""Funções comuns às duas implementações: adjacência, validação e leitura de casos.

As validações são iterativas para suportar árvores profundas (por exemplo, caminhos
com 10^6 vértices) sem atingir o limite de recursão do Python.
"""
import json
from collections import deque
from pathlib import Path
from typing import Any

from paa.models import Case, Edge, Instance, Solution


def normalize_edge(u: int, v: int) -> Edge:
    """Representação canônica de uma aresta não direcionada: (menor, maior)."""
    return (u, v) if u < v else (v, u)


def build_adjacency(instance: Instance) -> list[list[int]]:
    """Lista de adjacência: adjacency[v] contém os vizinhos de v. Tempo e espaço O(n)."""
    adjacency: list[list[int]] = [[] for _ in range(instance.n)]
    for u, v in instance.edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    return adjacency


def _is_vertex(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _check_edge(edge: Any, n: int, label: str) -> Edge:
    """Verifica formato e intervalo de uma aresta e devolve sua forma canônica."""
    if not isinstance(edge, (tuple, list)) or len(edge) != 2:
        raise ValueError(f"{label} {edge!r} deve ser um par (u, v).")
    u, v = edge
    if not (_is_vertex(u) and _is_vertex(v)):
        raise ValueError(f"{label} {edge!r} deve conter vértices inteiros.")
    if not (0 <= u < n and 0 <= v < n):
        raise ValueError(f"{label} {edge!r} contém vértice fora de 0..{n - 1}.")
    if u == v:
        raise ValueError(f"{label} {edge!r} é um laço.")
    return normalize_edge(u, v)


def validate_instance(instance: Instance) -> None:
    """Rejeita com ValueError qualquer entrada que não seja uma árvore com vértices 0..n-1."""
    n = instance.n
    if not _is_vertex(n) or n < 1:
        raise ValueError("n deve ser um inteiro positivo.")
    if not isinstance(instance.edges, (tuple, list)):
        raise ValueError("edges deve ser uma sequência de pares.")
    if len(instance.edges) != n - 1:
        raise ValueError(f"Uma árvore com {n} vértices tem {n - 1} arestas, não {len(instance.edges)}.")
    seen: set[Edge] = set()
    for edge in instance.edges:
        key = _check_edge(edge, n, "Aresta")
        if key in seen:
            raise ValueError(f"Aresta {edge!r} repetida.")
        seen.add(key)
    # Com n-1 arestas, ser conexo equivale a ser acíclico.
    adjacency = build_adjacency(instance)
    visited = [False] * n
    visited[0] = True
    queue = deque([0])
    reached = 1
    while queue:
        for w in adjacency[queue.popleft()]:
            if not visited[w]:
                visited[w] = True
                reached += 1
                queue.append(w)
    if reached != n:
        raise ValueError("O grafo não é conexo (contém ciclo), portanto não é uma árvore.")


def validate_matching(instance: Instance, solution: Solution) -> None:
    """Verifica que a solução é um emparelhamento da árvore; rejeita com ValueError.

    Não verifica otimalidade: isso cabe às provas e à comparação com ótimos conhecidos.
    Pressupõe que a instância já foi validada.
    """
    if not isinstance(solution, Solution):
        raise ValueError("O algoritmo deve retornar um objeto Solution.")
    if not isinstance(solution.matching, (tuple, list)):
        raise ValueError("Solution.matching deve ser uma sequência de pares.")
    tree_edges = {normalize_edge(u, v) for u, v in instance.edges}
    used = [False] * instance.n
    for edge in solution.matching:
        key = _check_edge(edge, instance.n, "Aresta emparelhada")
        if key not in tree_edges:
            raise ValueError(f"Aresta emparelhada {edge!r} não pertence à árvore.")
        for vertex in key:
            if used[vertex]:
                raise ValueError(f"Vértice {vertex} aparece em mais de uma aresta emparelhada.")
            used[vertex] = True


def instance_from_dict(data: dict[str, Any]) -> Instance:
    """Converte {"n": int, "edges": [[u, v], ...]} em Instance (sem validar)."""
    return Instance(data["n"], tuple(tuple(edge) for edge in data.get("edges", [])))


def load_cases(path: Path) -> list[Case]:
    """Lê casos no formato descrito no README e valida cada instância."""
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("O arquivo de casos deve conter uma lista.")
    cases = []
    for row in rows:
        case = Case(row["name"], instance_from_dict(row), row.get("expected_size"))
        validate_instance(case.instance)
        cases.append(case)
    return cases
