import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
TEMPLATE_PATH = ROOT / "mining_sim" / "demo_dashboard_template.html"
OUTPUT_PATH = RESULTS_DIR / "demo_dashboard.html"


def load_rows(path):
    rows = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            parsed = {}
            for key, value in row.items():
                if value == "":
                    parsed[key] = None
                elif key == "experiment":
                    parsed[key] = value
                elif key == "profitable":
                    parsed[key] = value == "True"
                elif key in {
                    "attacker_revenue",
                    "honest_revenue",
                    "orphaned_blocks",
                    "blocks",
                }:
                    parsed[key] = int(float(value))
                else:
                    parsed[key] = float(value)
            rows.append(parsed)
    return rows


def main():
    payloads = {
        "__LEGACY_DATA__": json.dumps(load_rows(RESULTS_DIR / "exp1_legacy.csv")),
        "__LATENCY_DATA__": json.dumps(load_rows(RESULTS_DIR / "exp2_latency.csv")),
        "__POOL_DATA__": json.dumps(load_rows(RESULTS_DIR / "exp3_pool.csv")),
    }

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    for token, payload in payloads.items():
        template = template.replace(token, payload)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(template, encoding="utf-8")
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
