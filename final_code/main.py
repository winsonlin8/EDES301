import time
from PIL import Image, ImageDraw
from screen import SPI_Display
from touch import STMPE610Touch

# Constants
DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240
ELLIPSE_RADIUS = 5
BACKGROUND_COLOR = (255, 255, 255)
DRAW_COLOR = (255, 0, 0)

# Raw calibration values
RAW_X_MIN, RAW_X_MAX = 56, 289
RAW_Y_MIN, RAW_Y_MAX = 26, 199

# Button config
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 5
CLEAR_BUTTON_BOX = (BUTTON_MARGIN, DISPLAY_HEIGHT - BUTTON_HEIGHT - BUTTON_MARGIN,
                    100, DISPLAY_HEIGHT - BUTTON_MARGIN)
GUESS_BUTTON_BOX = (DISPLAY_WIDTH - 100, DISPLAY_HEIGHT - BUTTON_HEIGHT - BUTTON_MARGIN,
                    DISPLAY_WIDTH - BUTTON_MARGIN, DISPLAY_HEIGHT - BUTTON_MARGIN)


def map_value(value, in_min, in_max, out_min, out_max):
    value = max(min(value, in_max), in_min)
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def draw_buttons(draw):
    draw.rectangle(CLEAR_BUTTON_BOX, fill=(200, 200, 200))
    draw.rectangle(GUESS_BUTTON_BOX, fill=(200, 200, 200))
    draw.text((CLEAR_BUTTON_BOX[0] + 10, CLEAR_BUTTON_BOX[1] + 10), "Clear", fill=(0, 0, 0))
    draw.text((GUESS_BUTTON_BOX[0] + 10, GUESS_BUTTON_BOX[1] + 10), "Guess", fill=(0, 0, 0))

def point_in_box(x, y, box):
    return box[0] <= x <= box[2] and box[1] <= y <= box[3]

def main():
    print("Initializing display...")
    display = SPI_Display(rotation=270)

    print("Initializing touchscreen...")
    touch = STMPE610Touch()

    canvas = Image.new("RGB", (DISPLAY_WIDTH, DISPLAY_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(canvas)

    def clear_canvas():
        draw.rectangle((0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT), fill=BACKGROUND_COLOR)
        draw_buttons(draw)
        display.display.image(canvas)

    print("Running main loop... Tap to draw.")
    clear_canvas()
    
    last_update = time.time()
    
    try:
        while True:
            point = touch.get_touch()
            if point:
                x_raw = point["x"]
                y_raw = point["y"]
                pressure = point["pressure"]

                x_disp = DISPLAY_WIDTH - map_value(x_raw, RAW_X_MIN, RAW_X_MAX, 0, DISPLAY_WIDTH - 1)
                y_disp = map_value(y_raw, RAW_Y_MIN, RAW_Y_MAX, 0, DISPLAY_HEIGHT - 1)

                print(f"Touch raw=({x_raw},{y_raw}) → mapped=({x_disp},{y_disp}), pressure={pressure}")

                if point_in_box(x_disp, y_disp, CLEAR_BUTTON_BOX):
                    print("Clear button pressed.")
                    clear_canvas()
                elif point_in_box(x_disp, y_disp, GUESS_BUTTON_BOX):
                    print("Guess button pressed. (TODO)")
                else:
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if 0 <= x_disp + dx < DISPLAY_WIDTH and 0 <= y_disp + dy < DISPLAY_HEIGHT:
                                canvas.putpixel((x_disp + dx, y_disp + dy), DRAW_COLOR)
                    now = time.time()
                    if now - last_update > 0.05:  # try 0.05 or even 0.08
                        display.display.image(canvas)
                        last_update = now

            time.sleep(0.005)

    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Turning off display.")
        display.fill((0, 0, 0))

if __name__ == "__main__":
    main()