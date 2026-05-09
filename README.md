# Topic 6: Bitcoin Mining and Selfish Mining - CS521

This project simulates and analyzes Bitcoin selfish mining. It studies how attacker hash rate, tie-breaking behavior, network latency, and mining pool size affect whether selfish mining becomes profitable.

The simulator writes CSV files under `results/`. The main experiment CSVs can also be combined into an interactive dashboard:

```text
results/demo_dashboard.html
```

## Project Goals

Selfish mining is a strategy where an attacker withholds newly mined blocks, builds a private chain, and selectively publishes blocks to make honest miners waste work on orphaned blocks. The attacker is profitable when its accepted block share is higher than its hash-rate share.

This project focuses on three questions:

- How does the tie-breaking parameter `gamma` change the profitability threshold?
- How does lower attacker latency affect estimated `gamma` and relative revenue?
- How does mining pool size affect propagation advantage and profitability?

## Project Structure

```text
CS521project/
|-- README.md
|-- selfish_mining_sim.py              # Command-line entry point
|-- build_demo_dashboard.py            # Builds results/demo_dashboard.html
|-- mining_sim/
|   |-- __init__.py
|   |-- cli.py                         # Argument parsing and experiment routing
|   |-- model.py                       # Data models, threshold formula, gamma estimation
|   |-- simulation.py                  # Core selfish mining simulation and sweeps
|   |-- analysis.py                    # Threshold residual and sensitivity analysis
|   |-- output.py                      # CSV writer
|   `-- demo_dashboard_template.html   # Dashboard template
`-- results/
    |-- exp1_legacy.csv
    |-- exp2_latency.csv
    |-- exp3_pool.csv
    |-- threshold_residuals.csv
    |-- gamma_sensitivity.csv
    |-- selfish_mining_sweep.csv
    |-- demo_dashboard.html
    |-- exp1_gamma.png
    |-- exp2_latency.png
    `-- exp3_pool.png
```

## Quick Start

Run the three main experiments:

```bash
python selfish_mining_sim.py --experiment legacy --gammas 0,0.25,0.5,0.75 --alpha-step 0.01 --blocks 100000 --trials 8 --csv results/exp1_legacy.csv

python selfish_mining_sim.py --experiment latency --alpha 0.20 --honest-latency-ms 100 --pool-size 0.2 --latency-values 20,40,60,80,100 --blocks 100000 --trials 8 --csv results/exp2_latency.csv

