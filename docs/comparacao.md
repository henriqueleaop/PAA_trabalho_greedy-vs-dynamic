# Comparação experimental e conclusão — ambos

## Complexidade

| Abordagem | Tempo (pior caso) | Espaço auxiliar | Observações |
| --- | --- | --- | --- |
| Programação dinâmica | TODO | TODO | TODO |
| Guloso | TODO | TODO | TODO |

## Ambiente

- Processador / memória: TODO
- Sistema operacional: TODO
- Versão do Python: TODO
- Comando executado: `python -m paa benchmark --sizes ... --repeat ... --seed ... --csv ...`

## Metodologia

- Topologias: `path`, `star`, `binary` (balanceada), `caterpillar`, `broom`
  (desbalanceadas) e `random` (árvore recursiva aleatória), geradas por
  `paa/generators.py` com rótulos e ordem das arestas embaralhados pela semente.
- Tamanhos (n): TODO
- Repetições por medição e semente: TODO
- Métrica: mediana e mínimo do tempo de `solve()` em ms; geração e validação
  ficam fora da medição; o coletor de lixo é desativado durante cada execução.
- Correção: cada resposta é validada como emparelhamento, e as cardinalidades dos
  dois algoritmos são comparadas (as arestas escolhidas podem diferir).

## Resultados

| Topologia | n | Cardinalidade | PD mediana (ms) | Guloso mediana (ms) |
| --- | --- | --- | --- | --- |
| TODO | TODO | TODO | TODO | TODO |

TODO: gráfico tempo × n por topologia (opcional) e verificação do crescimento linear.

## Discussão

TODO: crescimento observado × complexidade teórica, constantes, influência da
topologia (profundidade, grau máximo), limitações da medição.

Igualdade de cardinalidades e testes são evidências experimentais, não provas de
otimalidade.

## Conclusão

TODO
