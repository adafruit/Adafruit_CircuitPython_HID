# SPDX-FileCopyrightText: 2018 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_hid.consumer_control_code.ConsumerControlCode`
========================================================

* Author(s): Dan Halbert
"""


class ConsumerControlCode:
    """USB HID Consumer Control Device constants.

    This list includes a few common consumer control codes from
    https://www.usb.org/sites/default/files/hut1_21_0.pdf#page=118.
    """

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
    BRIGHTNESS_DECREMENT = 0x70
    """Decrease Brightness"""
    BRIGHTNESS_INCREMENT = 0x6F
    """Increase Brightness"""
    AL_CONSUMER_CONTROL_CONFIGURATION=0x0183
    """Launch generic controls for device"""
    AL_EMAIL_READER=0x018A
    """Launch e-mail reader"""
    AL_CALCULATOR=0x0192
    """Launch calculator"""
    AL_LOCAL_MACHINE_BROWSER=0x0194
    """Launch local machine file browser"""
    AC_SEARCH=0x0194
    """Search for documents"""
    AC_HOME=0x0221
    """Load the root of a set of objects"""
    AC_BACK=0x0223
    """Load the previous document"""
    AC_FORWARD=0x0224
    """Load the next document"""
    AC_STOP=0x0226
    """Stop loading of the current document"""
    AC_REFRESH=0x0227
    """Reload the current document"""
    AC_BOOKMARKS=0x022A
    """Display a list of stored links"""
