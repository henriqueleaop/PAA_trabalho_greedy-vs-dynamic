# Algoritmo guloso — integrante 2

Implementação: `paa/algorithms/greedy.py` (`solve(instance) -> Solution`).

## Ideia geral

Uma folha só pode ser emparelhada com seu único vizinho. O algoritmo poda a árvore
pelas folhas: a cada passo retira uma folha `v` da árvore restante e, se `v` e seu
vizinho `u` ainda estão livres, escolhe a aresta `(v, u)`. Cada decisão é local,
imediata e nunca é desfeita.

## Critério de escolha gulosa e ordem de processamento

- **Escolha gulosa:** ao retirar a folha `v` (vizinho `u`), emparelhar `(v, u)`
  sempre que ambos estiverem livres.
- **Ordem:** qualquer ordem de eliminação de folhas serve, isto é, qualquer ordem em
  que cada vértice, no momento de sua retirada, tenha no máximo um vizinho restante.
  A implementação usa uma pilha de folhas; um vértice entra na pilha quando seu grau
  restante cai para 1. O último vértice (grau restante 0) não tem aresta a escolher.
- **Desempates:** irrelevantes para a cardinalidade; ordens diferentes podem produzir
  emparelhamentos máximos diferentes.

### Representação sem listas de adjacência

Cada vértice guarda `degree[v]` (grau na árvore restante) e `neighbors_xor[v]` (XOR
dos rótulos dos vizinhos restantes). Como `x ^ x = 0`, quando `degree[v] = 1` o valor
`neighbors_xor[v]` é exatamente o único vizinho restante, e remover `v` da vizinhança
de `u` é `neighbors_xor[u] ^= v`. Assim a poda não precisa de listas de adjacência
nem de recursão (não há limite de profundidade) e, em medições locais com
n = 10⁶, foi 25–45% mais rápida que a variante com BFS sobre `build_adjacency`.

## Pseudocódigo

```text
GULOSO(n, E):
    para cada v em 0..n-1: grau[v] ← 0; viz[v] ← 0; emparelhado[v] ← falso
    para cada (u, v) em E:
        grau[u]++; grau[v]++; viz[u] ← viz[u] ⊕ v; viz[v] ← viz[v] ⊕ u
    P ← pilha com todos os v tais que grau[v] = 1
    M ← ∅
    enquanto P não vazia:
        v ← desempilha(P)
        se grau[v] = 0: continue            ▷ último vértice restante
        u ← viz[v]                          ▷ único vizinho restante
        se não emparelhado[v] e não emparelhado[u]:
            M ← M ∪ {(v, u)}; emparelhado[v] ← emparelhado[u] ← verdadeiro
        viz[u] ← viz[u] ⊕ v; grau[u]--      ▷ remove a folha v
        se grau[u] = 1: empilha(P, u)
    retorna M
```

## Prova de correção e otimalidade

Notação: ν(F) é a cardinalidade de um emparelhamento máximo da floresta F.

### A poda visita todos os vértices

Retirar uma folha de uma árvore resulta em uma árvore, então a árvore restante é
sempre conexa. Enquanto ela tem ao menos 2 vértices, possui ao menos 2 folhas, todas
na pilha (cada vértice é empilhado quando seu grau passa a 1; o grau só diminui,
então cada vértice é empilhado no máximo uma vez, exceto os de grau inicial 1, que
entram uma única vez na inicialização). Logo todo vértice é retirado como folha, e o
último é desempilhado com grau 0. Cada aresta `{v, u}` é examinada exatamente uma
vez: quando a primeira de suas pontas, `v`, é retirada.

Essa execução define uma **ordem de eliminação** v₁, …, vₙ e, para cada vᵢ exceto o
último, o **pai** p(vᵢ) = único vizinho restante no momento da retirada, que é
retirado depois de vᵢ. As arestas da árvore são exatamente {vᵢ, p(vᵢ)}, e o guloso
equivale a: para i = 1..n, se p(vᵢ) existe e vᵢ e p(vᵢ) estão livres, emparelhá-los.

Generalizamos para florestas: uma ordem v₁, …, vₖ com pais p(vᵢ) ∈ {vᵢ₊₁, …, vₖ} ∪ {nenhum}
em que as arestas da floresta são exatamente {vᵢ, p(vᵢ)}. Em qualquer ordem assim,
v₁ não tem filhos (filhos aparecem antes do pai), portanto é folha ou vértice isolado.

### Lema (escolha gulosa)

*Seja F uma floresta, v uma folha de F e u seu único vizinho. Existe um emparelhamento
máximo de F que contém (v, u).*

