from __future__ import annotations
from typing import Callable, Dict
from players import HumanPlayer, StrategyPlayer, Player
import strategies as strat


class PolicyFactory:
    """Factory for strategy policies by name."""
    _registry: Dict[str, Callable] = {
        "cautious": strat.cautious_policy,
        "risky": strat.risky_policy,
        "catchup": strat.catchup_policy,
        
        "hold20": strat.cautious_policy,
        "hold30": strat.risky_policy,
    }

    @classmethod
    def create(cls, spec: str) -> Callable:
        """
        spec examples: 'cautious', 'risky', 'catchup', 'hold20', 'hold30'
        """
        key = spec.strip().lower()
        if key not in cls._registry:
            raise ValueError(f"Unknown policy '{spec}'. Options: {', '.join(cls._registry)}")
        return cls._registry[key]


class PlayerFactory:
    """
    Factory for players.

    Specs:
      - 'human:<Name>'         → HumanPlayer
      - 'strategy:<Name>:<Policy>' → StrategyPlayer with policy
        e.g., 'strategy:Bot1:cautious'
    """
    @classmethod
    def create(cls, spec: str) -> Player:
        if not spec:
            raise ValueError("Empty player spec.")
        parts = [p.strip() for p in spec.split(":")]
        kind = parts[0].lower()

        if kind == "human":
            name = parts[1] if len(parts) > 1 else "Human"
            return HumanPlayer(name=name)

        if kind == "strategy":
            name = parts[1] if len(parts) > 1 else "Bot"
            policy_name = parts[2] if len(parts) > 2 else "cautious"
            policy = PolicyFactory.create(policy_name)
            return StrategyPlayer(name=name, policy=policy)

        raise ValueError(f"Unknown player type '{kind}'. Use 'human' or 'strategy'.")
