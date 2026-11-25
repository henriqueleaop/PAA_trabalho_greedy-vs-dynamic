# Fundamentação teórica — ambos

## Definição do problema

Dada uma árvore não ponderada T = (V, E), com V = {0, …, n−1} e |E| = n − 1, um
**emparelhamento** é um subconjunto M ⊆ E em que nenhuma dupla de arestas
compartilha um vértice. O problema do **emparelhamento máximo** consiste em
encontrar M de cardinalidade |M| máxima.

- Entrada: `Instance(n, edges)` — árvore com vértices 0..n−1 (`paa/models.py`).
- Saída: `Solution(matching)` — arestas emparelhadas; `Solution.size` = |M|.
- Função objetivo: maximizar |M|. Pode haver vários emparelhamentos máximos.
- Tamanho da entrada: n (número de vértices); a árvore tem n − 1 arestas.

## Conceitos

- [ ] Árvore, raiz, folha, subárvore (definições usadas nas provas)
- [ ] Emparelhamento, vértice saturado/livre
- [ ] Emparelhamento maximal × máximo (exemplo que diferencia os dois)
- [ ] Limite superior trivial |M| ≤ ⌊n/2⌋ e casos em que não é atingido

## Paradigmas

- [ ] Programação dinâmica: subestrutura ótima e sobreposição de subproblemas
- [ ] Algoritmo guloso: escolha gulosa e subestrutura ótima
- [ ] Por que o problema em árvores admite ambas as abordagens

## Referências

- [ ] TODO
