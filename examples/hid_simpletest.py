# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import digitalio
import usb_hid
from adafruit_hid.mouse import Mouse

mouse = Mouse(usb_hid.devices)

# define buttons. these can be any physical switches/buttons, but the values
# here work out-of-the-box with a CircuitPlayground Express' A and B buttons.
up = digitalio.DigitalInOut(board.D4)
up.direction = digitalio.Direction.INPUT
up.pull = digitalio.Pull.DOWN

down = digitalio.DigitalInOut(board.D5)
down.direction = digitalio.Direction.INPUT
down.pull = digitalio.Pull.DOWN

while True:
    # scroll up one unit (varies with host/OS)
    if up.value:
        mouse.move(wheel=1)

    # scroll down one unit (varies with host/OS)
    elif down.value:
        mouse.move(wheel=-1)

    time.sleep(0.1)
