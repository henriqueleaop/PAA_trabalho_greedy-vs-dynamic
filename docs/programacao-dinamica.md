# Programação dinâmica — integrante 1

Implementação: `paa/algorithms/dynamic_programming.py` (`solve(instance) -> Solution`).

## Ideia geral

Uma árvore $T = (V, E)$ com $|V| = n$ vértices torna-se acíclica e direcionada ao ser
enraizada arbitrariamente no vértice `0`. Nesse formato, cada subárvore enraizada em um
vértice `u` interage com o restante da árvore exclusivamente por meio do próprio `u`
(que pode ou não ser emparelhado com seu pai). Assim, o emparelhamento máximo em `T`
decompõe-se em subproblemas independentes sobre as subárvores dos filhos de `u`,
resolvidos de baixo para cima (*bottom-up*) sem recursão.

## Estados e casos base

Para cada vértice `u` da árvore enraizada em `0`, definimos dois estados sobre a
subárvore $T_u$ enraizada em `u`:

- `dp0[u]`: cardinalidade máxima de um emparelhamento em $T_u$ quando `u` **não** é
  emparelhado com nenhum de seus filhos (logo `u` fica livre dentro de $T_u$, podendo
  eventualmente se emparelhar com seu pai fora de $T_u$).
- `dp1[u]`: cardinalidade máxima de um emparelhamento em $T_u$ quando `u` **é**
  emparelhado com exatamente um de seus filhos `v`.

Além disso, mantemos `chosen_child[u]` para registrar qual filho `v*` maximiza `dp1[u]`
quando vale a pena emparelhar `u` com um filho (`dp1[u] > dp0[u]`), ou `-1` caso
contrário.

### Casos base

- **Árvore trivial ($n \le 1$):** não há arestas; `solve()` retorna `Solution(())` em
  $O(1)$.
- **Folha `u` (sem filhos na árvore enraizada):**
  `dp0[u] = 0`, `dp1[u] = 0` e `chosen_child[u] = -1`.

## Recorrência e ordem de avaliação

Seja $C(u)$ o conjunto de filhos de `u` na árvore enraizada em `0`.

1. **Caso `u` livre em $T_u$ (`dp0[u]`):**
   Como `u` não usa nenhuma aresta para seus filhos, cada subárvore $T_v$ ($v \in C(u)$)
   pode escolher independentemente seu melhor emparelhamento (com `v` livre ou
   emparelhado com algum neto):
   $$\text{dp0}[u] = \sum_{v \in C(u)} \max(\text{dp0}[v], \text{dp1}[v])$$

2. **Caso `u` emparelhado com um filho `v` (`dp1[u]`):**
   Se escolhemos a aresta `(u, v)` para algum $v \in C(u)$, então `v` não pode se
   emparelhar com nenhum de seus próprios filhos (contribuindo com `dp0[v]` em $T_v$),
   enquanto todos os outros filhos $w \in C(u) \setminus \{v\}$ continuam livres para
   contribuir com $\max(\text{dp0}[w], \text{dp1}[w])$:
   $$\text{dp1}[u] = \max_{v \in C(u)} \Big(\text{dp0}[u] - \max(\text{dp0}[v], \text{dp1}[v]) + 1 + \text{dp0}[v]\Big)$$

   Em termos de ganho marginal, emparelhar `u` com `v` acrescenta
   $\text{ganho}(v) = 1 + \text{dp0}[v] - \max(\text{dp0}[v], \text{dp1}[v])$ sobre
   `dp0[u]`. Se existir algum filho `v` com `dp0[v] >= dp1[v]`, o ganho máximo é `1`
   (`dp1[u] = dp0[u] + 1 > dp0[u]`) e registramos `chosen_child[u] = v`; caso
   contrário, o ganho máximo é `0` (`dp1[u] == dp0[u]`) e mantemos `chosen_child[u] = -1`.

- **Ordem de avaliação:** realizamos uma busca iterativa com pilha explícita a partir da
  raiz `0` para preencher `parent[v]` e a lista `order` em pré-ordem. Percorrer
  `reversed(order)` garante que todos os filhos de `u` são avaliados antes de `u`
  (pós-ordem *bottom-up*). A resposta ótima global é $\max(\text{dp0}[0], \text{dp1}[0])$.

