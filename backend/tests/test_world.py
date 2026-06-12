from app.config import WORLD_HEIGHT, WORLD_WIDTH
from app.simulation.world import World


def test_world_dimensions():
    world = World()
    assert world.width == WORLD_WIDTH
    assert world.height == WORLD_HEIGHT
    assert len(world.tiles) == WORLD_HEIGHT
    assert len(world.tiles[0]) == WORLD_WIDTH


def test_food_regrows_up_to_max():
    world = World()
    for row in world.tiles:
        for tile in row:
            tile.food = 0

    world.step()

    for row in world.tiles:
        for tile in row:
            assert 0 <= tile.food <= tile.max_food


def test_passable_neighbors_are_in_bounds_and_passable():
    world = World()
    for row in world.tiles:
        for tile in row:
            for nx, ny in world.passable_neighbors(tile.x, tile.y):
                assert world.in_bounds(nx, ny)
                assert world.get(nx, ny).passable


def test_best_food_tile_in_range_finds_richest_neighbor():
    world = World()
    for row in world.tiles:
        for tile in row:
            tile.food = 0

    world.tiles[5][5].food = 5.0
    best = world.best_food_tile_in_range(4, 4, vision=2)

    assert best == (5, 5)
