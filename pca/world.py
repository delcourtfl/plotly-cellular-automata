from pca.cell import Cell
from pca.objects.terrain import Terrain
from pca.objects.rabbit import Rabbit
from pca.objects.magic_terrain import MagicTerrain
from pca.objects.conway_cell import ConwayCell
from pca.objects.colorful_terrain import ColorfulTerrain
from pca.display.renderer import Renderer

from pca.display.models import ModelLoader
from pca.enum import Entity
import numpy as np

class World:
    def __init__(self, max_x=10, max_y=10, max_z=10):
        """
        Initializes the Cellular Automaton World with 3D grid size.
        
        :param grid_size: A tuple representing the grid's size (rows, columns, depth).
        """
        self.grid_size = (
            max_x, 
            max_y,
            max_z
        )
        self.loader = ModelLoader()

        max_x, max_y, max_z = self.grid_size[:3]

        # Create a 3D grid for storing Cell objects
        self.grid = np.empty((max_x, max_y, max_z), dtype=object)

        self.renderer = Renderer(self.grid, self.grid_size)

    def _is_within_bounds(self, x, y, z):
        return (
            0 <= x < self.grid.shape[0] and 
            0 <= y < self.grid.shape[1] and 
            0 <= z < self.grid.shape[2]
        )

    def get_cell(self, x, y, z):
        if self._is_within_bounds(x, y, z):
            return self.grid[x, y, z]
        raise IndexError("Indices out of bounds")
        
    def set_cell(self, x, y, z, element):
        if self._is_within_bounds(x, y, z):
            self.grid[x, y, z] = element
        else:
            raise IndexError("Indices out of bounds")
    
    def set_terrain(self, enum, x, y, z):
        terrain = self.create_entity(enum, x, y, z)
        self.grid[x, y, z] = terrain


    def set_entity(self, enum, x, y, z):
        entity = self.create_entity(enum, x, y, z)
        self.grid[x, y, z] = entity


    def set_terrain_with_heightmap(self, enum, height_map):
        np_map = np.array(height_map)
        for x, y in np.ndindex(np_map.shape):
            value = np_map[x, y]
            for z in range(value):
                self.set_terrain(enum, x, y, z)


    def set_entity_with_dict(self, entity_dict):
        for (x, y) in entity_dict:
            if not 0 <= x < self.grid_size[0] or not 0 <= y < self.grid_size[1]:
                continue
            enum = entity_dict.get((x, y), None)
            z = self.find_lowest_z(x, y)
            self.set_entity(enum, x, y, z)


    def find_lowest_z(self, x, y):
        """Find the lowest unoccupied z position for a given (x, y)."""
        max_z = self.grid_size[2]
        for z in range(max_z):
            if self.grid[x, y, z] is None:  # If the position is unoccupied
                return z
        return max_z - 1
    

    def create_entity(self, entity, x, y, z, model=None):
        match entity:
            case Entity.RABBIT:
                model = self.loader.get_model(entity)
                return Rabbit(state=0, x=x, y=y, z=z, model=model)
            case Entity.TERRAIN:
                model = self.loader.get_model(entity)
                return Terrain(state=0, x=x, y=y, z=z, model=model)
            case Entity.COLORFUL_TERRAIN:
                model = self.loader.get_model(entity)
                return ColorfulTerrain(state=0, x=x, y=y, z=z, model=model)
            case Entity.MAGIC_TERRAIN:
                model = self.loader.get_model(entity)
                return MagicTerrain(state=0, x=x, y=y, z=z, model=model)
            case Entity.CONWAY_CUBE:
                model = self.loader.get_model(entity)
                return ConwayCell(state=0, x=x, y=y, z=z, model=model)
            case _:
                return None
        return None
    

    def evolve(self):
        """
        Evolves the cellular automaton world. This is just a placeholder.
        You can implement rule-based evolution logic here.
        """
        new_grid = self.grid.copy()

        mask = self.grid != None
        indices = np.argwhere(mask)

        for x, y, z in indices:
            self.grid[x, y, z].step(new_grid, self.grid)

        self.grid = new_grid


    def generate_frame(self):
        self.renderer.set_elements(self.grid, self.grid_size)
        self.renderer.add_frame()
            
                
    def render(self):
        """
        Render the automaton world in 3D.
        """
        return self.renderer.render()