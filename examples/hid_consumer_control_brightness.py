# SPDX-FileCopyrightText: 2021 Tim C for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import digitalio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

cc = ConsumerControl(usb_hid.devices)

# define buttons. these can be any physical switches/buttons, but the values
# here work out-of-the-box with a FunHouse UP and DOWN buttons.
button_up = digitalio.DigitalInOut(board.BUTTON_UP)
button_up.switch_to_input(pull=digitalio.Pull.DOWN)

button_down = digitalio.DigitalInOut(board.BUTTON_DOWN)
button_down.switch_to_input(pull=digitalio.Pull.DOWN)

while True:
    if button_up.value:
        print("Button up pressed!")
        # send brightness up button press
        cc.send(ConsumerControlCode.BRIGHTNESS_INCREMENT)

    if button_down.value:
        print("Button down pressed!")
        # send brightness down button press
        cc.send(ConsumerControlCode.BRIGHTNESS_DECREMENT)

    time.sleep(0.1)
