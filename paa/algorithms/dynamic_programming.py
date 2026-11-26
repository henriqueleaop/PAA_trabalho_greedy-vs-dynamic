"""Emparelhamento máximo em árvores por programação dinâmica — integrante 1.

Estratégia: enraizamento iterativo no vértice 0 seguido de programação dinâmica
bottom-up com dois estados por vértice (`dp0[u]` quando `u` não se emparelha
com nenhum filho; `dp1[u]` quando `u` se emparelha com exatamente um filho) e
reconstrução iterativa top-down das arestas escolhidas. Toda a execução usa
pilhas explícitas (sem recursão) para evitar `RecursionError` em árvores
profundas, mantendo tempo O(n) e espaço O(n).
"""
from paa.models import Edge, Instance, Solution
from paa.problem import build_adjacency


def solve(instance: Instance) -> Solution:
    """Retorna um emparelhamento de cardinalidade máxima da árvore em O(n).

    Requisitos: solução ótima, tempo O(n) e espaço O(n). A entrada já é uma árvore
    válida (vértices 0..n-1); construir a adjacência faz parte do tempo medido
    (ver paa.problem.build_adjacency). A entrada não deve ser modificada.
    """
    n = instance.n
    if n <= 1:
        return Solution(())

    adjacency = build_adjacency(instance)

    # Enraizamento iterativo a partir de 0; `reversed(order)` garante ordem bottom-up.
    parent = [-1] * n
    order: list[int] = []
    stack = [0]
    while stack:
        u = stack.pop()
        order.append(u)
        pu = parent[u]
        for v in adjacency[u]:
            if v != pu:
                parent[v] = u
                stack.append(v)

    dp0 = [0] * n
    dp1 = [0] * n
    chosen_child = [-1] * n

    for u in reversed(order):
        pu = parent[u]
        total_free = 0
        best_gain = -1
        best_child = -1
        for v in adjacency[u]:
            if v == pu:
                continue
            child_best = dp0[v] if dp0[v] >= dp1[v] else dp1[v]
            total_free += child_best
            gain = 1 + dp0[v] - child_best
            if gain > best_gain:
                best_gain = gain
                best_child = v
        dp0[u] = total_free
        if best_child != -1:
            dp1[u] = total_free + best_gain
            if dp1[u] > dp0[u]:
                chosen_child[u] = best_child

    # Reconstrução iterativa top-down: `can_match_child` indica se `u` está livre.
    matching: list[Edge] = []
    recon_stack: list[tuple[int, bool]] = [(0, True)]
    while recon_stack:
        u, can_match_child = recon_stack.pop()
        pu = parent[u]
        match_v = chosen_child[u] if can_match_child else -1
        if match_v != -1:
            matching.append((u, match_v))
        for v in adjacency[u]:
            if v != pu:
                recon_stack.append((v, v != match_v))

    return Solution(tuple(matching))
