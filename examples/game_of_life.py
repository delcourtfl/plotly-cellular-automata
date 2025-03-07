from pca.world import World
from pca.enum import Entity
from pca.objects.conway_cell import ConwayCell
import random
import time
import plotly.graph_objects as go

# python -m examples.game_of_life
def game_of_life():
    # Set a seed for reproducibility
    random.seed(42)

    length = 14
    width = 14
    height = 4

    height_map = [[1 for _ in range(width)] for _ in range(length)]

    entities_map = {}

    print("World init")
    world = World(length, width, height)
    world.set_terrain_with_heightmap(Entity.CONWAY_CUBE, height_map)
    world.set_entity_with_dict(entities_map)

    coordinates = [
        (4, 4), (4, 5), (4, 6),
        (5, 4), (5, 5), (5, 6),
        (6, 4), (6, 5), (6, 6),

        (7, 7), (7, 8), (7, 9),
        (8, 7), (8, 8), (8, 9),
        (9, 7), (9, 8), (9, 9),
    ]

    # Iterate through coordinates
    for x, y in coordinates:
        cell: ConwayCell = world.get_cell(x, y, 0)
        cell.set_alive()


    start_time = time.time()

    world.generate_frame()
    for i in range(100):
        print(i)
        world.evolve()
        world.generate_frame()

    end_time = time.time()
    print(f"processing execution time: {end_time - start_time:.5f} seconds")

    
    start_time = time.time()
    fig: go.Figure = world.render()
    end_time = time.time()
    print(f"rendering execution time: {end_time - start_time:.5f} seconds")

    # fig.show()
    fig.write_html(
        'plotly_output.html', 
        auto_open=True,
        auto_play=True,
        animation_opts={
            "frame": {"duration": 100},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": 100, "easing": "linear"},
        }
    )

if __name__ == "__main__":
    game_of_life()