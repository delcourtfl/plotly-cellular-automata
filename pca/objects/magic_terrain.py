from pca.cell import Cell
import numpy as np
from pca.enum import Entity
import random

class MagicTerrain(Cell):

    def __init__(self, state=0, x=0, y=0, z=0, model={}):
        super().__init__(Entity.MAGIC_TERRAIN, state, x, y, z, model)

        self.colors = MagicTerrain.get_colors()

    def __copy__(self):
        new_cell = MagicTerrain(state=self.state, x=self.x, y=self.y, z=self.z, model=self.model)
        return new_cell

    def render(self):
        # print(self.colors)
        return self.vertices, self.faces, self.colors
    
    def step(self, new_grid, old_grid):
        # Get the grid dimensions (assuming grid is 3D)
        rows, cols, layers = old_grid.shape
        
        action = random.choice([0, 1, 2])

        if action == 0:
            if self.z > 0 and (self.z == layers - 1 or old_grid[self.x][self.y][self.z + 1] is None):
                new_grid[self.x][self.y][self.z] = None
        elif action == 1:
            if self.z < layers - 1 and old_grid[self.x][self.y][self.z + 1] is None:
                cop = self.__copy__()
                cop.z = self.z + 1
                new_grid[self.x][self.y][self.z + 1] = cop
        else:
            # new_grid[new_x][new_y][new_z] = self
            pass
    
    @staticmethod
    def get_colors():
        # Assign alternating intensity values per cube face (ensuring each face has the same color)
        num_faces = 12 // 2 # 2 triangles per face
        face_colors = np.tile([0, 1, 2, 3, 4, 5], num_faces // 6 + 1)[:num_faces]

        # Repeat each color twice so both triangles of a face have the same intensity
        intensity_values = np.repeat(face_colors, 2)

        return intensity_values
    