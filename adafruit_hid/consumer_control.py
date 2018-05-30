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
`adafruit_hid.consumer_control.ConsumerControl`
====================================================

* Author(s): Dan Halbert
"""

import sys
if sys.implementation[1][0] < 3:
    raise ImportError('{0} is not supported in CircuitPython 2.x or lower'.format(__name__))

# pylint: disable=wrong-import-position
import time
import usb_hid

class ConsumerControl:
    """Send ConsumerControl code reports, used by multimedia keyboards, remote controls, etc.

    *New in CircuitPython 3.0.*
    """

    def __init__(self):
        """Create a ConsumerControl object that will send Consumer Control Device HID reports."""
        self.hid_consumer = None
        for device in usb_hid.devices:
            if device.usage_page == 0x0C and device.usage == 0x01:
                self.hid_consumer = device
                break
        if not self.hid_consumer:
            raise IOError("Could not find an HID Consumer device.")

        # Reuse this bytearray to send consumer reports.
        self.report = bytearray(2)

        # View bytes as a single 16-bit number.
        self.usage_id = memoryview(self.report)[0:2]

        # Do a no-op to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.send(0x0)
        except OSError:
            time.sleep(1)
            self.send(0x0)

    def send(self, consumer_code):
        """Send a report to do the specified consumer control action,
        and then stop the action (so it will not repeat).

        :param consumer_code: a 16-bit consumer control code.

        Examples::

            from adafruit_hid.consumer_control_code import ConsumerControlCode

            # Raise volume.
            consumer_control.send(ConsumerControlCode.VOLUME_INCREMENT)

            # Advance to next track (song).
            consumer_control.send(ConsumerControlCode.SCAN_NEXT_TRACK)
        """
        self.usage_id[0] = consumer_code % 0x100
        self.usage_id[1] = consumer_code >> 8
        self.hid_consumer.send_report(self.report)
        self.usage_id[0] = 0x0
        self.usage_id[1] = 0x0
        self.hid_consumer.send_report(self.report)
