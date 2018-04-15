# The MIT License (MIT)
#
# Copyright (c) 2018 Dan Halbert for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

"""
`adafruit_hid.gamepad.Gamepad`
====================================================

* Author(s): Dan Halbert
"""
import time
import usb_hid

class Gamepad:
    """Emulate a generic gamepad controller with 16 buttons,
    numbered 1-16, and two joysticks, one controlling
    ``x` and ``y`` values, and the other controlling ``z`` and
    ``r_z`` (z rotation or ``Rz``) values.

    The joystick values could be interpreted
    differently by the receiving program: those are just the names used here.
    The joystick values are in the range -127 to 127.
"""

    def __init__(self):
        """Create a Gamepad object that will send USB gamepad HID reports."""
        self._hid_gamepad = None
        for device in usb_hid.devices:
            if device.usage_page == 0x1 and device.usage == 0x05:
                self._hid_gamepad = device
                break
        if not self._hid_gamepad:
            raise IOError("Could not find an HID gampead device.")

        # Reuse this bytearray to send mouse reports.
        # Typically controllers start numbering buttons at 1 rather than 0.
        # report[0] buttons 1-8 (LSB is button 1)
        # report[1] buttons 9-16
        # report[2] joystick 0 x: -127 to 127
        # report[3] joystick 0 y: -127 to 127
        # report[4] joystick 1 x: -127 to 127
        # report[5] joystick 1 y: -127 to 127
        self._report = bytearray(6)

        # Remember the last report as well, so we can avoid sending
        # duplicate reports.
        self._last_report = bytearray(6)

        # Store settings separately before putting into report. Saves code
        # especially for buttons.
        self._buttons_state = 0
        self._joy_x = 0
        self._joy_y = 0
        self._joy_z = 0
        self._joy_r_z = 0

        # Send an initial report to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.reset_all()
        except OSError:
            time.sleep(1)
            self.reset_all()

    def set_pressed_buttons(self, *buttons):
        """Mark the given buttons as pressed.
        Other buttons are not changed. Do not send a report yet."

        Example::

            g.clear_all_buttons()
            g.set_buttons(3, 11)
            # Send a report indicating buttons 3 and 11 are pressed.
            g.send()
        """

        for button in buttons:
            self._validate_button_number(button)
            self._buttons_state |= 1 << button - 1


    def set_released_buttons(self, *buttons):
        """Mark the given buttons as released.
        Other buttons are not changed. Do not send a report yet."
        """

        for button in buttons:
            self._validate_button_number(button)
            self._buttons_state &= ~(1 << button - 1)

    def press_buttons(self, *buttons):
        """Press and hold the given buttons. """

        self.set_pressed_buttons(*buttons)
        self.send()

    def release_buttons(self, *buttons):
        """Release the given buttons. """

        self.set_released_buttons(*buttons)
        self.send()

    def release_all_buttons(self):
        """Release all the buttons."""

        self._buttons_state = 0
        self.send()

    def click_buttons(self, *buttons):
        """Press and release the given buttons."""
        self.press_buttons(*buttons)
        self.release_buttons(*buttons)

    def set_joysticks(self, x=None, y=None, z=None, r_z=None):
        """Set the given joystick values in the report to be sent.
        Do not send a report yet.

        One joystick provides ``x`` and ``y`` values,
        and the other provides ``z`` and ``r_z`` (z rotation).
        Any values left as ``None`` will not be changed.

        All values must be in the range -127 to 127 inclusive.

        Examples::

            # Change x and y values only.
            gp.set_joysticks(x=100, y=-50)

            # Reset all joystick values to center position.
            gp.set_joysticks(0, 0, 0, 0)
        """
        if x is not None:
            self._validate_joystick_value(x)
            self._joy_x = x
        if y is not None:
            self._validate_joystick_value(y)
            self._joy_y = y
        if z is not None:
            self._validate_joystick_value(z)
            self._joy_z = z
        if r_z is not None:
            self._validate_joystick_value(r_z)
            self._joy_r_z = r_z

    def move_joysticks(self, x=None, y=None, z=None, r_z=None):
        """Set and send the given joystick values.
        The joysticks will remain set with the given values until changed."""
        self.set_joysticks(x, y, z, r_z)
        self.send()

    def reset_all(self):
        """Release all buttons and set joysticks to zero."""
        self._buttons_state = 0
        self.set_joysticks(0, 0, 0, 0)
        self.send(always=True)

    def send(self, always=False):
        """Send a report with all the existing settings.
        If ``always`` is ``False`` (the default), send only if there have been changes.
        """
        self._report[0] = self._buttons_state & 0xff
        self._report[1] = self._buttons_state >> 8
        self._report[2] = self._joy_x
        self._report[3] = self._joy_y
        self._report[4] = self._joy_z
        self._report[5] = self._joy_r_z

        if always or self._last_report != self._report:
            self._hid_gamepad.send_report(self._report)
            # Remember what we sent, without allocating a new report buffer.
            self._last_report[:] = self._report

    @staticmethod
    def _validate_button_number(button):
        if not 1 <= button <= 16:
            raise ValueError("Button number must in range 1 to 16")

    @staticmethod
    def _validate_joystick_value(value):
        if not -127 <= value <= 127:
            raise ValueError("Joystick value must be in range -127 to 127")