## Reconstrução do emparelhamento

Para obter as arestas do emparelhamento ótimo (e não apenas a cardinalidade), fazemos
uma travessia iterativa *top-down* a partir da raiz `0` usando uma pilha explícita de
pares `(u, can_match_child)`, iniciada com `(0, True)`:

- `can_match_child = True` indica que `u` não foi emparelhado com seu pai e pode
  escolher `chosen_child[u]` (se `chosen_child[u] != -1`).
- `can_match_child = False` indica que `u` já foi emparelhado com seu pai, devendo
  seguir o estado `dp0[u]` (nenhum filho emparelhado com `u`).

Ao desempilhar `(u, can_match_child)`:
1. Definimos `match_v = chosen_child[u]` se `can_match_child` for verdadeiro, ou `-1`
   caso contrário.
2. Se `match_v != -1`, adicionamos a aresta `(u, match_v)` ao emparelhamento `M`.
3. Para cada filho `v` de `u`, empilhamos `(v, v != match_v)`: apenas o filho escolhido
   `match_v` recebe `False` (pois já foi saturado pela aresta `(u, match_v)`), e todos
   os demais filhos recebem `True`.

Ao final, retornamos `Solution(tuple(M))`.

## Pseudocódigo

```text
PD_ARVORE(n, E):
    se n <= 1: retorna ()
    adj ← CONSTRUIR_ADJACENCIA(n, E)
    pai[0..n-1] ← -1
    ordem ← []
    P ← [0]                                  ▷ pilha explícita para enraizamento
    enquanto P não vazia:
        u ← desempilha(P)
        anexa u em ordem
        para cada v em adj[u]:
            se v != pai[u]:
                pai[v] ← u
                empilha(P, v)

    dp0[0..n-1] ← 0; dp1[0..n-1] ← 0; escolhido[0..n-1] ← -1
    para cada u em reverso(ordem):           ▷ ordem bottom-up
        total ← 0; melhor_ganho ← -1; melhor_filho ← -1
        para cada v em adj[u]:
            se v == pai[u]: continue
            melhor_v ← max(dp0[v], dp1[v])
            total ← total + melhor_v
            ganho ← 1 + dp0[v] - melhor_v
            se ganho > melhor_ganho:
                melhor_ganho ← ganho
                melhor_filho ← v
        dp0[u] ← total
        se melhor_filho != -1:
            dp1[u] ← total + melhor_ganho
            se dp1[u] > dp0[u]:
                escolhido[u] ← melhor_filho

    M ← []
    R ← [(0, verdadeiro)]                    ▷ pilha explícita de reconstrução
    enquanto R não vazia:
        (u, pode_emparelhar) ← desempilha(R)
        match_v ← escolhido[u] se pode_emparelhar senão -1
        se match_v != -1:
            anexa (u, match_v) em M
        para cada v em adj[u]:
            se v != pai[u]:
                empilha(R, (v, v != match_v))
    retorna tuple(M)
```

## Prova de otimalidade

Seja $T$ uma árvore enraizada em `0` e $\nu(T_u)$ a cardinalidade máxima de um
emparelhamento na subárvore $T_u$. Denotemos por $\nu_0(T_u)$ a cardinalidade máxima
entre os emparelhamentos de $T_u$ que deixam `u` livre, e por $\nu_1(T_u)$ a
cardinalidade máxima entre os que emparelham `u` com algum filho (ou $0$ se $u$ é
folha). Claramente $\nu(T_u) = \max(\nu_0(T_u), \nu_1(T_u))$.

### Subestrutura ótima

Em qualquer emparelhamento $M$ de $T_u$:
- **Caso 1 (`u` não é incidente a nenhuma aresta de $M$ em $T_u$):** as arestas de $M$
  particionam-se entre as subárvores disjuntas $T_v$ ($v \in C(u)$) sem restrições entre
  elas. Como subárvores distintas não compartilham vértices, o máximo é atingido
  tomando um emparelhamento máximo independente em cada $T_v$:
  $\nu_0(T_u) = \sum_{v \in C(u)} \nu(T_v)$.
