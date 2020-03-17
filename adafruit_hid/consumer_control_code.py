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
`adafruit_hid.consumer_control_code.ConsumerControlCode`
========================================================

* Author(s): Dan Halbert
"""


class ConsumerControlCode:
    """USB HID Consumer Control Device constants.

    This list includes a few common consumer control codes from
    http://www.usb.org/developers/hidpage/Hut1_12v2.pdf#page=75.

    *New in CircuitPython 3.0.*
    """

    # pylint: disable-msg=too-few-public-methods

    RECORD = 0xB2
    """Record"""
    FAST_FORWARD = 0xB3
    """Fast Forward"""
    REWIND = 0xB4
    """Rewind"""
    SCAN_NEXT_TRACK = 0xB5
    """Skip to next track"""
    SCAN_PREVIOUS_TRACK = 0xB6
    """Go back to previous track"""
    STOP = 0xB7
    """Stop"""
    EJECT = 0xB8
    """Eject"""
    PLAY_PAUSE = 0xCD
    """Play/Pause toggle"""
    MUTE = 0xE2
    """Mute"""
    VOLUME_DECREMENT = 0xEA
    """Decrease volume"""
    VOLUME_INCREMENT = 0xE9
    """Increase volume"""
