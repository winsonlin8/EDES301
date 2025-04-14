# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
SPI Display Library
--------------------------------------------------------------------------
License:   
Copyright 2021 Erik Welsh

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
Software API:

  SPI_DISPLAY()
    - Provide spi bus that dispaly is on
    - Provide spi address for the display
    
    blank()
      - Fills the display with black (i.e. color (0,0,0))
    
    fill(color)
      - Fills the display with the given (R, G, B) color tuple
    
    image(filename, rotation=90)
      - Erases display and shows image from filename
    
    text(value, fontsize=24, fontcolor=(255,255,255), backgroundcolor=(0,0,0), 
                justify=LEFT, align=TOP, rotation=90):
      - Erases display and shows text value on display
      - Value can either be a string or list of strings for multiple lines of text

--------------------------------------------------------------------------
Background Information: 

Links:
  - https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/overview
  - https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/spi-wiring-and-test
  - https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/python-wiring-and-setup
  - https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/python-usage

  - https://circuitpython.readthedocs.io/projects/rgb_display/en/latest/api.html#module-adafruit_rgb_display.rgb
  - https://circuitpython.readthedocs.io/projects/rgb_display/en/latest/_modules/adafruit_rgb_display/rgb.html
  
Software Setup:
  - sudo apt-get update
  - sudo pip3 install --upgrade Pillow
  - sudo pip3 install adafruit-circuitpython-busdevice
  - sudo pip3 install adafruit-circuitpython-rgb-display
  - sudo apt-get install ttf-dejavu -y

"""

import time
import busio
import board
import digitalio
import microcontroller
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import color565
import adafruit_rgb_display.ili9341 as ili9341
from microcontroller import pin as mpin

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------
LEFT    = 0
RIGHT   = 1
TOP     = 2
BOTTOM  = 3
CENTER  = 4
PADDING = -5

# ------------------------------------------------------------------------
# Display Class
# ------------------------------------------------------------------------
class SPI_Display():
    def __init__(self, clk_pin=board.SCLK, miso_pin=board.MISO, mosi_pin=board.MOSI,
                       cs_pin=board.P1_6, dc_pin=board.P1_4, reset_pin=board.P1_2,
                       baudrate=4000000, rotation=270):
        """ SPI Display Constructor
        
        :param clk_pin   : Value must be a pin from adafruit board library
        :param miso_pin  : Value must be a pin from adafruit board library
        :param mosi_pin  : Value must be a pin from adafruit board library
        :param cs_pin    : Value must be a pin from adafruit board library
        :param dc_pin    : Value must be a pin from adafruit board library
        :param reset_pin : Value must be a pin from adafruit board library
        :param baudrate  : SPI communication rate; default 24MHz
        :param rotation  : Rotation of display; default 90 degrees (landscape)
        
        """
        print("Initializing SPI Display...")
        print("Using SPI0 with CS, DC, RST on:", cs_pin, dc_pin, reset_pin)
        # Configuration for CS and DC pins:
        self.reset_pin = digitalio.DigitalInOut(reset_pin)
        self.dc_pin    = digitalio.DigitalInOut(dc_pin)
        self.cs_pin    = digitalio.DigitalInOut(cs_pin)

        # Setup SPI bus using hardware SPI
        self.spi_bus   = busio.SPI(clock=clk_pin, MISO=miso_pin, MOSI=mosi_pin)

        self.reset_pin = digitalio.DigitalInOut(reset_pin)
        self.reset_pin.direction = digitalio.Direction.OUTPUT
        self.reset_pin.value = False
        time.sleep(0.1)
        self.reset_pin.value = True
        time.sleep(0.1)

        # Create the ILI9341 display:
        self.display   = ili9341.ILI9341(self.spi_bus, cs=self.cs_pin, dc=self.dc_pin,
                                         rst=self.reset_pin, baudrate=baudrate, rotation=rotation)
        
        # Initialize Hardware
        self._setup()
        print("Display initialized!")

    def _setup(self):
        self.blank()

    def blank(self):
        self.fill((0, 0, 0))

    def fill(self, color):
        self.display.fill(color565(color[0], color[1], color[2]))

    def _get_dimensions(self, rotation):
        if rotation % 180 == 90:
            return (self.display.height, self.display.width)
        return (self.display.width, self.display.height)

    def image(self, filename, rotation=90):
        self.blank()
        image = Image.open(filename)
        width, height = self._get_dimensions(rotation)

        image_ratio  = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width  = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width  = width
            scaled_height = image.height * width // image.width

        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
        x = scaled_width  // 2 - width  // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))
        self.display.image(image)

    def text_fit(self, value, width):
        return [value[i:i + width] for i in range(0, len(value), width)]

    def text(self, value, fontsize=24, fontcolor=(255, 255, 255),
                   backgroundcolor=(0, 0, 0), justify=LEFT, align=TOP,
                   rotation=90):
        if justify not in [LEFT, CENTER, RIGHT]:
            raise ValueError("Invalid justify option")
        if align not in [TOP, CENTER, BOTTOM]:
            raise ValueError("Invalid align option")

        if not isinstance(value, list):
            value = [value]

        self.fill(backgroundcolor)
        width, height = self._get_dimensions(rotation)
        canvas = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)
        font_height = font.getsize(" ")[1]
        num_line = height // font_height

        if len(value) > num_line:
            value = value[:num_line]

        text_height = len(value) * font_height
        y = {
            TOP: 0,
            CENTER: (height - text_height) // 2,
            BOTTOM: height - text_height
        }.get(align, align) + PADDING

        for line in value:
            line_width = font.getsize(line)[0]
            if line_width > width:
                for i in range(len(line), 0, -1):
                    if font.getsize(line[:i])[0] <= width:
                        line = line[:i]
                        break

            x = {
                LEFT: 0,
                CENTER: (width - line_width) // 2,
                RIGHT: width - line_width
            }.get(justify, 0)

            draw.text((x, y), line, font=font, fill=fontcolor)
            y += font_height

        self.display.image(canvas)
