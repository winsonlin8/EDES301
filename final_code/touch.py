import time
import digitalio
import busio
from adafruit_stmpe610 import Adafruit_STMPE610_SPI

# These are the internal identifiers for the PocketBeagle AM335x
from adafruit_blinka.microcontroller.am335x.pin import SPI1_SCLK, SPI1_D1, SPI1_D0
import board  # still needed for CS pin like board.P2_31

class STMPE610Touch:
    def __init__(self,
                 cs_pin=board.P2_31,  # CS pin still comes from `board`
                 baudrate=1000000,
                 calibration=((0, 4095), (0, 4095)),
                 size=(320, 240),
                 rotation=0):

        # Manually define SPI1 using AM335x pin objects
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
        if self.is_touched():
            point = self.touch.touch_point
            if point is not None:
                x, y, pressure = point
                return {'x': x, 'y': y, 'pressure': pressure}
        return None

if __name__ == '__main__':
    print("Initializing STMPE610 touchscreen...")
    ts = STMPE610Touch()
    print("Touchscreen ready. Tap to see output.")
    while True:
        touch = ts.get_touch()
        if touch:
            print(f"Touch at x={touch['x']}, y={touch['y']}, pressure={touch['pressure']}")
        time.sleep(0.05)
