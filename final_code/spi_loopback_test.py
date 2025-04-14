import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)  # SPI0.0
spi.max_speed_hz = 1000000  # 1 MHz for safety
spi.mode = 0b00

print("Sending SPI test pattern...")
try:
    for i in range(10):
        sent = [0xAA, 0x55, i]
        received = spi.xfer2(sent)
        print(f"Sent: {sent}, Received: {received}")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass

spi.close()
