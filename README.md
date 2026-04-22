# Topic 6: Bitcoin Mining and Selfish Mining

This project contains a simulator for Bitcoin selfish mining. It models the attacker hash-rate share, honest network tie-breaking behavior, latency-derived propagation advantage, and pool-size effects. The simulator writes a CSV data set and an HTML chart for presentation use.

---

## How to Run and View Results

After running the simulator, the results are saved as:

- CSV file (data)
- HTML file (visualization)

---

## Experiment 1: Gamma Sweep

This experiment studies how selfish mining profitability depends on the parameter gamma.

### Run

    python selfish_mining_sim.py --experiment legacy \
      --csv results/exp1_legacy.csv \
      --html results/exp1_legacy.html

### Output

- CSV: `results/exp1_legacy.csv`
- HTML: `results/exp1_legacy.html`

### Visualization

- X-axis: alpha (attacker hash rate)
- Y-axis: relative attacker revenue
- Includes:
  - simulated revenue curve
  - break-even line (y = x)
  - theoretical threshold

---

## Experiment 2: Latency Sweep

This experiment studies how network latency affects selfish mining.

Latency first changes gamma, and gamma then affects the attacker's revenue.

### Run

    python selfish_mining_sim.py --experiment latency \
      --alpha 0.30 \
      --honest-latency-ms 100 \
      --pool-size 0.2 \
      --latency-values 20,40,60,80,100 \
      --csv results/exp2_latency.csv \
      --html results/exp2_latency.html

### Output

- CSV: `results/exp2_latency.csv`
- HTML: `results/exp2_latency.html`

### Visualization

- Chart 1: latency → relative revenue
- Chart 2: latency → gamma

---

## How to Open the HTML Files

### Method 1 (Recommended)

    open results/exp1_legacy.html
    open results/exp2_latency.html

---

### Method 2 (Using a Local Server)

    cd /Users/dl/PycharmProjects/CS521project
    python -m http.server 8000

Then open:

- http://localhost:8000/results/exp1_legacy.html
- http://localhost:8000/results/exp2_latency.html

---

### Note

Directly double-clicking the HTML file may not work reliably in some browsers due to local file security restrictions. If that happens, use one of the methods above.

---

## Mining Economics Background

Bitcoin miners earn expected revenue roughly proportional to their share of the global hash rate. Difficulty adjusts every 2016 blocks so that the network returns toward a 10 minute block interval after hash rate changes.

Mining pools reduce payout variance by sharing rewards:

- **PPS**: pays a fixed amount per submitted share, shifting variance risk to the pool operator.
- **PPLNS**: pays according to recent submitted shares around an actual block, keeping more variance on miners and discouraging pool hopping.

Energy consumption matters because mining profit is driven by block rewards and fees minus electricity, hardware, cooling, and operational costs. Strategies that increase relative revenue can be economically meaningful even if they do not increase total network block production.

---

## Selfish Mining Model

Eyal and Sirer showed that a miner can withhold blocks and selectively publish them to make honest miners waste work on orphaned blocks.

### Parameters

- **alpha**: attacker hash-rate share  
- **gamma**: fraction of honest miners mining on attacker’s chain during a tie  
- **network latency**: used to estimate gamma  
- **pool size**: propagation advantage  

### Theoretical Threshold

    alpha > (1 - gamma) / (3 - 2 * gamma)

### Examples

- gamma = 0.00 → threshold ≈ 0.333  
- gamma = 0.50 → threshold ≈ 0.250  
- gamma = 1.00 → threshold ≈ 0.000  