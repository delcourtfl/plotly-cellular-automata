class Cell:
    def __init__(self, type=0, state=0, x=0, y=0, z=0, model={}):
        """
        Initializes a cell with a specific state and 3D position.
        
        :param state: The initial state of the cell (e.g., 0 or 1).
        :param x, y, z: The position of the cell in 3D space (optional for rendering).
        """
        self.type = type
        self.state = state
        self.x = x
        self.y = y
        self.z = z

        self.model = model

        self.mesh = model.get('mesh', None)
        self.vertices = model.get('vertices', None)
        self.faces = model.get('faces', None)
        self.vertex_colors = model.get('vertex_colors', None)

    def update(self, new_state):
        """
        Update the cell's state.
        
        :param new_state: The new state the cell will transition to.
        """
        self.state = new_state

    def render(self):
        """
        Defines how the cell should be rendered in 3D.
        You can customize this to show different colors or representations based on the state.
        """
        raise ValueError("Render is not implemented for this cell")
    
    def step(self, new_grid, old_grid):
        pass

    @staticmethod
    def normalize_vertices(vertices):
        # Find min and max values for each axis
        min_vals = vertices.min(axis=0)
        max_vals = vertices.max(axis=0)

        # Compute the center and scale
        center = (min_vals + max_vals) / 2  # Center of the bounding box
        scale = (max_vals - min_vals).max()  # Largest dimension

        # Normalize to [-0.5, 0.5] range, then shift to [0,1] if needed
        norm_vertices = (vertices - center) / scale  # Scale to fit within [-0.5, 0.5]
        norm_vertices += 0.5

        return norm_vertices
    
    @staticmethod
    def normalize_vertices_to_floor(vertices):
        # Find min and max values for each axis
        min_vals = vertices.min(axis=0)
        max_vals = vertices.max(axis=0)

        # Compute the center and scale
        center = (min_vals + max_vals) / 2  # Center of the bounding box
        scale = (max_vals - min_vals).max()  # Largest dimension

        # Normalize to [-0.5, 0.5] range
        norm_vertices = (vertices - center) / scale
        norm_vertices += 0.5

        # Shift everything so the lowest Z point is at 0
        min_z = norm_vertices[:, 2].min()  # Find the new min Z value
        norm_vertices[:, 2] -= min_z * 0.99 # Lift everything up

        return norm_vertices
