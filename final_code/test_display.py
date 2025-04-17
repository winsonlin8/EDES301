from screen import SPI_Display
import time

# Initialize the display
display = SPI_Display()

# Brief pause to make sure init finishes
time.sleep(0.5)

# Cycle through red, green, blue to test the screen
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
for color in colors:
    print(f"Filling screen with color: {color}")
    display.fill(color)
    time.sleep(1)

# Optional: display some text
display.text("Hello, PocketBeagle!", fontsize=24, rotation=270)
