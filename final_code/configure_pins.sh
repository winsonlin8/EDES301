#!/bin/bash
# --------------------------------------------------------------------------
# SPI Screen - Configure Pins
# --------------------------------------------------------------------------
# License:   
# Copyright 2020 Erik Welsh
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this 
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors 
# may be used to endorse or promote products derived from this software without 
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# --------------------------------------------------------------------------
# 
# Configure pins for:
#   - SPI0 Display (ILI9341)
#     * SCLK, MISO, MOSI
#     * CS, RST, D/C (GPIO)
#   - SPI1 Touchscreen Controller (STMPE610)
#     * SCLK, MISO, MOSI
#     * CS (GPIO)
# --------------------------------------------------------------------------

echo "Configuring SPI0 (Display)..."
config-pin P1_08 spi_sclk    # SPI0 SCLK
config-pin P1_10 spi         # SPI0 MISO
config-pin P1_12 spi         # SPI0 MOSI

config-pin P1_02 gpio        # RESET pin
config-pin P1_04 gpio        # D/C pin
config-pin P1_06 gpio        # CS pin

echo "Configuring SPI1 (Touchscreen)..."
config-pin P2_29 spi_sclk    # SPI1 SCLK
config-pin P2_27 spi         # SPI1 MISO
config-pin P2_25 spi         # SPI1 MOSI

config-pin P2_31 gpio        # CS pin for STMPE610

echo "All SPI pins configured."