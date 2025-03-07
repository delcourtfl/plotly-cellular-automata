import plotly.graph_objects as go
from pca.cell import Cell
import numpy as np
from pca.enum import Entity

class Renderer:
    def __init__(self, grid, grid_size):
        """
        Initializes the Renderer to display the Cellular Automaton World in 3D.
        
        :param ca_world: The world object that holds the grid and automaton logic.
        """
        self.grid = grid
        self.grid_size = grid_size
        self.frame_cnt = 0
        self.frames = []
        self.render_setup()

    def set_elements(self, grid, grid_size):
        self.grid = grid
        self.grid_size = grid_size

    def render_setup(self):

        self.fig = go.Figure()

        self.terrain_faces = np.empty((0, 3))
        self.terrain_vertices = np.empty((0, 3))
        self.intensity_values = np.empty(0)
        self.n_vertices = 0
        self.n_faces = 0

        self.terrain_mesh = None
        self.entities_meshes = []

        # Update layout to improve visualization
        self.fig.update_layout(
            title="3D Cellular Automaton",
            scene=dict(
                xaxis=dict(showgrid=True, zeroline=False),
                yaxis=dict(showgrid=True, zeroline=False),
                zaxis=dict(showgrid=True, zeroline=False)
            ),
            showlegend=False,
            autosize=True,
            scene_aspectmode='data'
        )

    def add_frame(self):
        # https://stackoverflow.com/questions/69867334/multiple-traces-per-animation-frame-in-plotly

        self.terrain_mesh, self.entities_meshes = self.render_grid()

        self.frames.append(
            go.Frame(
                data=[self.terrain_mesh, *self.entities_meshes],
                name=f'frame_{self.frame_cnt}'
            )
        )
        self.frame_cnt = self.frame_cnt + 1

    
    def render(self):

        if self.frame_cnt > 0:
            self.fig.add_traces(
                self.frames[0].data
            )

        self.fig.frames = self.frames

        def frame_args(duration):
            return {
                "frame": {"duration": duration},
                "mode": "immediate",
                "fromcurrent": True,
                "transition": {"duration": duration, "easing": "linear"},
            }

        sliders = [
            {
                "pad": {"b": 10, "t": 60},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [[f.name], frame_args(0)],
                        "label": str(k),
                        "method": "animate",
                    }
                    for k, f in enumerate(self.fig.frames)
                ],
            }
        ]

        # Add animation controls to the existing layout
        self.fig.update_layout(
            title="Animated 3D Cellular Automaton in Plotly",
            updatemenus = [
                {
                    "buttons": [
                        {
                            "args": [None, frame_args(100)],
                            "label": "&#9654;", # play symbol
                            "method": "animate",
                        },

                        {
                            "args": [[None], frame_args(100)],
                            "label": "&#9724;", # pause symbol
                            "method": "animate",
                        },
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 70},
                    "type": "buttons",
                    "x": 0.1,
                    "y": 0,
                }
            ],
            sliders=sliders,
        )

        self.fig.update_traces(showscale=False)

        return self.fig
    
    def render_grid(self):

        entity_meshes = []

        hover_texts = []
        cube_index = 0

        max_cnt = self.grid_size[0] * self.grid_size[1] * self.grid_size[2]

        cell_count = max_cnt # to initialize the empty arrays
        max_vertices = cell_count * 8
        max_faces = 2 * cell_count * 6

        self.terrain_vertices = np.empty((max_vertices, 3), dtype=np.float32)
        self.terrain_faces = np.empty((max_faces, 3), dtype=np.int32)
        self.intensity_values = np.empty(max_faces, dtype=np.int32)
        self.n_vertices = 0
        self.n_faces = 0

        for x, y, z in np.argwhere(self.grid != None):
            cell = self.grid[x, y, z]

            if Entity.is_terrain(cell.type):
                terrain = cell

                exposed_faces = self.check_neighbors(terrain)

                if not any(exposed_faces):
                    continue  # Skip fully hidden cubes

                # Can be improved further by filtering on the global vertices instead of locally
                new_vertices, new_faces, new_colors = self.filter_visible_faces(terrain, exposed_faces)

                num_new_vertices = len(new_vertices)
                num_new_faces = len(new_faces)

                if num_new_vertices == 0 or num_new_faces == 0:
                    continue

                # Insert vertices directly into preallocated arrays
                self.terrain_vertices[self.n_vertices:self.n_vertices + num_new_vertices] = new_vertices
                self.terrain_faces[self.n_faces:self.n_faces + num_new_faces] = new_faces
                self.intensity_values[self.n_faces:self.n_faces + num_new_faces] = new_colors

                hover_texts += [f"Cube Index: {cube_index}"] * num_new_vertices
                self.n_vertices += num_new_vertices
                self.n_faces += num_new_faces
                cube_index += 1

            else:
                entity = cell

                vertices, faces, vertex_colors = entity.render()
                entity_meshes.append(
                    go.Mesh3d(
                        x=vertices[:, 0], 
                        y=vertices[:, 1], 
                        z=vertices[:, 2],
                        i=faces[:, 0], 
                        j=faces[:, 1],
                        k=faces[:, 2],
                        vertexcolor=vertex_colors,
                    )
                )

        # Trim excess memory
        self.terrain_vertices = self.terrain_vertices[:self.n_vertices]
        self.terrain_faces = self.terrain_faces[:self.n_faces]
        self.intensity_values = self.intensity_values[:self.n_faces]

        # Get unique vertices without reordering
        unique_vertices, unique_indices = np.unique(self.terrain_vertices, axis=0, return_inverse=True)
        updated_faces = unique_indices[self.terrain_faces]

        self.terrain_vertices = unique_vertices
        self.terrain_faces = updated_faces

        terrain_mesh = self.create_terrain_mesh(hover_texts)
        return terrain_mesh, entity_meshes


    def check_neighbors(self, cell: Cell):
        """Check which faces of the cube are exposed."""
        x, y, z = cell.x, cell.y, cell.z  # Cube position
        max_x, max_y, max_z = self.grid_size # Grid bounds

        neighbor_up = self.grid[x][y][z + 1] if z != max_z - 1 else None
        neighbor_left = self.grid[x - 1][y][z] if x != 0 else None
        neighbor_right = self.grid[x + 1][y][z] if x != max_x - 1 else None
        neighbor_down = self.grid[x][y - 1][z] if y != 0 else None
        neighbor_upward = self.grid[x][y + 1][z] if y != max_y - 1 else None

        return [
            False,  # No need for bottom faces
            not neighbor_up or not Entity.is_terrain(neighbor_up.type),
            not neighbor_left or not Entity.is_terrain(neighbor_left.type),
            not neighbor_right or not Entity.is_terrain(neighbor_right.type),
            not neighbor_down or not Entity.is_terrain(neighbor_down.type),
            not neighbor_upward or not Entity.is_terrain(neighbor_upward.type),
        ]
    
    def filter_visible_faces(self, cell: Cell, exposed_faces):

        vertices, faces, colors = cell.render()
        
        visible_faces = []
        visible_colors = []
        # Only add visible faces
        # face_mapping = ["bottom", "top", "left", "right", "front", "back"]
        for i in range(6):
            if exposed_faces[i]:  # Only add if face is exposed
                indices = (i * 2, i * 2 + 1)
                visible_faces.extend([faces[pos] for pos in indices])
                visible_colors.extend([colors[pos] for pos in indices])

        if len(visible_faces) < len(faces):
            filtered_vertices, filtered_faces = self.filter_and_remap_faces(vertices, visible_faces)
            new_vertices = filtered_vertices + np.array([cell.x, cell.y, cell.z])
            new_faces = filtered_faces + self.n_vertices
            new_colors = visible_colors
        else:
            new_vertices = vertices + np.array([cell.x, cell.y, cell.z])
            new_faces = faces + self.n_vertices
            new_colors = colors

        return new_vertices, new_faces, new_colors


    # mesh optimization to avoid drawing too much faces / vertices when they are not visible
    def filter_and_remap_faces(self, vertices, faces_to_keep):

        faces_to_keep = np.array(faces_to_keep)

        # Collect all unique vertex indices used in the selected faces
        used_vertices = np.unique(faces_to_keep.flatten())

        # Create a new list of vertices by only keeping the specified ones
        vertices_to_keep = vertices[used_vertices]

        # Create a mapping from old indices to new indices
        old_to_new_index = {old_idx: new_idx for new_idx, old_idx in enumerate(used_vertices)}

        # Re-index the faces based on the new vertex indices
        new_faces = np.array([[old_to_new_index[idx] for idx in face] for face in faces_to_keep])

        return vertices_to_keep, new_faces 

    def create_terrain_mesh(self, hover_texts=None):

        custom_colorscale = [
            [0.00, "rgb(0, 0, 0)"],        # Black (Dark)

            [0.05, "rgb(100, 0, 0)"],      # Dark Red
            [0.10, "rgb(255, 0, 0)"],      # Red (Light)
            
            [0.15, "rgb(100, 70, 0)"],     # Dark Orange
            [0.20, "rgb(255, 165, 0)"],    # Orange (Light)
            
            [0.25, "rgb(100, 100, 0)"],    # Dark Yellow
            [0.30, "rgb(255, 255, 0)"],    # Yellow (Light)
            
            [0.35, "rgb(0, 100, 0)"],      # Dark Green
            [0.40, "rgb(0, 200, 0)"],      # Green (Light)
            
            [0.45, "rgb(0, 100, 100)"],    # Dark Cyan
            [0.50, "rgb(0, 255, 255)"],    # Cyan (Light)
            
            [0.55, "rgb(0, 0, 100)"],      # Dark Blue
            [0.60, "rgb(0, 0, 255)"],      # Blue (Light)
            
            [0.65, "rgb(50, 0, 50)"],      # Dark Purple
            [0.70, "rgb(128, 0, 128)"],    # Purple (Light)
            
            [0.75, "rgb(100, 0, 100)"],    # Dark Magenta
            [0.80, "rgb(255, 0, 255)"],    # Magenta (Light)
            
            [0.85, "rgb(200, 200, 200)"],  # Dark White (Grayish)
            [0.90, "rgb(255, 255, 255)"],  # White (Bright)
            
            [0.95, "rgb(50, 50, 50)"],     # Dark Gray
            [1.00, "rgb(128, 128, 128)"]   # Gray (Neutral)
        ]

        # print("Generating Mesh3d")
        # color scale : x-->(x-min(x))/(max(x)-min(x))
        # example : i = 4 -> color = (4 - 0) / (20 - 0) = 0.2
        
        # Create the Mesh3d trace
        mesh = go.Mesh3d(
            x=self.terrain_vertices[:, 0],
            y=self.terrain_vertices[:, 1],
            z=self.terrain_vertices[:, 2],
            i=self.terrain_faces[:, 0],
            j=self.terrain_faces[:, 1],
            k=self.terrain_faces[:, 2],
            intensity=np.concatenate((self.intensity_values, [0, 20])), # set min/max range
            intensitymode='cell',
            colorscale=custom_colorscale,  # Custom colors
            hovertext=hover_texts,
            hoverinfo="text+x+y+z",
            # opacity=1.0,
            flatshading=True,
            lighting={
                "vertexnormalsepsilon": 0,
                "facenormalsepsilon": 0
            },
        )

        return mesh
