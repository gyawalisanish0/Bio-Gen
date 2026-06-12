from app.config import TRAIT_BOUNDS
from app.simulation.genome import Genome


def test_random_genome_within_bounds():
    genome = Genome.random()
    for name, (lo, hi, _sigma) in TRAIT_BOUNDS.items():
        assert lo <= getattr(genome, name) <= hi


def test_mutate_stays_within_bounds():
    genome = Genome.random()
    for _ in range(200):
        genome = genome.mutate(mutation_rate=1.0)
        for name, (lo, hi, _sigma) in TRAIT_BOUNDS.items():
            assert lo <= getattr(genome, name) <= hi


def test_mutate_zero_rate_keeps_genome_unchanged():
    genome = Genome.random()
    assert genome.mutate(mutation_rate=0.0) == genome
