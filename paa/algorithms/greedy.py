"""Emparelhamento máximo em árvores por algoritmo guloso — integrante 2.

Estratégia: poda sucessiva de folhas. Enquanto houver folhas na árvore restante,
retira-se uma folha v cujo único vizinho é u; se v e u estão livres, a aresta
(v, u) entra no emparelhamento. Em seguida v é removida da árvore. A prova de
otimalidade e a análise de complexidade estão em docs/guloso.md.

Detalhe de implementação: em vez de listas de adjacência, cada vértice guarda o
grau atual e o XOR dos rótulos dos vizinhos ainda presentes. Quando o grau é 1,
o XOR é exatamente o único vizinho restante; remover o vizinho w de u é
`neighbors_xor[u] ^= w`. Isso mantém tempo e espaço O(n), evita recursão (sem
limite de profundidade) e é mais rápido em Python do que montar n listas.
"""
from paa.models import Edge, Instance, Solution


def solve(instance: Instance) -> Solution:
    """Retorna um emparelhamento de cardinalidade máxima da árvore em O(n)."""
    n = instance.n
    degree = [0] * n
    neighbors_xor = [0] * n
    for u, v in instance.edges:
        degree[u] += 1
        degree[v] += 1
        neighbors_xor[u] ^= v
        neighbors_xor[v] ^= u

    # Pilha de folhas da árvore restante; cada vértice entra no máximo uma vez,
    # pois o grau só diminui e é empilhado apenas quando passa a valer 1.
    leaves = [v for v in range(n) if degree[v] == 1]
    matched = [False] * n
    matching: list[Edge] = []

    while leaves:
        v = leaves.pop()
        if degree[v] == 0:
            continue  # Último vértice restante: não há aresta para escolher.
        u = neighbors_xor[v]  # Único vizinho restante de v.
        if not matched[v] and not matched[u]:
            matched[v] = matched[u] = True
            matching.append((v, u))
        # Remove a folha v da árvore restante.
        neighbors_xor[u] ^= v
        degree[u] -= 1
        if degree[u] == 1:
            leaves.append(u)

    return Solution(tuple(matching))
