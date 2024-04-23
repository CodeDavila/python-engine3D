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
    tx, ty, tz = position
    translation_matrix = numpy.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1]
    ])
    # Apply translation_matrix to points

def rotate_x(angle):
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    rotation_matrix = numpy.array([
        [1, 0, 0, 0],
        [0, cos_a, -sin_a, 0],
        [0, sin_a, cos_a, 0],
        [0, 0, 0, 1]
    ])
    # Apply rotation_matrix to points about x-axis

def rotate_y(angle):
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    rotation_matrix = numpy.array([
        [cos_a, 0, sin_a, 0],
        [0, 1, 0, 0],
        [-sin_a, 0, cos_a, 0],
        [0, 0, 0, 1]
    ])
    # Apply rotation_matrix to points about y-axis

def rotate_z(angle):
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    rotation_matrix = numpy.array([
        [cos_a, -sin_a, 0, 0],
        [sin_a, cos_a, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    # Apply rotation_matrix to points about z-axis

def scale(scaling_factors):
    sx, sy, sz = scaling_factors
    scaling_matrix = numpy.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])
    # Apply scaling_matrix to points

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

