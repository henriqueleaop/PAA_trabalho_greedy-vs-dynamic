"""Geração reproduzível de árvores para testes e benchmark.

A forma da árvore é determinada pela topologia; em seguida, rótulos dos vértices,
ordem e orientação das arestas são embaralhados com uma semente. Assim, nenhum
algoritmo pode depender de o vértice 0 ser raiz ou de as arestas virem ordenadas.
"""
import random

from paa.models import Edge, Instance


def _path(n: int, rng: random.Random) -> list[Edge]:
    return [(i - 1, i) for i in range(1, n)]


def _star(n: int, rng: random.Random) -> list[Edge]:
    return [(0, i) for i in range(1, n)]


def _binary(n: int, rng: random.Random) -> list[Edge]:
    """Árvore binária completa (layout de heap): balanceada, altura ⌊log2 n⌋."""
    return [((i - 1) // 2, i) for i in range(1, n)]


def _caterpillar(n: int, rng: random.Random) -> list[Edge]:
    """Espinha (caminho) com ⌈n/2⌉ vértices; cada folha pende de um vértice da espinha."""
    spine = (n + 1) // 2
    return [(i - 1, i) for i in range(1, spine)] + [(i - spine, i) for i in range(spine, n)]


def _broom(n: int, rng: random.Random) -> list[Edge]:
    """Cabo (caminho) com ⌈n/2⌉ vértices e as demais folhas presas à sua extremidade."""
    handle = (n + 1) // 2
    return [(i - 1, i) for i in range(1, handle)] + [(handle - 1, i) for i in range(handle, n)]


def _random(n: int, rng: random.Random) -> list[Edge]:
    """Árvore recursiva aleatória: o pai de i é sorteado uniformemente entre 0..i-1."""
    return [(rng.randrange(i), i) for i in range(1, n)]


GENERATORS = {
    "path": _path,
    "star": _star,
    "binary": _binary,
    "caterpillar": _caterpillar,
    "broom": _broom,
    "random": _random,
}
TOPOLOGIES = tuple(GENERATORS)


def generate(topology: str, n: int, seed: int = 0) -> Instance:
    """Gera uma árvore com n vértices; mesma (topologia, n, semente) produz a mesma instância."""
    if topology not in GENERATORS:
        raise ValueError(f"Topologia desconhecida: {topology!r}. Opções: {', '.join(TOPOLOGIES)}.")
    if n < 1:
        raise ValueError("n deve ser positivo.")
    rng = random.Random(f"{seed}:{topology}:{n}")
    edges = GENERATORS[topology](n, rng)
    labels = list(range(n))
    rng.shuffle(labels)
    relabeled = [(labels[u], labels[v]) if rng.random() < 0.5 else (labels[v], labels[u]) for u, v in edges]
    rng.shuffle(relabeled)
    return Instance(n, tuple(relabeled))
