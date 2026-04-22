"""CSV output for simulator results."""

import csv
from pathlib import Path

from mining_sim.model import SimulationResult, theoretical_threshold


def write_csv(path, rows):
    """Write simulation rows as a presentation-friendly CSV file."""
    # Save all simulation results in table form.
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "alpha",
                "gamma",
                "theoretical_threshold",
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
                    "alpha": f"{row.alpha:.6f}",
                    "gamma": f"{row.gamma:.6f}",
                    "theoretical_threshold": f"{theoretical_threshold(row.gamma):.6f}",
                    "relative_revenue": f"{row.relative_revenue:.6f}",
                    "revenue_gain": f"{row.revenue_gain:.6f}",
                    "profitable": row.profitable,
                    "attacker_revenue": row.attacker_revenue,
                    "honest_revenue": row.honest_revenue,
                    "orphaned_blocks": row.orphaned_blocks,
                    "blocks": row.blocks,
                }
            )
