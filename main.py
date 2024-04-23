import pygame

# Constants for window resolution and colors
RESOLUTION = WIDTH, HEIGHT = 800, 600
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)
VERTEX_COLOR = (250, 250, 250)

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

