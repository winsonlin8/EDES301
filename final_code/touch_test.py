import time
import board
import busio
import digitalio
from adafruit_stmpe610 import Adafruit_STMPE610_SPI

# PocketBeagle SPI1 Pins
SCK_PIN  = board.P2_29   # SPI1_SCLK
MOSI_PIN = board.P2_25   # SPI1_D1
MISO_PIN = board.P2_27   # SPI1_D0
CS_PIN   = board.P2_31   # Chip Select for STMPE610

class STMPE610Touch:
    def __init__(self,
                 baudrate=1000000,
                 calibration=((0, 4095), (0, 4095)),
                 size=(320, 240),
                 rotation=0):

        # Setup SPI bus
        self.spi = busio.SPI(clock=SCK_PIN, MOSI=MOSI_PIN, MISO=MISO_PIN)

        # Setup CS pin
        self.cs = digitalio.DigitalInOut(CS_PIN)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.cs.value = True

        # Initialize STMPE610 driver
        self.touch = Adafruit_STMPE610_SPI(self.spi,
                                           self.cs,
                                           baudrate=baudrate,
                                           calibration=calibration,
                                           size=size,
                                           disp_rotation=rotation)

    def get_touch(self):
        if self.touch.touched:
            x, y, pressure = self.touch.touch_point
            return {'x': x, 'y': y, 'pressure': pressure}
        return None


def main():
    print("Initializing STMPE610 touchscreen...")
    ts = STMPE610Touch()
    print("Touchscreen initialized. Touch the screen to see coordinates.\n")

    while True:
        touch = ts.get_touch()
        if touch:
            print(f"Touch at x={touch['x']}, y={touch['y']}, pressure={touch['pressure']}")
        time.sleep(0.05)


if __name__ == '__main__':
    main()
