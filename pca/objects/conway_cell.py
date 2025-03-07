import numpy as np
from pca.cell import Cell
from pca.enum import Entity
import random

class ConwayCell(Cell):

    def __init__(self, state=0, x=0, y=0, z=0, model={}):
        super().__init__(Entity.CONWAY_CUBE, state, x, y, z, model)
        self.set_dead()

    def __copy__(self):
        new_cell = ConwayCell(state=self.state, x=self.x, y=self.y, z=self.z, model=self.model)
        return new_cell

    def render(self):
        # Render method for displaying the cell's face colors.
        return self.vertices, self.faces, self.colors
    
    def set_alive(self):
        self.colors = ConwayCell.get_alive_colors()
        self.state = 1

    def set_dead(self):
        self.colors = ConwayCell.get_death_colors()
        self.state = 0

    def step(self, new_grid, old_grid):
        # Get the grid dimensions
        rows, cols, layers = old_grid.shape

        # Count only horizontal live neighbors
        live_neighbors = self.count_live_neighbors(old_grid, rows, cols, layers)

        # Apply Conway's Game of Life rules (customized)
        if self.state == 1:  # If the cell is alive
            if live_neighbors < 2 or live_neighbors > 3:
                # Dies due to underpopulation or overpopulation
                cop = self.__copy__()
                cop.set_dead()
                new_grid[self.x, self.y, self.z] = cop
            else:
                # Stays alive
                # cop = self.__copy__()
                # cop.set_alive()
                # new_grid[self.x, self.y, self.z] = cop
                pass

        elif self.state == 0 and live_neighbors == 3:
            # Dead cell comes to life due to reproduction
            cop = self.__copy__()
            cop.set_alive()
            new_grid[self.x, self.y, self.z] = cop


    def count_live_neighbors(self, grid, rows, cols, layers):
        # Check only horizontal neighbors (no change in z-axis)
        directions = [(-1, -1, 0), (-1, 0, 0), (-1, 1, 0),
                    (0, -1, 0),            (0, 1, 0),
                    (1, -1, 0), (1, 0, 0), (1, 1, 0)]

        live_neighbors = 0
        for dx, dy, dz in directions:
            nx, ny, nz = self.x + dx, self.y + dy, self.z + dz
            if 0 <= nx < rows and 0 <= ny < cols and 0 <= nz < layers:
                neighbor = grid[nx][ny][nz]
                if neighbor is not None and neighbor.state == 1:
                    live_neighbors += 1
        return live_neighbors


    @staticmethod
    def get_alive_colors():
        # Assign alternating intensity values per cube face (ensuring each face has the same color)
        num_faces = 12 // 2  # 2 triangles per face
        face_colors = np.tile([18, 18, 18, 18, 18, 18], num_faces // 6 + 1)[:num_faces]

        # Repeat each color twice so both triangles of a face have the same intensity
        intensity_values = np.repeat(face_colors, 2)

        return intensity_values
    
    @staticmethod
    def get_death_colors():
        # Assign alternating intensity values per cube face (ensuring each face has the same color)
        num_faces = 12 // 2  # 2 triangles per face
        face_colors = np.tile([0, 0, 0, 0, 0, 0], num_faces // 6 + 1)[:num_faces]

        # Repeat each color twice so both triangles of a face have the same intensity
        intensity_values = np.repeat(face_colors, 2)

        return intensity_values
