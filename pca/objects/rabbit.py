from pca.cell import Cell
import numpy as np
import trimesh
import plotly.graph_objects as go
from pca.enum import Entity
import random

class Rabbit(Cell):

    def __init__(self, state=0, x=0, y=0, z=0, model={}):
        super().__init__(Entity.RABBIT, state, x, y, z, model)

    def render(self):

        norm_vertices = self.normalize_vertices_to_floor(self.vertices)
        norm_vertices = norm_vertices + (self.x, self.y, self.z)

        return norm_vertices, self.faces, self.vertex_colors
    
    def step(self, new_grid, old_grid):
        # Get the grid dimensions (assuming grid is 3D)
        rows, cols, layers = old_grid.shape
        possible_moves = []

        # Define relative movement directions (up, down, left, right, forward, backward)
        directions = [
            (-1, 0, 0),  # Move left (x - 1)
            (1, 0, 0),   # Move right (x + 1)
            (0, -1, 0),  # Move up (y - 1)
            (0, 1, 0),   # Move down (y + 1)
            (0, 0, -1),  # Move backward (z - 1)
            (0, 0, 1),   # Move forward (z + 1)
        ]
        
        # Check each direction for an empty space
        for dx, dy, dz in directions:
            new_x, new_y, new_z = self.x + dx, self.y + dy, self.z + dz
            # Ensure the new position is within bounds
            if 0 <= new_x < rows and 0 <= new_y < cols and 0 <= new_z < layers:
                # Check if the position is empty (None) and terrain is valid if moving down
                if old_grid[new_x][new_y][new_z] is None:
                    possible_moves.append((new_x, new_y, new_z))
        
        # Move to a random empty space if available
        if possible_moves:
            new_x, new_y, new_z = random.choice(possible_moves)
            new_grid[self.x][self.y][self.z] = None  # Clear old position
            new_grid[new_x][new_y][new_z] = self  # Move rabbit
            self.x, self.y, self.z = new_x, new_y, new_z  # Update rabbit's position