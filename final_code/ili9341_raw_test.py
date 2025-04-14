from pathlib import Path
import spidev
import time
import Adafruit_BBIO.GPIO as GPIO

# Pin mapping (PocketBeagle pins)
DC_PIN = "P1_04"
RST_PIN = "P1_02"
CS_PIN = "P1_06"

# Setup GPIOs (no setmode needed)
GPIO.setup(DC_PIN, GPIO.OUT)
GPIO.setup(RST_PIN, GPIO.OUT)
GPIO.setup(CS_PIN, GPIO.OUT)

# Reset the display
GPIO.output(RST_PIN, GPIO.HIGH)
time.sleep(0.1)
GPIO.output(RST_PIN, GPIO.LOW)
time.sleep(0.1)
GPIO.output(RST_PIN, GPIO.HIGH)
time.sleep(0.1)

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI0.0
spi.max_speed_hz = 10000000
spi.mode = 0

def send_command(cmd):
    GPIO.output(DC_PIN, GPIO.LOW)
    GPIO.output(CS_PIN, GPIO.LOW)
    spi.writebytes([cmd])
    GPIO.output(CS_PIN, GPIO.HIGH)

def send_data(data):
    GPIO.output(DC_PIN, GPIO.HIGH)
    GPIO.output(CS_PIN, GPIO.LOW)
    if isinstance(data, list):
        spi.writebytes(data)
    else:
        spi.writebytes([data])
    GPIO.output(CS_PIN, GPIO.HIGH)

# ILI9341 init sequence (minimal)
send_command(0x01)  # Software reset
time.sleep(0.2)
send_command(0x28)  # Display OFF

send_command(0x3A)  # COLMOD: Pixel Format Set
send_data(0x55)     # 16-bit/pixel

send_command(0x36)  # Memory Access Control
send_data(0x48)     # MX, BGR

send_command(0x11)  # Sleep OUT
time.sleep(0.1)

send_command(0x29)  # Display ON
time.sleep(0.1)

# Fill screen with color (RED)
def fill_screen(color):
    send_command(0x2A)  # Column addr set
    send_data([0x00, 0x00, 0x00, 0xEF])  # X start/end (240 px)
    send_command(0x2B)  # Row addr set
    send_data([0x00, 0x00, 0x01, 0x3F])  # Y start/end (320 px)
    send_command(0x2C)  # Memory write

    pixel_data = [color >> 8, color & 0xFF] * (240 * 320)
    for i in range(0, len(pixel_data), 4096):
        send_data(pixel_data[i:i+4096])

fill_screen(0xF800)  # Red

# Write to file
Path("ili9341_raw_test.py").write_text(minimal_driver_code.strip())
"Minimal driver script 'ili9341_raw_test.py' created. Edit pin mappings for PocketBeagle and run with sudo."
