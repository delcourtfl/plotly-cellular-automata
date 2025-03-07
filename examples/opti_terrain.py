from pca.world import World
from pca.enum import Entity
import random
import time
import plotly.graph_objects as go

def opti_terrain():
    # Set a seed for reproducibility
    random.seed(42)

    length = 800
    width = 800
    height = 3

    height_map = [[random.randint(1, height) for _ in range(width)] for _ in range(length)]

    entities_map = {}

    print("World init")
    world = World(length, width, height)
    world.set_terrain_with_heightmap(Entity.COLORFUL_TERRAIN, height_map)
    world.set_entity_with_dict(entities_map)

    start_time = time.time()

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
    opti_terrain()