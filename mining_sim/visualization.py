import json
from pathlib import Path

from mining_sim.model import SimulationResult, theoretical_threshold


def write_html(path, rows):
    # Insert simulation data into the chart template.
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [
        {
            "alpha": row.alpha,
            "gamma": row.gamma,
            "threshold": theoretical_threshold(row.gamma),
            "relativeRevenue": row.relative_revenue,
            "gain": row.revenue_gain,
        }
        for row in rows
    ]
    template = Path(__file__).with_name("chart_template.html").read_text(encoding="utf-8")
    path.write_text(template.replace("__DATA__", json.dumps(payload)), encoding="utf-8")
