import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
width, height = 320, 240
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pygame Canvas')

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
yellow = (255, 204, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (75, 0, 130)
pink = (255, 192, 203)
colors = [black, red, orange, yellow, green, blue, indigo, pink]  # List of colors
color_index = 0  # Initial index in the color list
current_color = colors[color_index]

# Button specifications
button_color = current_color  # Start with the first color
color_button_rect = pygame.Rect(10, 10, 80, 30)  # Position and size of the color button
clear_button_rect = pygame.Rect(100, 10, 80, 30)  # Position and size of the clear button

# Helper function to draw buttons
def draw_button(text, rect, color):
    pygame.draw.rect(screen, color, rect)
    font = pygame.font.Font(None, 24)
    text_surf = font.render(text, True, white)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

# Function to refresh the screen
def refresh_screen():
    draw_button("Color", color_button_rect, button_color)  # Draw the color button
    draw_button("Clear", clear_button_rect, black)  # Draw the clear button
    pygame.display.flip()
    
def clear_screen():
    screen.fill(white)  # Clear the canvas
    draw_button("Color", color_button_rect, button_color)  # Draw the color button
    draw_button("Clear", clear_button_rect, black)  # Draw the clear button
    pygame.display.flip()
    
# Draw initial UI
clear_screen()
refresh_screen()

# Main loop
running = True
drawing = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if color_button_rect.collidepoint(event.pos):
                # Cycle through the colors
                color_index = (color_index + 1) % len(colors)
                current_color = colors[color_index]
                button_color = current_color
                refresh_screen()
            elif clear_button_rect.collidepoint(event.pos):
                # Clear the screen when clear button is pressed
                clear_screen()
            else:
                drawing = True
                pygame.draw.circle(screen, current_color, event.pos, 3)
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.MOUSEMOTION and drawing:
            pygame.draw.circle(screen, current_color, event.pos, 3)

    pygame.display.flip()

pygame.quit()
sys.exit()
