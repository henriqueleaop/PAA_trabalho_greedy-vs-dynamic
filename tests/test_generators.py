"""Geração reproduzível de árvores."""
import unittest

from paa.generators import TOPOLOGIES, generate
from paa.problem import build_adjacency, validate_instance


class GeneratorTests(unittest.TestCase):
    def test_generates_valid_trees(self):
        for topology in TOPOLOGIES:
            for n in (1, 2, 3, 10, 101):
                with self.subTest(topology=topology, n=n):
                    instance = generate(topology, n, seed=7)
                    self.assertEqual(instance.n, n)
                    validate_instance(instance)

    def test_reproducible(self):
        for topology in TOPOLOGIES:
            with self.subTest(topology=topology):
                self.assertEqual(generate(topology, 200, seed=1), generate(topology, 200, seed=1))

    def test_seed_changes_instance(self):
        self.assertNotEqual(generate("random", 200, seed=1), generate("random", 200, seed=2))

    def test_shapes(self):
        degrees = lambda instance: sorted(len(a) for a in build_adjacency(instance))
        self.assertEqual(degrees(generate("path", 6)), [1, 1, 2, 2, 2, 2])
        self.assertEqual(degrees(generate("star", 6)), [1, 1, 1, 1, 1, 5])
        self.assertEqual(degrees(generate("binary", 7)), [1, 1, 1, 1, 2, 3, 3])
        self.assertEqual(degrees(generate("caterpillar", 8)), [1, 1, 1, 1, 2, 2, 3, 3])
        self.assertEqual(degrees(generate("broom", 7)), [1, 1, 1, 1, 2, 2, 4])

    def test_invalid_arguments(self):
        with self.assertRaises(ValueError):
            generate("ciclo", 10)
        with self.assertRaises(ValueError):
            generate("path", 0)


if __name__ == "__main__":
    unittest.main()
