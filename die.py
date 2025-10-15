from __future__ import annotations
import random
from typing import Optional, Protocol, Callable


class Rollable(Protocol):
    def roll(self) -> int: ...


class Die:
    """Real subject: a standard six-sided die (configurable)."""
    def __init__(self, sides: int = 6, rng: Optional[random.Random] = None) -> None:
        if sides < 2:
            raise ValueError("Die must have >= 2 sides.")
        self.sides = sides
        self.rng = rng or random.Random()

    def roll(self) -> int:
        return self.rng.randint(1, self.sides)




class LoggingDieProxy:
    """
    Proxy that wraps a Rollable (e.g., Die) to add logging and roll statistics.

    Cross-cutting concerns (logging, metrics) belong here, not in Game logic.
    """
    def __init__(self, real_die: Rollable, logger: Callable[[str], None] = print) -> None:
        self._real = real_die
        self._logger = logger
        self.total_rolls = 0
        self.sum_of_faces = 0

    def roll(self) -> int:
        face = self._real.roll()
        self.total_rolls += 1
        self.sum_of_faces += face
        self._logger(f"[DieProxy] Roll #{self.total_rolls} → {face}")
        return face

    @property
    def average(self) -> float:
        return (self.sum_of_faces / self.total_rolls) if self.total_rolls else 0.0
