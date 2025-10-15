from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable
from players import Player
from die import Rollable


@dataclass
class Game:
    p1: Player
    p2: Player
    target: int = 100
    die: Rollable = field(default=None)          
    announce: Callable[[str], None] = print     

    def play(self) -> Player:
        self.p1.reset(); self.p2.reset()
        current, other = self.p1, self.p2
        self.announce(f"Starting Pig to {self.target}: {self.p1.name} vs {self.p2.name}\n")

        while True:
            turn_total = 0
            self.announce(f"— {current.name}'s turn —")
            while True:
                action = current.choose_action(turn_total, other.score, self.target)
                if action == "h":
                    current.score += turn_total
                    self.announce(f"{current.name} holds (+{turn_total}) → {current.score}\n")
                    break
                # action == "r"
                face = self.die.roll()
                self.announce(f"{current.name} rolled {face}.")
                if face == 1:
                    self.announce(f"Pig! {current.name} scores 0 this turn.\n")
                    turn_total = 0
                    break
                turn_total += face
                self.announce(f"Turn total: {turn_total} (Game: {current.score})")

            if current.score >= self.target:
                self.announce(f"🎉 {current.name} wins with {current.score}!")
                return current

            current, other = other, current
