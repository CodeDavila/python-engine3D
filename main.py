import pygame
import math
import numpy as np

# Constants for window resolution and colors
RESOLUTION = WIDTH, HEIGHT = 800, 600
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)
LINE_COLOR = (255, 0, 255)
VERTEX_COLOR = (255, 255, 255)

# Matrix operation Functions

def translate(position):
    """
    Translate a point or a set of points by the given translation vector.

    Args:
        position (tuple): Translation vector (tx, ty, tz).
    
    Returns:
        numpy.ndarray: Translation matrix.
    """
    tx, ty, tz = position
    translation_matrix = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1]
    ])
    return translation_matrix

def rotate_x(angle):
    """
    Rotate a point or a set of points about the x-axis by the given angle.

    Args:
        angle (float): Rotation angle in degrees.
    
    Returns:
        numpy.ndarray: Rotation matrix.
    """
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    rotation_matrix = np.array([
        [1, 0, 0, 0],
        [0, cos_a, -sin_a, 0],
        [0, sin_a, cos_a, 0],
        [0, 0, 0, 1]
    ])
    return rotation_matrix

def rotate_y(angle):
    """
    Rotate a point or a set of points about the y-axis by the given angle.

    Args:
        angle (float): Rotation angle in degrees.
    
    Returns:
        numpy.ndarray: Rotation matrix.
    """
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    rotation_matrix = np.array([
        [cos_a, 0, sin_a, 0],
        [0, 1, 0, 0],
        [-sin_a, 0, cos_a, 0],
        [0, 0, 0, 1]
    ])
    return rotation_matrix

def rotate_z(angle):
    """
    Rotate a point or a set of points about the z-axis by the given angle.

    Args:
        angle (float): Rotation angle in degrees.
    
    Returns:
        numpy.ndarray: Rotation matrix.
    """
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    rotation_matrix = np.array([
        [cos_a, -sin_a, 0, 0],
        [sin_a, cos_a, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    return rotation_matrix

def scale(scaling_factors):
    """
    Scale a point or a set of points by the given scaling factors.

    Args:
        scaling_factors (tuple): Scaling factors (sx, sy, sz).
    
    Returns:
        numpy.ndarray: Scaling matrix.
    """
    sx, sy, sz = scaling_factors
    scaling_matrix = np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])
    return scaling_matrix

# 3D - Cube
cube_vertexes = np.array([
    (0, 0, 0, 1),
    (0, 1, 0, 1),
    (1, 1, 0, 1),
    (1, 0, 0, 1),
    (0, 0, 1, 1),
    (0, 1, 1, 1),
    (1, 1, 1, 1),
    (1, 0, 1, 1)
])

cube_faces = np.array([
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (0, 4, 5, 1),
    (2, 3, 7, 6),
    (1, 2, 6, 5),
    (0, 3, 7, 4)
])

# Class to create 3D objects

class Object3D:
    def __init__(self, render, vertexes, faces):
        """
        Initialize a 3D object with vertexes and faces.

        Args:
            render: Render object.
            vertexes (numpy.ndarray): Array of vertexes in homogeneous coordinates.
            faces (numpy.ndarray): Array of faces, each represented by the indices of vertexes.
        """
        self.render = render
        self.vertexes = vertexes
        self.faces = faces

    def draw(self):
        """
        Draw the 3D object on the screen.
        """
        vertexes = self._screen_projection()
        for face in self.faces:
            polygon = vertexes[face]
            if not np.any(polygon == [HALF_WIDTH, HALF_HEIGHT]):
                pygame.draw.polygon(window, pygame.Color(LINE_COLOR), polygon, 3)

        for vertex in vertexes:
            if not np.any(vertex == [HALF_WIDTH, HALF_HEIGHT]):
                pygame.draw.circle(window, pygame.Color(VERTEX_COLOR), vertex, 6)

    def _screen_projection(self):
        """
        Project the vertexes of the object onto the screen.

        Returns:
            numpy.ndarray: Screen-projected vertexes.
        """
        vertexes = self.vertexes @ self.render.camera._camera()
        vertexes = vertexes @ self.render.Clip_Projection.projection_matrix
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        vertexes[(vertexes > 1) | (vertexes < -1)] = 0
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2]

        return vertexes

    def _translate(self, position):
        """
        Translate the object by the given translation vector.

        Args:
            position (tuple): Translation vector (tx, ty, tz).
        """
        self.vertexes = self.vertexes @ translate(position=position)

    def _rotate_x(self, angle):
        """
        Rotate the object about the x-axis by the given angle.

        Args:
            angle (float): Rotation angle in degrees.
        """
        self.vertexes = self.vertexes @ rotate_x(angle=angle)

    def _rotate_y(self, angle):
        """
        Rotate the object about the y-axis by the given angle.

        Args:
            angle (float): Rotation angle in degrees.
        """
        self.vertexes = self.vertexes @ rotate_y(angle=angle)

    def _rotate_z(self, angle):
        """
        Rotate the object about the z-axis by the given angle.

        Args:
            angle (float): Rotation angle in degrees.
        """
        self.vertexes = self.vertexes @ rotate_z(angle=angle)

    def _scale(self, scaling_factors):
        """
        Scale the object by the given scaling factors.

        Args:
            scaling_factors (tuple): Scaling factors (sx, sy, sz).
        """
        self.vertexes = self.vertexes @ scale(scaling_factors=scaling_factors)