python selfish_mining_sim.py --experiment pool --alpha 0.20 --attacker-latency-ms 50 --honest-latency-ms 100 --pool-values 0.0,0.1,0.2,0.3,0.4,0.5 --blocks 100000 --trials 8 --csv results/exp3_pool.csv
```

Build the dashboard:

```bash
python build_demo_dashboard.py
```

Then open:

```text
results/demo_dashboard.html
```

## Command-Line Usage

Main command:

```bash
python selfish_mining_sim.py --experiment <experiment> [options]
```

Supported experiment modes:

| Mode | Description |
| --- | --- |
| `legacy` | Experiment 1: sweep `alpha` across one or more `gamma` values |
| `latency` | Experiment 2: fix `alpha` and sweep attacker latency |
| `pool` | Experiment 3: fix `alpha` and sweep attacker pool size |
| `threshold_residuals` | Estimate empirical thresholds from Experiment 1 and compare them with the closed-form threshold |
| `sensitivity` | Analyze how alternative latency and pool weights affect estimated `gamma` |

Common options:

| Option | Default | Description |
| --- | --- | --- |
| `--experiment` | `legacy` | Experiment mode to run |
| `--blocks` | `100000` | Number of mining events per trial |
| `--trials` | `8` | Number of Monte Carlo trials per parameter setting |
| `--seed` | `521` | Random seed for reproducible runs |
| `--csv` | `results/selfish_mining_sweep.csv` | Output CSV path |
| `--alpha` | `0.30` | Fixed attacker hash-rate share for latency and pool experiments |
| `--alpha-step` | `0.01` | Step size for the `alpha` sweep in the legacy experiment |
| `--gammas` | `0,0.25,0.5,0.75` | Comma-separated `gamma` values for the legacy experiment |
| `--attacker-latency-ms` | none | Attacker block propagation latency in milliseconds |
| `--honest-latency-ms` | none | Honest network block propagation latency in milliseconds |
| `--latency-values` | none | Comma-separated attacker latency values for the latency experiment |
| `--pool-size` | `0.0` when needed | Attacker pool share for the latency experiment or derived legacy `gamma` |
| `--pool-values` | none | Comma-separated pool sizes for the pool experiment |
| `--input-csv` | `results/exp1_legacy.csv` | Input CSV for `threshold_residuals` |

## Experiment 1: Gamma Sweep

This experiment studies how selfish mining profitability changes with `gamma`, the fraction of honest miners that mine on the attacker branch during a public fork race.

```bash
python selfish_mining_sim.py --experiment legacy --gammas 0,0.25,0.5,0.75 --alpha-step 0.01 --blocks 100000 --trials 8 --csv results/exp1_legacy.csv
```

Output:

```text
results/exp1_legacy.csv
```

Dashboard view:

- X-axis: attacker hash-rate share `alpha`
- Y-axis: attacker relative revenue
- Break-even line: `relative_revenue = alpha`
- Theoretical profitability threshold for each `gamma`

The `legacy` mode can also derive a single `gamma` from latency values if both `--attacker-latency-ms` and `--honest-latency-ms` are provided.

## Experiment 2: Latency Sweep

This experiment fixes attacker hash-rate share `alpha` and sweeps attacker latency. The simulator converts latency advantage and pool size into an estimated `gamma`, then runs the selfish mining simulation.

```bash
python selfish_mining_sim.py --experiment latency --alpha 0.20 --honest-latency-ms 100 --pool-size 0.2 --latency-values 20,40,60,80,100 --blocks 100000 --trials 8 --csv results/exp2_latency.csv
```

Output:

```text
results/exp2_latency.csv
```

Rows from this mode are written with `experiment=latency_sweep` in the CSV.

## Experiment 3: Pool Size Sweep

This experiment fixes attacker hash-rate share and network latency, then sweeps attacker pool size. In this model, a larger pool improves propagation reach and increases the estimated `gamma`.

```bash
python selfish_mining_sim.py --experiment pool --alpha 0.20 --attacker-latency-ms 50 --honest-latency-ms 100 --pool-values 0.0,0.1,0.2,0.3,0.4,0.5 --blocks 100000 --trials 8 --csv results/exp3_pool.csv
```

Output:

```text
results/exp3_pool.csv
```

Rows from this mode are written with `experiment=pool_sweep` in the CSV.

## Additional Analysis

### Threshold Residuals

This mode reads Experiment 1 output, estimates the empirical profitability threshold, and compares it with the closed-form threshold.

```bash
python selfish_mining_sim.py --experiment threshold_residuals --input-csv results/exp1_legacy.csv --csv results/threshold_residuals.csv
```

Output columns:

```text
gamma, closed_form_threshold, empirical_threshold, residual
```

### Gamma Mapping Sensitivity

This mode evaluates alternative latency and pool weighting assumptions in `gamma_from_latency()`.

```bash
python selfish_mining_sim.py --experiment sensitivity --csv results/gamma_sensitivity.csv
```

Output columns:

```text
setting, latency_weight, pool_weight,
exp2_gamma_fast_latency, exp2_gamma_slow_latency,
exp2_threshold_fast_latency, exp2_threshold_slow_latency,
exp3_gamma_low_pool, exp3_gamma_high_pool,
exp3_threshold_low_pool, exp3_threshold_high_pool
```

## Main CSV Columns

The main experiment CSV files (`exp1_legacy.csv`, `exp2_latency.csv`, and `exp3_pool.csv`) contain these columns:

| Column | Meaning |
| --- | --- |
| `experiment` | Experiment label: `legacy`, `latency_sweep`, or `pool_sweep` |
| `sweep_value` | Swept value: `alpha` for legacy, attacker latency for latency sweep, pool size for pool sweep |
| `alpha` | Attacker hash-rate share |
| `gamma` | Fraction of honest miners that choose the attacker branch during a tie |
| `theoretical_threshold` | Closed-form profitability threshold |
| `attacker_latency_ms` | Attacker latency in milliseconds, when applicable |
| `honest_latency_ms` | Honest network latency in milliseconds, when applicable |
| `pool_size` | Attacker pool share, when applicable |
| `relative_revenue` | Attacker accepted-block share |
| `relative_revenue_std` | Sample standard deviation of relative revenue across trials |
| `relative_revenue_ci95` | 95% Student-t confidence interval half-width for relative revenue |
| `revenue_gain` | `relative_revenue - alpha` |
| `revenue_gain_std` | Sample standard deviation of revenue gain across trials |
| `revenue_gain_ci95` | 95% Student-t confidence interval half-width for revenue gain |
| `profitable` | Whether the attacker earns more than its hash-rate share |
| `attacker_revenue` | Accepted blocks credited to the attacker |
| `honest_revenue` | Accepted blocks credited to honest miners |
| `orphaned_blocks` | Blocks wasted through forks or orphaning |
| `trials` | Monte Carlo trials averaged for the row |
| `blocks` | Number of simulated mining events |

## Selfish Mining Model

The closed-form profitability condition used in this project is:

```text
alpha > (1 - gamma) / (3 - 2 * gamma)
```

Where:

- `alpha` is the attacker hash-rate share.
- `gamma` is the fraction of honest miners that mine on the attacker branch during a tie.

Examples:

| gamma | Threshold |
| --- | --- |
| `0.00` | `0.333` |
| `0.50` | `0.250` |
| `0.75` | `0.167` |

The project estimates `gamma` from latency and pool size with a simplified mapping:

```text
gamma = base_gamma + latency_weight * latency_edge + pool_weight * pool_size
latency_edge = (honest_latency_ms - attacker_latency_ms) / (honest_latency_ms + attacker_latency_ms)
```

By default, `base_gamma = 0.5`, `latency_weight = 0.35`, and `pool_weight = 0.15`. The final `gamma` is clipped to the range `[0.0, 1.0]`.

This is an experimental mapping for comparing propagation advantage and pool reach. It is not a full network-level Bitcoin propagation model.

## Dashboard

`build_demo_dashboard.py` reads:

```text
results/exp1_legacy.csv
results/exp2_latency.csv
results/exp3_pool.csv
```

It injects those CSV rows into `mining_sim/demo_dashboard_template.html` and writes:

```text
results/demo_dashboard.html
```

The dashboard summarizes:

- Experiment 1: profitability curves for different `gamma` values
- Experiment 2: attacker latency, estimated `gamma`, and relative revenue
- Experiment 3: pool size, estimated `gamma`, and relative revenue

## Key Takeaways

- Selfish mining can be profitable below 50% hash rate.
- Higher `gamma` lowers the theoretical profitability threshold.
- Lower propagation latency can increase the attacker's effective tie-breaking advantage.
- Larger pool size can improve propagation reach and increase relative revenue.
- Profitability occurs when `relative_revenue` is greater than `alpha`.
