# SPDX-FileCopyrightText: 2017 Scott Shawcroft for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_hid`
====================================================

This driver simulates USB HID devices.

* Author(s): Scott Shawcroft, Dan Halbert

Implementation Notes
--------------------
**Software and Dependencies:**
* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_HID.git"


def find_device(devices, *, usage_page, usage):
    """Search through the provided list of devices to find the one with the matching usage_page and
    usage."""
    if hasattr(devices, "send_report"):
        devices = [devices]
    for device in devices:
        if (
            device.usage_page == usage_page
            and device.usage == usage
            and hasattr(device, "send_report")
        ):
            return device
    raise ValueError("Could not find matching HID device.")
