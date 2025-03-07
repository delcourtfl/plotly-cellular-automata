from pca.cell import Cell
import numpy as np
from pca.enum import Entity

class Terrain(Cell):

    def __init__(self, state=0, x=0, y=0, z=0, model={}):
        super().__init__(Entity.TERRAIN, state, x, y, z, model)

        self.colors = Terrain.get_colors()

    def render(self):
        return self.vertices, self.faces, self.colors
    
    @staticmethod
    def get_colors():
        # Assign alternating intensity values per cube face (ensuring each face has the same color)
        num_faces = 12 // 2  # 2 triangles per face
        face_colors = np.tile([0, 7, 7, 7, 8, 8], num_faces // 6 + 1)[:num_faces]
        # face_colors = np.tile([0, 1, 2, 3, 4, 5], num_faces // 6 + 1)[:num_faces]

        # Repeat each color twice so both triangles of a face have the same intensity
        intensity_values = np.repeat(face_colors, 2)

        # intensity_values = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        return intensity_values
    