- **Caso 2 (`u` é emparelhado com um único filho $v \in C(u)$):** a aresta `(u, v)`
  contribui com $1$, obriga `v` a não usar outra aresta dentro de $T_v$ (logo $M \cap E(T_v)$
  tem cardinalidade no máximo $\nu_0(T_v)$), e deixa cada outro filho $w \neq v$ livre
  para atingir $\nu(T_w)$ em $T_w$. O máximo sobre todas as escolhas possíveis de $v$ é
  $\nu_1(T_u) = \max_{v \in C(u)} \big(1 + \nu_0(T_v) + \sum_{w \in C(u)\setminus\{v\}} \nu(T_w)\big)$.

### Indução estrutural na altura da subárvore

Provamos por indução na altura $h(u)$ da subárvore $T_u$ que $\text{dp0}[u] = \nu_0(T_u)$
e $\text{dp1}[u] = \nu_1(T_u)$:

- **Base ($h(u) = 0$, isto é, `u` é folha):** $E(T_u) = \emptyset$, logo
  $\nu_0(T_u) = \nu_1(T_u) = 0$. O algoritmo inicializa `dp0[u] = 0` e `dp1[u] = 0`,
  valendo a igualdade.
- **Passo indutivo ($h(u) > 0$):** suponha que, para todo filho $v \in C(u)$ (que possui
  $h(v) < h(u)$), valem $\text{dp0}[v] = \nu_0(T_v)$ e $\text{dp1}[v] = \nu_1(T_v)$,
  implicando $\max(\text{dp0}[v], \text{dp1}[v]) = \nu(T_v)$. Como `reversed(order)`
  processa cada filho `v` antes do pai `u`, as transições calculam:
  $$\text{dp0}[u] = \sum_{v \in C(u)} \max(\text{dp0}[v], \text{dp1}[v]) = \sum_{v \in C(u)} \nu(T_v) = \nu_0(T_u)$$
  e, reescrevendo $\sum_{w \neq v} \nu(T_w) = \text{dp0}[u] - \max(\text{dp0}[v], \text{dp1}[v])$:
  $$\text{dp1}[u] = \max_{v \in C(u)} \big(\text{dp0}[u] - \max(\text{dp0}[v], \text{dp1}[v]) + 1 + \text{dp0}[v]\big) = \nu_1(T_u).$$

Na raiz `0`, portanto, $\max(\text{dp0}[0], \text{dp1}[0]) = \nu(T_0) = \nu(T)$. A
reconstrução *top-down* respeita exatamente a restrição de que um vértice emparelhado com
seu pai (`can_match_child = False`) não é emparelhado com nenhum filho, garantindo um
emparelhamento válido de cardinalidade $\nu(T)$.

## Complexidade

| Etapa | Tempo | Espaço |
| --- | --- | --- |
| Construção da adjacência (`build_adjacency`) | $O(n)$ | $O(n)$ |
| Enraizamento iterativo (pilha explícita + `parent` + `order`) | $O(n)$ | $O(n)$ |
| Cálculo *bottom-up* de `dp0`, `dp1` e `chosen_child` | $O(n)$ | $O(n)$ |
| Reconstrução iterativa *top-down* do emparelhamento `M` | $O(n)$ | $O(n)$ |
| **Total** | **$O(n)$** | **$O(n)$** |

Justificativa: uma árvore possui $|E| = n - 1$ arestas, logo a soma dos graus é
$\sum_{u \in V} \deg(u) = 2(n - 1) = O(n)$. Tanto o enraizamento quanto o laço
*bottom-up* e a reconstrução *top-down* visitam cada vértice exatamente uma vez e
percorrem cada lista de adjacência uma única vez, resultando em tempo total $O(n)$. As
estruturas auxiliares (`adjacency`, `parent`, `order`, `dp0`, `dp1`, `chosen_child`,
pilhas e lista `matching`) ocupam no máximo $O(n)$ palavras de memória. Além disso, como
toda travessia utiliza pilhas explícitas em vez de recursão, a profundidade máxima de
chamada em Python é constante $O(1)$ — evitando `RecursionError` mesmo em caminhos
degenerados com $n = 200\,000$ (nos testes) ou $n = 1\,000\,000$ (nos benchmarks).

## Checklist

- [x] `solve` implementado sem modificar a entrada
- [x] `python -m unittest discover -s tests -v` sem testes de PD ignorados
- [x] `python -m paa solve --algorithm dp` confere todos os casos
