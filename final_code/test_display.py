from screen import SPI_Display
import time

display = SPI_Display()

# Cycle through red, green, blue
for i in range(3):
    display.fill((255 * (i == 0), 255 * (i == 1), 255 * (i == 2)))
    time.sleep(1)