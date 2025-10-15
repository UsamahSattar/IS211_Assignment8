from __future__ import annotations
import argparse
import random
from factory import PlayerFactory
from die import Die, LoggingDieProxy
from game import Game


def build_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Pig (Proxy + Factory patterns)")
    ap.add_argument("--p1", default="human:Player1",
                    help="Player 1 spec (e.g., 'human:Alice' or 'strategy:Bot1:cautious')")
    ap.add_argument("--p2", default="strategy:Bot2:cautious",
                    help="Player 2 spec (e.g., 'human:Bob' or 'strategy:Bot2:risky')")
    ap.add_argument("--target", type=int, default=100, help="Winning score")
    ap.add_argument("--sides", type=int, default=6, help="Die sides")
    ap.add_argument("--seed", type=int, default=None, help="RNG seed (optional)")
    ap.add_argument("--nolog", action="store_true", help="Disable die logging proxy")
    ap.add_argument("--quiet", action="store_true", help="Suppress game announcements")
    return ap.parse_args()


def main() -> None:
    args = build_args()

    rng = random.Random(args.seed) if args.seed is not None else None
    real_die = Die(sides=args.sides, rng=rng)

    if args.nolog:
        die = real_die
        logger = print
    else:
        
        die_proxy = LoggingDieProxy(real_die)
        die = die_proxy
        def logger(msg: str) -> None:
            print(msg)

    p1 = PlayerFactory.create(args.p1)
    p2 = PlayerFactory.create(args.p2)

    announce = (lambda _: None) if args.quiet else print
    game = Game(p1=p1, p2=p2, target=args.target, die=die, announce=announce)
    winner = game.play()

    
    if isinstance(die, LoggingDieProxy):
        print(f"\n[DieProxy] Total rolls: {die.total_rolls}, Avg face: {die.average:.2f}")


if __name__ == "__main__":
    main()
