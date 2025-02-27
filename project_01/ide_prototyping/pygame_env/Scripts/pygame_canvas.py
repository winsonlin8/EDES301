import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
width, height = 320, 240
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pygame Drawing App')

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
current_color = black

# Fill background
screen.fill(white)
pygame.display.flip()

# Main loop
running = True
drawing = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            pygame.draw.circle(screen, current_color, event.pos, 3)
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.MOUSEMOTION and drawing:
            pygame.draw.circle(screen, current_color, event.pos, 3)
        
        # Event to change the color when pressing 'r'
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                current_color = red if current_color == black else black

    pygame.display.flip()

pygame.quit()
sys.exit()
