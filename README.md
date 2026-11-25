# PAA — Programação Dinâmica × Guloso

Comparar duas estratégias para o mesmo problema de otimização. Ambas devem produzir soluções ótimas e ter complexidades de tempo semelhantes, preferencialmente da mesma ordem assintótica.

## Pré-requisitos

Python 3.10 ou superior. Não há dependências externas nem necessidade de instalar o projeto; execute os comandos a partir da raiz.

```bash
python -m unittest discover -s tests -v
python -m paa --help
python -m paa --cases data/cases.json --repeat 10
```

O último comando só produzirá medições depois da definição dos casos e implementação dos algoritmos e validadores. No scaffold, os testes de infraestrutura passam, e o teste de otimalidade fica explicitamente pendente.

## Divisão de responsabilidades

| Integrante | Código principal | Documentação |
| --- | --- | --- |
| 1 | `paa/algorithms/dynamic_programming.py` | `docs/programacao-dinamica.md` |
| 2 | `paa/algorithms/greedy.py` | `docs/guloso.md` |
| Ambos | Contrato, validadores, casos de teste e comparação | `docs/comparacao.md` |

## Estrutura

```text
paa/
  algorithms/
    dynamic_programming.py  # TODO integrante 1
    greedy.py               # TODO integrante 2
  models.py                 # Entrada e saída compartilhadas
  problem.py                # TODO regras e validação comuns
  benchmark.py              # Infraestrutura de comparação
  __main__.py               # CLI
data/
  cases.json                # TODO casos de teste
tests/
  test_algorithms.py        # Testes com ótimos conhecidos
  test_benchmark.py         # Testes da infraestrutura
docs/
  programacao-dinamica.md
  guloso.md
  comparacao.md
```

## Primeira etapa (em conjunto)

1. Escolher o problema e confirmar que há duas estratégias ótimas com complexidades comparáveis, sem trabalho artificial.
2. Definir o domínio, a medida de tamanho da entrada e a função objetivo (maximização ou minimização).
3. Especializar `Instance` e `Solution` em `paa/models.py` se necessário, preservando o contrato `solve(instance) -> Solution`. Caso mude o formato, adaptar o carregador e os testes.
4. Implementar `validate_instance` e `validate_solution` em `paa/problem.py`. A validação de solução deve verificar restrições e recalcular a função objetivo, não chamar os algoritmos para obter uma resposta.
5. Criar casos pequenos com ótimo conhecido independentemente, casos extremos e entradas maiores. Definir como representar instâncias inviáveis, se aplicável.
6. Cada integrante implementa seu algoritmo e documenta prova e complexidade. Integrar e comparar ao final.

## Contrato de casos

`data/cases.json` contém uma lista de objetos com `name` (texto), `data` (objeto específico do problema) e `expected_objective` (número ótimo conhecido independentemente, ou `null` quando desconhecido). Está vazio de propósito. Exemplo exclusivamente estrutural, não é um caso válido de um problema já escolhido:

```json
[
  {"name": "caso-pequeno", "data": {}, "expected_objective": null}
]
```

`Solution.objective` contém o valor da função objetivo e `Solution.decisions` contém as decisões da solução. O benchmark compara os objetivos, não a igualdade das decisões. Objetivos inteiros são comparados exatamente; floats usam tolerância de 1e-9 (ajustar à escala se o problema exigir).

## Benchmark

O CLI executa ambos os métodos em cada caso e apresenta o objetivo e a mediana do tempo de execução, em milissegundos. Cada repetição recebe uma cópia da mesma entrada. Cópia, leitura de arquivos e validação ficam fora da região cronometrada. A ordenação ou qualquer pré-processamento exigido pelo algoritmo deve ficar dentro de `solve`, salvo se o enunciado garantir entrada previamente processada.

A comparação de memória ainda é analítica (complexidade espacial); não há medição empírica de memória. Para experimentos finais, use várias escalas, repetições e entradas representativas e controle o ambiente. Objetivos iguais não provam que ambos são ótimos.

## Git (opcional)

Depois de iniciar o repositório e compartilhar o scaffold em `main`, cada integrante pode trabalhar em uma branch: `feature/dynamic-programming` e `feature/greedy`. Alterações no contrato compartilhado devem ser combinadas antes da implementação.
