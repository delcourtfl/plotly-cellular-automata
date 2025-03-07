from pca.cell import Cell
import numpy as np
import trimesh
import plotly.graph_objects as go
from pca.enum import Entity
from pathlib import Path
import os

WORK_DIR = Path.cwd()

class ModelLoader():
    file_paths = {
        Entity.RABBIT: "./res/animals/Rabbit/Rabbit_01.obj"
    }

    def __init__(self):
        self.models = {}
        self.load_all_models()

    def load_all_models(self):
        for entity, path in self.file_paths.items():
            self.load_obj(entity, path)

        box_model = ModelLoader.create_box_model()
        for ent in Entity:
            if ent not in self.models:
                self.models[ent] = box_model 

    def load_obj(self, entity, path):
        mesh = trimesh.load_mesh(path)

        # Extract vertex and face data
        vertices = np.array(mesh.vertices)
        faces = np.array(mesh.faces)

        # Apply UV mapping to extract colors
        uv_coords = mesh.visual.uv
        texture_img = mesh.visual.material
        vertex_colors = texture_img.to_color(uv_coords)

        self.models[entity] = {
            'mesh': mesh,
            'vertices': vertices,
            'faces': faces,
            'vertex_colors': vertex_colors
        }

    def get_model(self, entity):

        model = self.models.get(entity, None)
        if not model:
            raise ValueError(f"Model {entity} not found by the ModelLoader")

        return model

    @staticmethod
    def create_box_model():

        # Define vertices and faces
        vertices = {
            "x": [0, 1, 0, 1, 0, 1, 0, 1],
            "y": [0, 0, 1, 1, 0, 0, 1, 1],
            "z": [0, 0, 0, 0, 1, 1, 1, 1],
        }

        faces = {
            "a": [0, 3, 4, 7, 0, 6, 1, 7, 0, 5, 2, 7],
            "b": [1, 2, 5, 6, 2, 4, 3, 5, 4, 1, 6, 3],
            "c": [3, 0, 7, 4, 6, 0, 7, 1, 5, 0, 7, 2],
        }

        # Convert vertices to a (8,3) NumPy array
        vertices_np = np.column_stack((vertices["x"], vertices["y"], vertices["z"]))

        # Convert faces to a (12,3) NumPy array
        faces_np = np.column_stack((faces["a"], faces["b"], faces["c"]))

        return {
            'mesh': None,
            'vertices': vertices_np,
            'faces': faces_np,
            'vertex_colors': None
        }