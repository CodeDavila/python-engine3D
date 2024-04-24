import pygame
import math
import numpy as np
from numba import njit


pygame.init()

# Numba wraper 
@njit(fastmath = True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))

# Constants for window resolution and colors
RESOLUTION = WIDTH, HEIGHT = 1200, 700
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)
LINE_COLOR = (255, 0, 255)
VERTEX_COLOR = (255, 255, 255)
FONT_COLOR = (255, 255, 0)

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

# Read a obj File Functions
def readOBJ(file):
    vertex, faces = [], []
    with open(file) as file_handle:
        for line in file_handle:
            if line.startswith('v '):
                vertex.append([float(i) for i in line.split()[1:]] + [1])
            elif line.startswith('f'):
                faces_ = line.split()[1:]
                faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])

    vertexes_r = np.array([np.array(v) for v in vertex])
    faces_r = np.array([np.array(f) for f in faces])

    return vertexes_r, faces_r

# Duck model from file 
# duck_vertexes, duck_faces = readOBJ('duck.obj')
# Plane mpdel from file 
plane_vertexes, plane_faces = readOBJ('plane_japan_wwII.obj')

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
        [0, cos_a, sin_a, 0],
        [0, -sin_a, cos_a, 0],
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
        [cos_a, 0, -sin_a, 0],
        [0, 1, 0, 0],
        [sin_a, 0, cos_a, 0],
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
        [cos_a, sin_a, 0, 0],
        [-sin_a, cos_a, 0, 0],
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


# Class to create 3D objects

class Object3D:
    def __init__(self, render, vertexes, faces, draw_vertexes = False):
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

        self.font = pygame.font.SysFont('arial', 30, bold=True)
        self.color_faces = [(pygame.Color(LINE_COLOR), face) for face in self.faces]
        self.draw_vertexes = draw_vertexes
        self.label = ''

    def draw(self, window):
        """
        Draw the 3D object on the screen.
        """
        vertexes = self._screen_projection()

        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            polygon = vertexes[face]
            if not any_func(polygon, HALF_WIDTH, HALF_HEIGHT):
                pygame.draw.polygon(window, color, polygon, 1)
                if self.label:
                    text = self.font.render(self.label[index], True, pygame.Color(FONT_COLOR))
                    window.blit(text, polygon[-1])

        if self.draw_vertexes:
            for vertex in vertexes:
                if not any_func(vertex, HALF_WIDTH, HALF_HEIGHT):
                    pygame.draw.circle(window, pygame.Color(VERTEX_COLOR), vertex, 2)

    def _screen_projection(self):
        """
        Project the vertexes of the object onto the screen.

        Returns:
            numpy.ndarray: Screen-projected vertexes.
        """
        vertexes = self.vertexes @ self.render.camera._camera()
        vertexes = vertexes @ self.render.Clip_Projection.projection_matrix
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0
        vertexes = vertexes @ self.render.Clip_Projection.to_screen_matrix
        vertexes = vertexes[:, :2]

        return vertexes

    def translate(self, position):
        """
        Translate the object by the given translation vector.

        Args:
            position (tuple): Translation vector (tx, ty, tz).
        """
        self.vertexes = self.vertexes @ translate(position=position)

    def rotate_x(self, angle):
        """
        Rotate the object about the x-axis by the given angle.

        Args:
            angle (float): Rotation angle in degrees.
        """
        self.vertexes = self.vertexes @ rotate_x(angle=angle)

    def rotate_y(self, angle):
        """
        Rotate the object about the y-axis by the given angle.

        Args:
            angle (float): Rotation angle in degrees.
        """
        self.vertexes = self.vertexes @ rotate_y(angle=angle)

    def rotate_z(self, angle):
        """
        Rotate the object about the z-axis by the given angle.

        Args:
            angle (float): Rotation angle in degrees.
        """
        self.vertexes = self.vertexes @ rotate_z(angle=angle)

    def scale(self, scaling_factors):
        """
        Scale the object by the given scaling factors.

        Args:
            scaling_factors (tuple): Scaling factors (sx, sy, sz).
        """
        self.vertexes = self.vertexes @ scale(scaling_factors=scaling_factors)

