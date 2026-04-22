"""CSV output for simulator results."""

import csv

from mining_sim.model import theoretical_threshold

def write_csv(path, rows):
    """Write simulation rows as a presentation-friendly CSV file."""
    # Save all simulation results in table form.
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "experiment",
                "sweep_value",
                "alpha",
                "gamma",
                "theoretical_threshold",
                "attacker_latency_ms",
                "honest_latency_ms",
                "pool_size",
                "relative_revenue",
                "revenue_gain",
                "profitable",
                "attacker_revenue",
                "honest_revenue",
                "orphaned_blocks",
                "blocks",
            ],
        )
        writer.writeheader()

        for row in rows:
            writer.writerow(
                {
                    # Use legacy when experiment is not explicitly stored.
                    "experiment": row.experiment if row.experiment is not None else "legacy",

                    # In legacy sweep, use alpha as the sweep value.
                    "sweep_value": f"{row.sweep_value:.6f}" if row.sweep_value is not None else f"{row.alpha:.6f}",

                    "alpha": f"{row.alpha:.6f}",
                    "gamma": f"{row.gamma:.6f}",
                    "theoretical_threshold": f"{theoretical_threshold(row.gamma):.6f}",

                    "attacker_latency_ms": f"{row.attacker_latency_ms:.6f}" if row.attacker_latency_ms is not None else "",
                    "honest_latency_ms": f"{row.honest_latency_ms:.6f}" if row.honest_latency_ms is not None else "",
                    "pool_size": f"{row.pool_size:.6f}" if row.pool_size is not None else "",

                    "relative_revenue": f"{row.relative_revenue:.6f}",
                    "revenue_gain": f"{row.revenue_gain:.6f}",
                    "profitable": row.profitable,
                    "attacker_revenue": row.attacker_revenue,
                    "honest_revenue": row.honest_revenue,
                    "orphaned_blocks": row.orphaned_blocks,
                    "blocks": row.blocks,
                }
            )