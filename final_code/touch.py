import time
import board
import busio
import digitalio
from adafruit_stmpe610 import Adafruit_STMPE610_SPI
from adafruit_blinka.microcontroller.am335x.pin import SPI1_SCLK, SPI1_D1, SPI1_D0

class STMPE610Touch:
    def __init__(self,
                 cs_pin=board.P2_31,
                 baudrate=1000000,
                 calibration=((0, 4095), (0, 4095)),
                 size=(320, 240),
                 rotation=0):

        # Use SPI1
        self.spi = busio.SPI(clock=SPI1_SCLK, MOSI=SPI1_D1, MISO=SPI1_D0)

        # Setup CS pin
        self.cs = digitalio.DigitalInOut(cs_pin)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.cs.value = True

        # Initialize STMPE610 driver
        self.touch = Adafruit_STMPE610_SPI(self.spi,
                                           self.cs,
                                           baudrate=baudrate,
                                           calibration=calibration,
                                           size=size,
                                           disp_rotation=rotation)

    def is_touched(self):
        return self.touch.touched

    def get_touch(self):
        point = self.touch.touch_point
        if point is not None:
            x, y, pressure = point
            return {'x': x, 'y': y, 'pressure': pressure}
        return None

    def check_region(self, x_range, y_range):
        touch = self.get_touch()
        if touch:
            x, y = touch['x'], touch['y']
            return x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]
        return False

    def check_top_right(self):
        return self.check_region((0, 800), (0, 800))

    def check_top_left(self):
        return self.check_region((0, 800), (3300, 4095))

    def check_bottom_right(self):
        return self.check_region((3300, 4095), (0, 800))

    def check_bottom_left(self):
        return self.check_region((3300, 4095), (3300, 4095))

    def check_middle(self):
        return self.check_region((1800, 2200), (1800, 2200))

    def check_bottom_middle(self):
        return self.check_region((2000, 4095), (1800, 2200))

    def check_top_middle(self):
        return self.check_region((0, 2000), (1800, 2200))

    def check_quad_1(self):
        return self.check_region((0, 2000), (0, 2000))

    def check_quad_2(self):
        return self.check_region((0, 2000), (2000, 4095))

    def check_quad_3(self):
        return self.check_region((2000, 4095), (2000, 4095))

    def check_quad_4(self):
        return self.check_region((2000, 4095), (0, 2000))

if __name__ == '__main__':
    print("Initializing STMPE610 touchscreen...")
    ts = STMPE610Touch()
    print("Touchscreen ready. Tap to see output.")
    while True:
        touch = ts.get_touch()
        if touch:
            print(f"Touch at x={touch['x']}, y={touch['y']}, pressure={touch['pressure']}")
        time.sleep(0.01)