# Class to create a camera
class Camera:
    def __init__(self, render, position):
        """
        Initialize a camera with position and orientation.

        Args:
            render: Render object.
            position (tuple): Position of the camera (x, y, z).
        """
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100

    def _translate(self):
        """
        Create a translation matrix for the camera position.
        
        Returns:
            numpy.ndarray: Translation matrix.
        """
        x, y, z, _ = self.position
        return translate((-x, -y, -z))

    def _rotate(self):
        """
        Create a rotation matrix for the camera orientation.

        Returns:
            numpy.ndarray: Rotation matrix.
        """
        rx, ry, rz, _ = self.right
        fx, fy, fz, _ = self.forward
        ux, uy, uz, _ = self.up
        rotation_matrix = np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])
        return rotation_matrix

    def _camera(self):
        """
        Get the combined transformation matrix for the camera.

        Returns:
            numpy.ndarray: Combined transformation matrix.
        """
        return self._translate() @ self._rotate()

# Class for the clipping projection of the camera
class Clip_Projection:
    def __init__(self, render):
        """
        Initialize the clipping projection with parameters from the camera.

        Args:
            render: Render object.
        """
        NEAR = render.camera.near_plane
        FAR = render.camera.far_plane
        RIGHT = math.tan(render.camera.h_fov / 2)
        LEFT = -RIGHT
        TOP = math.tan(render.camera.v_fov / 2)
        BOTTOM = -TOP

        m00 = 2 / (RIGHT - LEFT)
        m11 = 2 / (TOP - BOTTOM)
        m22 = (FAR + NEAR) / (FAR - NEAR)
        m32 = -2 * NEAR * FAR / (FAR - NEAR)

        self.projection_matrix = np.array([
            [m00, 0, 0, 0],
            [0, m11, 0, 0],
            [0, 0, m22, m32],
            [0, 0, 1, 0]
        ])
        HW, HH = HALF_WIDTH, HALF_HEIGHT
        self.to_screen_matrix = np.array([
            [HW, 0, 0, 0],
            [0, -HH, 0, 0],
            [0, 0, 1, 0],
            [HW, HH, 0, 1]
        ])

# Initialize Pygame
pygame.init()

# Create the game window
window = pygame.display.set_mode(RESOLUTION)

# Create a Pygame clock object to control the frame rate
clock = pygame.time.Clock()

# Main game loop
while True:
    # Fill the window with the background color
    window.fill(pygame.Color(BACKGROUND_COLOR))

    # Handle events
    for event in pygame.event.get():
        # Check if the user clicked the close button
        if event.type == pygame.QUIT:
            # If so, exit the program
            exit()

    # Set the window title to display the current FPS
    pygame.display.set_caption(str(clock.get_fps()))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to FPS
    clock.tick(FPS)

