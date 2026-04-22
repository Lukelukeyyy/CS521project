import json
from pathlib import Path

from mining_sim.model import theoretical_threshold


def write_html(path, rows):
    # Insert simulation data into the correct chart template.
    path.parent.mkdir(parents=True, exist_ok=True)

    experiment = "legacy"
    if rows:
        experiment = rows[0].experiment if rows[0].experiment is not None else "legacy"

    payload = [
        {
            "experiment": row.experiment if row.experiment is not None else "legacy",
            "sweepValue": row.sweep_value if row.sweep_value is not None else row.alpha,
            "alpha": row.alpha,
            "gamma": row.gamma,
            "threshold": theoretical_threshold(row.gamma),
            "relativeRevenue": row.relative_revenue,
            "gain": row.revenue_gain,
            "attackerLatency": row.attacker_latency_ms,
            "honestLatency": row.honest_latency_ms,
            "poolSize": row.pool_size,
            "profitable": row.profitable,
        }
        for row in rows
    ]

    if experiment == "latency_sweep":
        template_name = "chart_template_latency.html"
    else:
        template_name = "chart_template_legacy.html"

    template = Path(__file__).with_name(template_name).read_text(encoding="utf-8")
    html = template.replace("__DATA__", json.dumps(payload))
    html = html.replace("__EXPERIMENT__", experiment)
    path.write_text(html, encoding="utf-8")