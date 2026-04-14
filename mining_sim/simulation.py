import random

from mining_sim.model import SimulationConfig, SimulationResult

# -------------- selfish mining simulator ---------------------
def validate_config(config):
    # Check whether the simulation parameters are valid.
    if not 0 < config.alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    if not 0 <= config.gamma <= 1:
        raise ValueError("gamma must be between 0 and 1")
    if config.blocks <= 0:
        raise ValueError("blocks must be positive")


def resolve_public_race(config, random_number_generator, mining_events,
                         attacker_revenue, honest_revenue, orphaned_blocks):
    # Handle the fork race when lead == 1.
    if mining_events >= config.blocks:
        # No time to resolve race, attacker keeps block.
        attacker_revenue += 1
        return mining_events, attacker_revenue, honest_revenue, orphaned_blocks, True

    # One more block is mined to resolve the fork.
    mining_events += 1
    race_random_number = random_number_generator.random()

    attacker_finds_race_block = race_random_number < config.alpha
    honest_mines_on_attacker_branch = (race_random_number < config.alpha + (1 - config.alpha) * config.gamma)

    if attacker_finds_race_block:
        # Attacker wins both blocks.
        attacker_revenue += 2
        orphaned_blocks += 1
    elif honest_mines_on_attacker_branch:
        # Honest mines on attacker chain.
        attacker_revenue += 1
        honest_revenue += 1
        orphaned_blocks += 1
    else:
        # Honest wins both blocks.
        honest_revenue += 2
        orphaned_blocks += 1

    return mining_events, attacker_revenue, honest_revenue, orphaned_blocks, False


def handle_honest_block(config, random_number_generator, private_chain_lead, mining_events,
                        attacker_revenue, honest_revenue, orphaned_blocks):
    # Update the state after the honest network finds a block.
    should_break = False

    if private_chain_lead == 0:
        # No private chain, honest gets reward.
        honest_revenue += 1

    elif private_chain_lead == 1:
        (mining_events, attacker_revenue, honest_revenue, orphaned_blocks, should_break) \
            = resolve_public_race(
            config, random_number_generator, mining_events,
            attacker_revenue, honest_revenue, orphaned_blocks)

        # Race resolved, reset lead.
        private_chain_lead = 0

    elif private_chain_lead == 2:
        # Attacker publishes 2-block lead.
        attacker_revenue += 2
        orphaned_blocks += 1
        private_chain_lead = 0

    else:
        # Publish one block to stay ahead.
        attacker_revenue += 1
        orphaned_blocks += 1
        private_chain_lead -= 1

    return (private_chain_lead, mining_events, attacker_revenue,
            honest_revenue, orphaned_blocks, should_break)


def build_simulation_result(config, private_chain_lead, attacker_revenue, honest_revenue, orphaned_blocks):
    # Add the remaining private blocks and compute final metrics.
    attacker_revenue += private_chain_lead
    accepted_blocks = attacker_revenue + honest_revenue
    relative_revenue = attacker_revenue / accepted_blocks if accepted_blocks else 0.0
    revenue_gain = relative_revenue - config.alpha

    return SimulationResult(alpha=config.alpha, gamma=config.gamma, blocks=config.blocks,
            attacker_revenue=attacker_revenue, honest_revenue=honest_revenue, orphaned_blocks=orphaned_blocks,
            relative_revenue=relative_revenue, revenue_gain=revenue_gain, profitable=revenue_gain > 0)


def simulate_selfish_mining(config):
    # Simulate one attacker and the honest network mining blocks.
    validate_config(config)

    random_number_generator = random.Random(config.seed)

    # lead means: attacker private chain length - public chain length.
    private_chain_lead = 0
    attacker_revenue = 0
    honest_revenue = 0
    orphaned_blocks = 0
    mining_events = 0

    while mining_events < config.blocks:
        # Decide who finds the block.
        attacker_found_block = random_number_generator.random() < config.alpha
        mining_events += 1

        if attacker_found_block:
            # Attacker withholds block.
            private_chain_lead += 1
            continue

        (private_chain_lead, mining_events, attacker_revenue, honest_revenue, orphaned_blocks, should_break,) \
            = handle_honest_block(config,random_number_generator,
                                private_chain_lead, mining_events,
                                attacker_revenue, honest_revenue, orphaned_blocks)

        # Stop if race cannot be resolved.
        if should_break:
            break

    return build_simulation_result(config, private_chain_lead, attacker_revenue,
                                   honest_revenue, orphaned_blocks)

