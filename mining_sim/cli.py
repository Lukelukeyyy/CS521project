import argparse
from pathlib import Path

from mining_sim.model import gamma_from_latency, theoretical_threshold
from mining_sim.output import write_csv
from mining_sim.simulation import sweep
from mining_sim.visualization import write_html


def parse_gammas(raw):
    # Turn a comma-separated string into a list of gamma values.
    gammas = []

    for value in raw.split(","):
        value = value.strip()
        if value:
            gammas.append(float(value))

    if not gammas:
        raise argparse.ArgumentTypeError("at least one gamma is required")

    for gamma in gammas:
        if not 0 <= gamma <= 1:
            raise argparse.ArgumentTypeError("gamma values must be between 0 and 1")

    return gammas


def build_parser():
    # Define the command-line options for the simulator.
    parser = argparse.ArgumentParser(
        description="Simulate selfish mining profitability and generate a visualization."
    )
    parser.add_argument("--blocks", type=int, default=100000, help="mining events per trial")
    parser.add_argument("--trials", type=int, default=8, help="Monte Carlo trials per alpha")
    parser.add_argument("--alpha-step", type=float, default=0.01, help="sweep increment")
    parser.add_argument("--gammas", type=parse_gammas, default=parse_gammas("0,0.25,0.5,0.75"))
    parser.add_argument("--seed", type=int, default=521, help="random seed")
    parser.add_argument("--csv", type=Path, default=Path("results/selfish_mining_sweep.csv"))
    parser.add_argument("--html", type=Path, default=Path("results/selfish_mining_chart.html"))
    parser.add_argument("--pool-size", type=float, default=None, help="attacker pool share for latency mode")
    parser.add_argument("--attacker-latency-ms", type=float, default=None)
    parser.add_argument("--honest-latency-ms", type=float, default=None)
    return parser


def main():
    # Read user options, run the simulation, and write output files.
    parser = build_parser()
    args = parser.parse_args()

    gammas = args.gammas

    using_latency_mode = (
        args.attacker_latency_ms is not None or args.honest_latency_ms is not None
    )
    if using_latency_mode:
        if args.attacker_latency_ms is None or args.honest_latency_ms is None:
            parser.error("latency mode requires both --attacker-latency-ms and --honest-latency-ms")

        pool_size = 0.0 if args.pool_size is None else args.pool_size
        estimated_gamma = gamma_from_latency(
            args.attacker_latency_ms,
            args.honest_latency_ms,
            pool_size=pool_size,
        )
        gammas = [estimated_gamma]

    simulation_results = sweep(
        gammas=gammas,
        blocks=args.blocks,
        trials=args.trials,
        seed=args.seed,
        alpha_step=args.alpha_step,
    )
    write_csv(args.csv, simulation_results)
    write_html(args.html, simulation_results)

    print(f"wrote {args.csv}")
    print(f"wrote {args.html}")

    for gamma in gammas:
        threshold = theoretical_threshold(gamma)
        print(f"gamma={gamma:.3f} theoretical_threshold={threshold:.3f}")


__all__ = ["build_parser", "main", "parse_gammas"]
