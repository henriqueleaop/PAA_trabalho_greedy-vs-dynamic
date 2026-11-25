# PAA — Emparelhamento máximo em árvores: Programação Dinâmica × Guloso

Duas soluções em Python para o mesmo problema, ambas ótimas, com tempo O(n) e
espaço O(n): uma por **programação dinâmica** e outra por **algoritmo guloso**.

## Problema

Dada uma árvore não ponderada com `n` vértices rotulados `0..n-1` e `n-1` arestas,
encontrar um subconjunto de arestas de **cardinalidade máxima** em que nenhuma dupla
de arestas selecionadas compartilhe um vértice (emparelhamento máximo).

```python
from paa.models import Instance
from paa.algorithms import dynamic_programming, greedy

tree = Instance(n=4, edges=((0, 1), (1, 2), (2, 3)))   # caminho 0-1-2-3
solution = greedy.solve(tree)       # mesma assinatura em dynamic_programming.solve
solution.matching                   # por exemplo ((0, 1), (2, 3)); orientação irrelevante
solution.size                       # 2
```

Pode haver vários emparelhamentos máximos: testes e benchmark comparam apenas a
**cardinalidade**, não as arestas escolhidas.

## Pré-requisitos

Python 3.10+. Somente a biblioteca padrão; nada a instalar. Execute a partir da raiz.

## Comandos

```bash
# Testes (os que dependem de algoritmos pendentes aparecem como "skipped")
python -m unittest discover -s tests -v

# Resolver os casos de data/cases.json e conferir com os ótimos conhecidos
python -m paa solve                          # ambos
python -m paa solve --algorithm dp           # só programação dinâmica
python -m paa solve --algorithm greedy       # só guloso

# Benchmark em árvores geradas (reproduzível pela semente)
python -m paa benchmark --algorithm both --sizes 1000 10000 100000 --repeat 5 --seed 42
python -m paa benchmark --topologies path random --sizes 1000000 --csv resultados.csv
```

Enquanto um algoritmo lançar `NotImplementedError`, os comandos com ele retornam
código 1 com a mensagem "Pendente"; use `--algorithm` para rodar só o outro.

## Estrutura

```text
paa/
  models.py                 # Instance, Solution, Case (dataclasses compartilhadas)
  problem.py                # build_adjacency, validate_instance, validate_matching, load_cases
  generators.py             # árvores reproduzíveis: path, star, binary, caterpillar, broom, random
  benchmark.py              # measure/compare: tempo de solve() + validação + checagem de cardinalidade
  __main__.py               # CLI: solve | benchmark
  algorithms/
    __init__.py             # ALGORITHMS = {"dp": ..., "greedy": ...}
    dynamic_programming.py  # TODO integrante 1
    greedy.py               # TODO integrante 2
data/
  cases.json                # casos pequenos com ótimo conhecido
tests/
  test_problem.py           # adjacência, entradas inválidas, emparelhamentos inválidos, cases.json
  test_generators.py        # validade, forma e reprodutibilidade das árvores geradas
  test_benchmark.py         # infraestrutura de medição (com solvers fictícios)
  test_algorithms.py        # ótimos conhecidos, árvore profunda, PD × guloso (ignorados se pendentes)
docs/
  fundamentacao-teorica.md  # ambos
  programacao-dinamica.md   # integrante 1
  guloso.md                 # integrante 2
  comparacao.md             # ambos: experimentos e conclusão
```

## Contrato

- `solve(instance: Instance) -> Solution`, idêntico nos dois módulos.
- A entrada é uma árvore já validada; `solve` não deve modificá-la e deve construir
  suas próprias estruturas (ex.: `build_adjacency`) dentro do tempo medido.
- `Solution.matching` é uma tupla de pares `(u, v)`; `validate_matching` verifica que
  cada par é aresta da árvore e que nenhum vértice se repete. Não verifica otimalidade.
- Caminhos com centenas de milhares de vértices excedem o limite de recursão padrão
  do Python; `test_deep_tree` usa `n = 200000`.

### Casos (`data/cases.json`)

Lista de objetos `{"name": str, "n": int, "edges": [[u, v], ...], "expected_size": int}`.
Os ótimos foram conferidos independentemente (força bruta em instâncias pequenas).
Incluem árvore unitária, caminhos, estrelas, binárias completas (balanceadas), lagarta,
vassoura, aranha e uma árvore desbalanceada com cauda longa. Além deles,
`test_algorithms.py` usa ótimos por fórmula fechada em árvores geradas
(caminho: ⌊n/2⌋; estrela: 1; lagarta com n par: n/2; vassoura).

### Benchmark

Para cada topologia e tamanho, gera uma instância (rótulos, ordem e orientação das
arestas embaralhados pela semente), executa cada algoritmo `--repeat` vezes e reporta
mediana e mínimo em ms. Geração, validação e I/O ficam fora da região cronometrada;
o coletor de lixo é desativado durante cada chamada. Com `both`, as cardinalidades
precisam coincidir. Memória é comparada analiticamente (não há medição empírica).

## Divisão de responsabilidades

| Integrante | Código | Documentação |
| --- | --- | --- |
| 1 | `paa/algorithms/dynamic_programming.py` | `docs/programacao-dinamica.md`: estados, recorrência, prova de otimalidade, complexidade |
| 2 | `paa/algorithms/greedy.py` | `docs/guloso.md`: critério guloso, prova de otimalidade, complexidade |
| Ambos | testes adicionais, execução do benchmark | `docs/fundamentacao-teorica.md`, `docs/comparacao.md` (experimentos e conclusão) |

Alterações no contrato compartilhado (`models.py`, `problem.py`) devem ser combinadas
antes. Sugestão de branches: `feature/dynamic-programming` e `feature/greedy`.
