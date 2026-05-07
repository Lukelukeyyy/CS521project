"""Selfish mining simulator package."""

from mining_sim.analysis import estimate_threshold_residuals
from mining_sim.model import SimulationConfig, SimulationResult, gamma_from_latency, theoretical_threshold
from mining_sim.simulation import run_trials, simulate_selfish_mining, sweep

__all__ = [
    "estimate_threshold_residuals",
    "SimulationConfig",
    "SimulationResult",
    "gamma_from_latency",
    "theoretical_threshold",
    "run_trials",
    "simulate_selfish_mining",
    "sweep",
]