class Axes(Object3D):
    def __init__(self, render, vertexes = np.array([
            (0, 0, 0, 1),
            (1, 0, 0, 1),
            (0, 1, 0, 1),
            (0, 0, 1, 1)
            ]), faces = np.array([
            (0, 1),
            (0, 2),
            (0, 3)
            ]), draw_vertexes=False):
        super().__init__(render, vertexes, faces, draw_vertexes)
        self.vertexes = vertexes
        self.faces = faces
        self.colors = [pygame.Color('red'), pygame.Color('green'), pygame.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertexes = False
        self.label = 'XYZ'

# Class to create a camera
class Camera:
    def __init__(self, position):
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
        self.v_fov = self.h_fov * (HEIGHT / WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = 0.02
        self.rotation_speed = 0.5

    def control(self) -> None:
        """
        Method to control camera movement and rotation based on user input.
        """
        key = pygame.key.get_pressed()

        # Handling user input for camera controls
        if key[pygame.K_a]:
            # Move left (along the camera's right vector)
            self.position -= self.right * self.moving_speed

        elif key[pygame.K_d]:
            # Move right (along the camera's right vector)
            self.position += self.right * self.moving_speed

        elif key[pygame.K_w]:
            # Move forward (along the camera's forward vector)
            self.position += self.forward * self.moving_speed

        elif key[pygame.K_s]:
            # Move backward (along the camera's forward vector)
            self.position -= self.forward * self.moving_speed

        elif key[pygame.K_q]:
            # Move up (along the camera's up vector)
            self.position += self.up * self.moving_speed

        elif key[pygame.K_e]:
            # Move down (along the camera's up vector)
            self.position -= self.up * self.moving_speed

        elif key[pygame.K_LEFT]:
            # Rotate the camera (along the y axis)
            self._camera_yaw(-self.rotation_speed)

        elif key[pygame.K_RIGHT]:
            # Rotate the camera (along the y axis)
            self._camera_yaw(self.rotation_speed)

        elif key[pygame.K_UP]:
            # Rotate the camera (along the x axis)
            self._camera_pitch(-self.rotation_speed)

        elif key[pygame.K_DOWN]:
            # Rotate the camera (along the x axis)
            self._camera_pitch(self.rotation_speed)

        elif key[pygame.K_h]:
            # Print controls guide when 'h' key is pressed
            print("""
            Camera moving controls:

                a - to go LEFT
                d - to go RIGHT
                w - to go FORWARD
                s - to go BACKWARD
                q - to go UP
                e - to go DOWN

            Camera rotation controls:

                ← - to LEFT YAW
                → - to RIGHT YAW
                ↑ - to PITCH
                ↓ - to PITCH
            """)

    def _camera_yaw(self, angle):
        rotate = rotate_y(angle=angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def _camera_pitch(self, angle):
        rotate = rotate_x(angle=angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

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
            [0, 0, m22, 1],
            [0, 0, m32, 0]
        ])
        HW, HH = HALF_WIDTH, HALF_HEIGHT
        self.to_screen_matrix = np.array([
            [HW, 0, 0, 0],
            [0, -HH, 0, 0],
            [0, 0, 1, 0],
            [HW, HH, 0, 1]
        ])

# Class to render an object
class Render:
    def __init__(self, camera_position):
        """
        Initialize the Render object.
        """
        self.camera = Camera(position=camera_position)
        self.Clip_Projection = Clip_Projection(self)

    def create_object(self, vertexes, faces, draw_vertexes = False):
        """
        Create a 3D object.

        Args:
            vertexes (numpy.ndarray): Array of vertexes in homogeneous coordinates.
            faces (numpy.ndarray): Array of faces, each represented by the indices of vertexes.

        Returns:
            Object3D: A 3D object.
        """
        return Object3D(self, vertexes, faces, draw_vertexes)
    
    def create_axes(self):
        return Axes(self)

# Create a Render object
render = Render(camera_position=[0.5, 1.2, -6])

# Create a 3D object (a cube)
# cube = render.create_object(cube_vertexes, cube_faces, draw_vertexes=True)
# cube.translate([0.2, 0.4, 0.2])

# Create cube axes
# axes = render.create_axes()
# axes.translate([0.7, 0.9, 0.7])

# Create a 3D object (a duck)
# duck = render.create_object(duck_vertexes, duck_faces, draw_vertexes=False)
# duck.scale([0.04, 0.04, 0.04])
# duck.rotate_x(-90)
# duck.rotate_y(-150)
# duck.translate([1, 0.0001, 1])

# Create a 3D object (a plane)
plane = render.create_object(plane_vertexes, plane_faces, draw_vertexes=False)
plane.scale([2.5, 2.5, 2.5])
plane.rotate_x(-90)
plane.rotate_y(150)
plane.translate([1, 1, 1])
# Create world axes
world_axes = render.create_axes()
world_axes.scale([2.5, 2.5, 2.5])
world_axes.translate([0.0001, 0.0001, 0.0001])

# Initialize Pygame

# Create the game window
window = pygame.display.set_mode(RESOLUTION)

# Create a Pygame clock object to control the frame rate
clock = pygame.time.Clock()

# Main game loop
while True:
    # Fill the window with the background color
    window.fill(pygame.Color(BACKGROUND_COLOR))

    # Draw the world_axes
    world_axes.draw(window=window)

    # Draw the cube
    # cube.draw(window=window)
    # Move the cube
    # cube.rotate_y(math.degrees(pygame.time.get_ticks() % 0.005))

    # Draw the cube axes
    # axes.draw(window=window)
    # Move the axes along the cube
    # axes.rotate_y(math.degrees(pygame.time.get_ticks() % 0.005))

    # Draw the duck
    # duck.draw(window=window)
    # Move the duck
    # duck.rotate_y(math.degrees(pygame.time.get_ticks() % 0.005))

    # Draw the plane
    plane.draw(window=window)
    # Move the plane
    plane.rotate_y(math.degrees(pygame.time.get_ticks() % 0.005))

    # Activate the control of the camera
    render.camera.control()

    # Handle events
    for event in pygame.event.get():
        # Check if the user clicked the close button
        if event.type == pygame.QUIT:
            # If so, exit the program
            exit()

    # Set the window title to display the current FPS
    pygame.display.set_caption(str(math.ceil(clock.get_fps())))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to FPS
    clock.tick(FPS)

