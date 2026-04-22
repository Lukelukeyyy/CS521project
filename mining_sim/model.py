class SimulationConfig:
    def __init__(self, alpha, gamma, blocks, seed=None,
                 attacker_latency_ms=None, honest_latency_ms=None,
                 pool_size=None, experiment=None, sweep_value=None):
        # Store one simulation setup.
        self.alpha = alpha
        self.gamma = gamma
        self.blocks = blocks
        self.seed = seed
        self.attacker_latency_ms = attacker_latency_ms
        self.honest_latency_ms = honest_latency_ms
        self.pool_size = pool_size
        self.experiment = experiment
        self.sweep_value = sweep_value


class SimulationResult:
    def __init__(self, alpha, gamma, blocks, attacker_revenue, honest_revenue,
                 orphaned_blocks, relative_revenue, revenue_gain, profitable,
                 attacker_latency_ms=None, honest_latency_ms=None,
                 pool_size=None, experiment=None, sweep_value=None):
        # Store one simulation result.
        self.alpha = alpha
        self.gamma = gamma
        self.blocks = blocks
        self.attacker_revenue = attacker_revenue
        self.honest_revenue = honest_revenue
        self.orphaned_blocks = orphaned_blocks
        self.relative_revenue = relative_revenue
        self.revenue_gain = revenue_gain
        self.profitable = profitable
        self.attacker_latency_ms = attacker_latency_ms
        self.honest_latency_ms = honest_latency_ms
        self.pool_size = pool_size
        self.experiment = experiment
        self.sweep_value = sweep_value


def theoretical_threshold(gamma):
    # Calculate the minimum alpha needed for selfish mining to be profitable.
    if not 0 <= gamma <= 1:
        raise ValueError("gamma must be between 0 and 1")
    return (1 - gamma) / (3 - 2 * gamma)


def gamma_from_latency(attacker_latency_ms, honest_latency_ms, *, pool_size=0.0, base_gamma=0.5, ):
    # Convert latency and pool reach into an estimated gamma value.
    if attacker_latency_ms < 0 or honest_latency_ms < 0:
        raise ValueError("latencies must be non-negative")
    if not 0 <= pool_size <= 1:
        raise ValueError("pool_size must be between 0 and 1")

    total = max(attacker_latency_ms + honest_latency_ms, 1e-9)
    latency_edge = (honest_latency_ms - attacker_latency_ms) / total
    raw_gamma = base_gamma + 0.35 * latency_edge + 0.15 * pool_size
    return min(1.0, max(0.0, raw_gamma))
