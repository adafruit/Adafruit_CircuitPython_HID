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
`adafruit_hid.digitizer.Digitizer`
====================================================

* Author(s): Dan Halbert
"""
import struct
import time
import usb_hid

class Digitizer:
    """Emulate a generic digitizer tablet and stylus.
    The stylus has a tip switch, barrel switch, eraser switch,
    and can report that it is inverted (upside down).

    The ``x`` and ``y`` position values range from 0 to 32767.
    """

    IN_RANGE = 0x01
    """Stylus is in-range of digitizer. Must be set to register switch state."""
    TIP_SWITCH = 0x02
    """Stylus tip switch."""
    BARREL_SWITCH = 0x04
    """Stylus barrel switch."""
    ERASER_SWITCH = 0x08
    """Stylus eraser switch."""

    def __init__(self):
        """Create a Digitizer object that will send USB digitizer HID reports."""
        self.hid_digitizer = None
        for device in usb_hid.devices:
            if device.usage_page == 0x0D and device.usage == 0x02:
                self._hid_digitizer = device
                break
        if not self._hid_digitizer:
            raise IOError("Could not find an HID digitizer device.")

        # Reuse this bytearray to send digitizer reports.
        # report[0] stylus buttons and state
        # report[1-2] x position
        # report[3-4] y position
        self._report = bytearray(5)

        self._stylus_state = 0
        # Center to start with.
        self._x_pos = 16384
        self._y_pos = 16384

        # Send a report to see if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self._send()
        except OSError:
            time.sleep(1)
            self._send()

    def stylus_set(self, stylus_state):
        """Press and turn on the given stylus buttons and state bits.
        Existing state is not changed.

        :param stylus: a bitwise-or'd combination of ``IN_RANGE``, ``TIP_SWITCH``,
            ``BARREL_SWITCH``, and ``ERASER_SWITCH`.

        Example::

            # Press the tip switch.
            d.stylus_set(Digitizer.TIP_SWITCH | Digitizer.IN_RANGE)
        """
        self._stylus_state |= stylus_state
        self._send()

    def stylus_clear(self, stylus_state):
        """Release or turn off the given stylus buttons and state bits.
        Existing state is not changed.

        :param stylus: a bitwise-or'd combination of ``IN_RANGE``, ``TIP_SWITCH``,
            ``BARREL_SWITCH``, and ``ERASER_SWITCH`.

        Example::

            # Press the tip switch.
            d.stylus_set(Digitizer.TIP_SWITCH | Digitizer.BARREL_SWITCH)
            # Release the tip switch, but continue to press the barrel switch.
            d.stylus_clear(Digitizer.TIP_SWITCH)
        """
        self._stylus_state &= ~stylus_state
        self._send()

    def stylus_clear_all(self):
        """Turn off and release all stylus buttons and state bits."""
        self._stylus_state = 0
        self._send()

    def click(self, stylus_state):
        """Cycle on and off and press and release the
        given stylus buttons and state bits.

        :param stylus: a bitwise-or'd combination of ``IN_RANGE``, ``TIP_SWITCH``,
            ``BARREL_SWITCH``, and ``ERASER_SWITCH`.

        Examples::

            # Click the stylus barrel switch while touching the digitizer.
            d.set_stylus(Digitizer.BARREL_SWITCH)

        """
        self.stylus_set(stylus_state)
        self.stylus_clear(stylus_state)

    def move_to(self, x=0, y=0):
        """Move the stylus to the indicated position.

        :param x: Position on the x axis. Negative is to the left, positive
            is to the right.
        :param y: Position on the y axis. Negative is upwards on the display,
            positive is downwards.

        ``x`` and ``y`` must be in the range 0 to 32767.

        Examples::

            # Move to the upper left.
            d.move_to(0, 0)
            # move to the center.
            m.move_to(16384, 16384)
        """
        self._x_pos = self._validate_position(x)
        self._y_pos = self._validate_position(y)
        self._send()

    def _send(self):
        """Send a button-only report."""
        struct.pack_into("<BHH", self._report, 0,
                         self._stylus_state, self._x_pos, self._y_pos)
        self._hid_digitizer.send_report(self._report)

    @staticmethod
    def _validate_position(pos):
        if not 0 <= pos <= 32767:
            raise ValueError("x and y must be in range 0 to 32767")
        return pos
