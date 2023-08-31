# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)


# define buttons. these can be any physical switches/buttons, but the values
# here work out-of-the-box with a CircuitPlayground Express' A and B buttons.
slow_write = digitalio.DigitalInOut(board.D4)
slow_write.direction = digitalio.Direction.INPUT
slow_write.pull = digitalio.Pull.DOWN

fast_write = digitalio.DigitalInOut(board.D5)
fast_write.direction = digitalio.Direction.INPUT
fast_write.pull = digitalio.Pull.DOWN

while True:
    # Write `Hello World!` slowly
    if slow_write.value:
        layout.write("Hello World!", delay=0.2)

    # Write `Hello World!` normally
    elif fast_write.value:
        layout.write("Hello World!")

    time.sleep(0.1)
