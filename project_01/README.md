# Sketch Interpreter

Hackster (hardware documentation): https://www.hackster.io/533535/edes-301-touchsreen-sketch-identifier-501ab1

## Configuration for PocketBeagle Drawing Classifier

This guide will walk you through setting up a touchscreen drawing classifier on a PocketBeagle. The system allows you to draw on an SPI display and classify the shape (e.g., circle or triangle) using local Python code.

1. Flash the SD Card

PocketBeagle's SD card should be flashed, images can be downloaded from beagleboard.org.

2. Update & Install Python Dependencies

Run the following commands on your PocketBeagle:

```bash
sudo apt-get update
sudo apt-get install build-essential python3-dev python3-setuptools python3-smbus zip -y
sudo apt-get install python3-pip -y
sudo pip3 install --upgrade setuptools
sudo pip3 install Adafruit_BBIO adafruit-blinka Pillow
```

3. Install Display and Touchscreen Libraries

```bash
# For SPI Display
sudo pip3 install adafruit-circuitpython-busdevice
sudo pip3 install adafruit-circuitpython-rgb-display
sudo apt-get install ttf-dejavu -y

# For Touchscreen (STMPE610)
sudo pip3 install adafruit-circuitpython-stmpe610
```

4. Clone Project

```bash
git clone https://github.com/winsonlin8/EDES301
cd final_code
```

As of right now, main.py is set up to work in the final_code director outside of project_01 directory.
Make sure your main.py, screen.py, touch.py, and configure_pins.sh are all in this folder.

5. Make configure_pins.sh Executable

```bash
chmod +x configure_pins.sh
```

6. Create Startup Script

Create a launch.sh file in the folder:

```bash
#!/bin/bash
sudo ./configure_pins.sh
python3 main.py
```

Make this file executable as well
```bash
chmod +x launch.sh
```

7. Setup systemd

Create file: 

```bash
sudo nano /etc/systemd/system/finalcode.service
```

Paste this: 

```bash
[Unit]
Description=Launch Display Drawing App
After=network.target

[Service]
ExecStart=/bin/bash /var/lib/cloud9/EDES301/final_code/launch.sh
WorkingDirectory=/var/lib/cloud9/EDES301/final_code
StandardOutput=inherit
StandardError=inherit
Restart=always
User=debian

[Install]
WantedBy=multi-user.target
```

Enable, start, reboot: 

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable finalcode.service
sudo systemctl start finalcode.service
```

8. Run it

On boot, PocketBeagle will run your configure_pins.sh and then launch the drawing classification interface automatically. Draw shapes on your screen and see them classified in real time (with restrictions)