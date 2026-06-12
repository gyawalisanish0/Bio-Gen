"""Genome representation and mutation logic for evolvable organism traits."""

from __future__ import annotations

import random
from dataclasses import asdict, dataclass

from app.config import TRAIT_BOUNDS


@dataclass(frozen=True)
class Genome:
    size: float
    speed: float
    vision: float
    metabolism: float
    fertility: float

    @classmethod
    def random(cls) -> "Genome":
        """Create a genome with each trait sampled uniformly from its bounds."""
        return cls(**{name: random.uniform(lo, hi) for name, (lo, hi, _sigma) in TRAIT_BOUNDS.items()})

    def mutate(self, mutation_rate: float) -> "Genome":
        """Return a new genome where each trait independently mutates with
        probability ``mutation_rate``, using Gaussian noise clamped to bounds."""
        values = asdict(self)
        for name, (lo, hi, sigma) in TRAIT_BOUNDS.items():
            if random.random() < mutation_rate:
                values[name] = _clamp(values[name] + random.gauss(0, sigma), lo, hi)
        return Genome(**values)

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))
