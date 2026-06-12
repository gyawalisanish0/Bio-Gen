from app.simulation.engine import SimulationConfig, SimulationEngine


def test_engine_initial_population():
    engine = SimulationEngine(SimulationConfig(population_size=10))

    assert len(engine.organisms) == 10
    assert engine.tick == 0
    assert len(engine.stats_history) == 1


def test_engine_step_advances_tick_and_records_stats():
    engine = SimulationEngine(SimulationConfig(population_size=5))

    engine.step()

    assert engine.tick == 1
    assert len(engine.stats_history) == 2


def test_engine_population_survives_many_ticks():
    engine = SimulationEngine(SimulationConfig(population_size=12, mutation_rate=0.2))

    for _ in range(100):
        engine.step()

    # Extinction triggers an automatic respawn, so population is never zero.
    assert len(engine.organisms) > 0


def test_reset_restores_initial_population_size():
    engine = SimulationEngine(SimulationConfig(population_size=8))

    for _ in range(10):
        engine.step()
    engine.reset(SimulationConfig(population_size=8))

    assert engine.tick == 0
    assert len(engine.organisms) == 8
    assert len(engine.stats_history) == 1
