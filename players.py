from __future__ import annotations
from dataclasses import dataclass, field
from typing import Protocol, Callable


class Policy(Protocol):
    def __call__(self, my_score: int, opp_score: int, turn_total: int, target: int) -> str: ...


@dataclass
class Player:
    name: str
    score: int = 0

    def reset(self) -> None:
        self.score = 0

    def choose_action(self, turn_total: int, opponent_score: int, target: int) -> str:
        raise NotImplementedError


class HumanPlayer(Player):
    def choose_action(self, turn_total: int, opponent_score: int, target: int) -> str:
        while True:
            raw = input(
                f"[{self.name}] Turn={turn_total} | You={self.score} | Opp={opponent_score} "
                "(r)oll or (h)old? "
            ).strip().lower()
            if raw in ("r", "h"):
                return raw
            print("Please enter 'r' or 'h'.")


@dataclass
class StrategyPlayer(Player):
    policy: Policy = field(default=None)  

    def choose_action(self, turn_total: int, opponent_score: int, target: int) -> str:
        return self.policy(self.score, opponent_score, turn_total, target)
