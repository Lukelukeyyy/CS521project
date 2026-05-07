import csv
from collections import defaultdict

from mining_sim.model import gamma_from_latency, theoretical_threshold


DEFAULT_WEIGHT_SETTINGS = [
    ("conservative", 0.25, 0.10),
    ("baseline", 0.35, 0.15),
    ("aggressive", 0.45, 0.20),
]


def read_results_csv(path):
    # Load simulator CSV rows as dictionaries with string values.
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def interpolate_zero_crossing(points):
    # Estimate the alpha value where revenue_gain crosses zero.
    if len(points) < 2:
        return None

    sorted_points = sorted(points)
    previous_alpha, previous_gain = sorted_points[0]

    if previous_gain == 0:
        return previous_alpha

    for alpha, gain in sorted_points[1:]:
        if gain == 0:
            return alpha

        crosses_zero = previous_gain < 0 < gain or previous_gain > 0 > gain
        if crosses_zero:
            weight = (0 - previous_gain) / (gain - previous_gain)
            return previous_alpha + weight * (alpha - previous_alpha)

        previous_alpha, previous_gain = alpha, gain

    return None


def estimate_threshold_residuals(rows):
    # Compare empirical alpha thresholds from Exp1 against the closed form.
    points_by_gamma = defaultdict(list)

    for row in rows:
        gamma = float(row.gamma if hasattr(row, "gamma") else row["gamma"])
        alpha = float(row.alpha if hasattr(row, "alpha") else row["alpha"])
        revenue_gain = float(
            row.revenue_gain if hasattr(row, "revenue_gain") else row["revenue_gain"]
        )
        points_by_gamma[gamma].append((alpha, revenue_gain))

    residual_rows = []
    for gamma in sorted(points_by_gamma):
        empirical_threshold = interpolate_zero_crossing(points_by_gamma[gamma])
        if empirical_threshold is None:
            continue

        closed_form_threshold = theoretical_threshold(gamma)
        residual_rows.append(
            {
                "gamma": gamma,
                "closed_form_threshold": closed_form_threshold,
                "empirical_threshold": empirical_threshold,
                "residual": empirical_threshold - closed_form_threshold,
            }
        )

    return residual_rows


def gamma_mapping_sensitivity(
    weight_settings=None,
    *,
    latency_attacker_min_ms=20.0,
    latency_attacker_max_ms=100.0,
    latency_honest_ms=100.0,
    latency_pool_size=0.20,
    pool_attacker_latency_ms=50.0,
    pool_honest_latency_ms=100.0,
    pool_min=0.0,
    pool_max=0.5,
):
    # Compute Exp2/Exp3 gamma and threshold endpoints for alternative weights.
    if weight_settings is None:
        weight_settings = DEFAULT_WEIGHT_SETTINGS

    rows = []
    for setting_name, latency_weight, pool_weight in weight_settings:
        exp2_gamma_fast = gamma_from_latency(
            latency_attacker_min_ms,
            latency_honest_ms,
            pool_size=latency_pool_size,
            latency_weight=latency_weight,
            pool_weight=pool_weight,
        )
        exp2_gamma_slow = gamma_from_latency(
            latency_attacker_max_ms,
            latency_honest_ms,
            pool_size=latency_pool_size,
            latency_weight=latency_weight,
            pool_weight=pool_weight,
        )
        exp3_gamma_low = gamma_from_latency(
            pool_attacker_latency_ms,
            pool_honest_latency_ms,
            pool_size=pool_min,
            latency_weight=latency_weight,
            pool_weight=pool_weight,
        )
        exp3_gamma_high = gamma_from_latency(
            pool_attacker_latency_ms,
            pool_honest_latency_ms,
            pool_size=pool_max,
            latency_weight=latency_weight,
            pool_weight=pool_weight,
        )

        rows.append(
            {
                "setting": setting_name,
                "latency_weight": latency_weight,
                "pool_weight": pool_weight,
                "exp2_gamma_fast_latency": exp2_gamma_fast,
                "exp2_gamma_slow_latency": exp2_gamma_slow,
                "exp2_threshold_fast_latency": theoretical_threshold(exp2_gamma_fast),
                "exp2_threshold_slow_latency": theoretical_threshold(exp2_gamma_slow),
                "exp3_gamma_low_pool": exp3_gamma_low,
                "exp3_gamma_high_pool": exp3_gamma_high,
                "exp3_threshold_low_pool": theoretical_threshold(exp3_gamma_low),
                "exp3_threshold_high_pool": theoretical_threshold(exp3_gamma_high),
            }
        )

    return rows


def write_dict_csv(path, rows):
    # Write analysis dictionaries to CSV.
    path.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        with path.open("w", newline="", encoding="utf-8") as handle:
            handle.write("")
        return

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            formatted_row = {}
            for key, value in row.items():
                if isinstance(value, float):
                    formatted_row[key] = f"{value:.6f}"
                else:
                    formatted_row[key] = value
            writer.writerow(formatted_row)


__all__ = [
    "DEFAULT_WEIGHT_SETTINGS",
    "estimate_threshold_residuals",
    "gamma_mapping_sensitivity",
    "interpolate_zero_crossing",
    "read_results_csv",
    "write_dict_csv",
]
