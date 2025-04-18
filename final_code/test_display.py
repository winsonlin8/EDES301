# -*- coding: utf-8 -*-

from screen import SPI_Display
import time

# Initialize display
display = SPI_Display()

# Brief pause
time.sleep(0.5)

# Cycle through red, green, blue
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
for color in colors:
    print(f"Filling screen with color: {color}")
    display.fill(color)
    time.sleep(1)

# Display some text
display.text("Hello world", fontsize=24, rotation=270)
