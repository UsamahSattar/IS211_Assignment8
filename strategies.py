from __future__ import annotations


def cautious_policy(my: int, opp: int, tt: int, target: int) -> str:
    
    if my + tt >= target:
        return "h"
    return "h" if tt >= 20 else "r"


def risky_policy(my: int, opp: int, tt: int, target: int) -> str:
    
    if my + tt >= target:
        return "h"
    return "h" if tt >= 30 else "r"


def catchup_policy(my: int, opp: int, tt: int, target: int) -> str:
    
    gap = opp - my
    threshold = 30 if gap >= 25 else 20
    if my + tt >= target:
        return "h"
    return "h" if tt >= threshold else "r"
