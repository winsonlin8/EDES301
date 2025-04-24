import time
from PIL import Image, ImageDraw, ImageFilter
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

def point_in_box(x, y, box, padding=20):
    return (box[0] - padding <= x <= box[2] + padding and
            box[1] - padding <= y <= box[3] + padding)

def guess_shape(canvas):
    gray = canvas.convert("L")
    pixels = gray.load()
    width, height = gray.size
    threshold = 100

    points = [(x, y) for y in range(height) for x in range(width) if pixels[x, y] < threshold]

    if not points:
        return "None", 0.0, 0.0

    xs, ys = zip(*points)
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    center_x = (min_x + max_x) // 2
    center_y = (min_y + max_y) // 2

    # Count points in 4 quadrants around center
    q1 = q2 = q3 = q4 = 0
    for x, y in points:
        if x < center_x and y < center_y:
            q1 += 1
        elif x >= center_x and y < center_y:
            q2 += 1
        elif x < center_x and y >= center_y:
            q3 += 1
        else:
            q4 += 1

    total = q1 + q2 + q3 + q4
    if total == 0:
        return "None", 0.0, 0.0

    # Symmetry scores
    horizontal_symmetry = abs((q1 + q2) - (q3 + q4)) / total
    vertical_symmetry = abs((q1 + q3) - (q2 + q4)) / total

    print(f"Quadrants: Q1:{q1} Q2:{q2} Q3:{q3} Q4:{q4}")
    print(f"H-Symmetry: {horizontal_symmetry:.2f}, V-Symmetry: {vertical_symmetry:.2f}")

    # Heuristic: low symmetry difference → circle
    if horizontal_symmetry < 0.3 and vertical_symmetry < 0.3:
        return "Circle", horizontal_symmetry, vertical_symmetry
    else:
        return "Triangle", horizontal_symmetry, vertical_symmetry


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
                    print("Guess button pressed.")
                    prediction, circ, sym = guess_shape(canvas)
                    print(f"Prediction: {prediction}")
                    draw.rectangle((120, 5, DISPLAY_WIDTH - 120, 30), fill=BACKGROUND_COLOR)
                    prediction, h_sym, v_sym = guess_shape(canvas)
                    draw.text((130, 10), f"{prediction}, fill=(0, 0, 0))
                    display.display.image(canvas)
                else:
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if 0 <= x_disp + dx < DISPLAY_WIDTH and 0 <= y_disp + dy < DISPLAY_HEIGHT:
                                canvas.putpixel((x_disp + dx, y_disp + dy), DRAW_COLOR)
                    now = time.time()
                    if now - last_update > 0.05:
                        display.display.image(canvas)
                        last_update = now

            time.sleep(0.005)

    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Turning off display.")
        display.fill((0, 0, 0))

if __name__ == "__main__":
    main()
