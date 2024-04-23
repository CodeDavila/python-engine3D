import pygame
import math
import numpy

# Constants for window resolution and colors
RESOLUTION = WIDTH, HEIGHT = 800, 600
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)
VERTEX_COLOR = (250, 250, 250)

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
    translation_matrix = numpy.array([
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
    rotation_matrix = numpy.array([
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
    rotation_matrix = numpy.array([
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
    rotation_matrix = numpy.array([
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
    scaling_matrix = numpy.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])
    return scaling_matrix

# 3D - Cube
vertexes = numpy.array([
    (0, 0, 0, 1),
    (0, 1, 0, 1),
    (1, 1, 0, 1),
    (1, 0, 0, 1),
    (0, 0, 1, 1),
    (0, 1, 1, 1),
    (1, 1, 1, 1),
    (1, 0, 1, 1)
    ])

faces = numpy.array([
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (0, 4, 5, 1),
    (2, 3, 7, 6),
    (1, 2, 6, 5),
    (0, 3, 7, 4)
    ])

# Class to create 3D objects

class Object3D:
    def __init__(self, vertexes, faces):
        """
        Initialize a 3D object with vertexes and faces.

        Args:
            vertexes (numpy.ndarray): Array of vertexes in homogeneous coordinates.
            faces (numpy.ndarray): Array of faces, each represented by the indices of vertexes.
        """
        self.vertexes = vertexes
        self.faces = faces

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