Seja M máximo. Se (v, u) ∈ M, pronto. Caso contrário, v está livre em M (seu único
vizinho é u). Se u também estivesse livre, M ∪ {(v, u)} seria um emparelhamento maior,
absurdo. Então u está emparelhado com algum w ≠ v, e M' = M − {(u, w)} ∪ {(v, u)} é um
emparelhamento (v estava livre e w fica livre) com |M'| = |M|, logo máximo e contém (v, u). ∎

### Subestrutura ótima

*Se v é folha de F com vizinho u, então ν(F) = 1 + ν(F − {u, v}).*

(≥) Um emparelhamento máximo de F − {u, v} mais (v, u) é emparelhamento de F.
(≤) Pelo lema, existe M máximo de F com (v, u) ∈ M; M − {(v, u)} não usa u nem v,
logo é emparelhamento de F − {u, v}, e ν(F − {u, v}) ≥ ν(F) − 1. ∎

### Teorema

*Para qualquer floresta F com ordem de eliminação como acima, o guloso devolve um
emparelhamento de cardinalidade ν(F).*

O resultado é um emparelhamento: só se escolhe (v, u) com ambos livres e ambos são
marcados. Para otimalidade, indução no número de vértices k.

- **Base (k = 0):** emparelhamento vazio, ν = 0.
- **Passo:** considere v₁.
  - *p(v₁) não existe:* v₁ é isolado; o guloso não o emparelha e nenhum emparelhamento
    o usa. A execução no restante coincide com a execução em F − {v₁}, com a ordem
    induzida, e ν(F) = ν(F − {v₁}). Pela hipótese de indução, o guloso é ótimo.
  - *u = p(v₁) existe:* no primeiro passo nada está emparelhado, então o guloso escolhe
    (v₁, u). Seja F' = F − {v₁, u} com a ordem induzida, onde os vértices cujo pai era
    u passam a não ter pai (essa ordem continua válida). A partir daí, as decisões
    do guloso em F coincidem com as do guloso em F': para w em F' com p(w) ≠ u, o
    teste depende só de vértices de F', em que os estados coincidem; para w com
    p(w) = u, o guloso em F encontra u emparelhado e não escolhe nada, exatamente
    como em F', onde w não tem pai. Assim |M| = 1 + |M'| = 1 + ν(F') = ν(F), pela
    hipótese de indução e pela subestrutura ótima. ∎

Aplicado a T com a ordem produzida pela pilha, o algoritmo devolve um emparelhamento
máximo.

## Complexidade

| Etapa | Tempo | Espaço |
| --- | --- | --- |
| Graus e XOR dos vizinhos (uma passada em n − 1 arestas) | Θ(n) | Θ(n): `degree`, `neighbors_xor` |
| Inicialização da pilha de folhas | Θ(n) | O(n): `leaves` |
| Poda: cada vértice é desempilhado no máximo uma vez, O(1) por vértice | Θ(n) | Θ(n): `matched` |
| Saída (no máximo ⌊n/2⌋ arestas) | O(n) | O(n): `matching` |
| **Total** | **Θ(n)** | **Θ(n)** |

Justificativa: há n − 1 arestas, cada uma lida uma vez; a pilha recebe cada vértice no
máximo uma vez (argumento acima), e cada iteração faz um número constante de operações
O(1) em listas. Não há ordenação nem recursão, então a pilha de chamadas é O(1),
independentemente da altura da árvore. Operações aritméticas e XOR são O(1) no
modelo RAM com palavras de Θ(log n) bits.

## Medições preliminares

`python -m paa benchmark --algorithm greedy --sizes 1000 10000 100000 1000000 --repeat 5 --seed 42`
(Python 3.12.10, Windows 11; mediana em ms). Resultados completos e comparação com a
PD ficam em `docs/comparacao.md`.

| Topologia | n = 10³ | n = 10⁴ | n = 10⁵ | n = 10⁶ |
| --- | --- | --- | --- | --- |
| path | 0,49 | 5,3 | 80 | 1409 |
| star | 0,47 | 4,6 | 64 | 877 |
| binary | 0,51 | 5,4 | 85 | 1477 |
| caterpillar | 0,56 | 5,8 | 85 | 1524 |
| broom | 0,50 | 5,1 | 77 | 1184 |
| random | 0,58 | 5,5 | 86 | 1528 |

O crescimento é aproximadamente linear até 10⁵; de 10⁵ para 10⁶ o fator fica entre
14× e 18×, compatível com efeitos de cache e alocação de memória do interpretador,
não com mudança de ordem assintótica.

## Checklist

- [x] `solve` implementado sem modificar a entrada
- [x] `python -m unittest discover -s tests -v` sem testes do guloso ignorados
- [x] `python -m paa solve --algorithm greedy` confere todos os casos
- [x] Comparação com força bruta em todas as árvores rotuladas com n ≤ 6 e aleatórias com n ≤ 10
