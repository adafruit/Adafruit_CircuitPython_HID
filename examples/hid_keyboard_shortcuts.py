# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)

# define buttons. these can be any physical switches/buttons, but the values
# here work out-of-the-box with a CircuitPlayground Express' A and B buttons.
swap = digitalio.DigitalInOut(board.D4)
swap.direction = digitalio.Direction.INPUT
swap.pull = digitalio.Pull.DOWN

search = digitalio.DigitalInOut(board.D5)
search.direction = digitalio.Direction.INPUT
search.pull = digitalio.Pull.DOWN

while True:
    # press ALT+TAB to swap windows
    if swap.value:
        kbd.send(Keycode.ALT, Keycode.TAB)

    # press CTRL+K, which in a web browser will open the search dialog
    elif search.value:
        kbd.send(Keycode.CONTROL, Keycode.K)

    time.sleep(0.1)
