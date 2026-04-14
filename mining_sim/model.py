class SimulationConfig:
    def __init__(self, alpha, gamma, blocks, seed=None):
        # Store one simulation setup.
        self.alpha = alpha
        self.gamma = gamma
        self.blocks = blocks
        self.seed = seed


class SimulationResult:
    def __init__(self, alpha, gamma, blocks, attacker_revenue, honest_revenue, orphaned_blocks, relative_revenue,revenue_gain,profitable):

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

