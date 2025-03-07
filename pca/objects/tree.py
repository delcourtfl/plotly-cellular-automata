from pca.cell import Cell
import numpy as np
import trimesh
import plotly.graph_objects as go
from pca.enum import Entity

class Tree(Cell):

    def __init__(self, state=0, x=0, y=0, z=0, model={}):
        super().__init__(Entity.TREE, state, x, y, z, model)
