
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-hid/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/hid/en/latest/
    :alt: Documentation Status

.. image :: https://badges.gitter.im/adafruit/circuitpython.svg
    :target: https://gitter.im/adafruit/circuitpython?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
    :alt: Gitter

This driver provides USB HID related constants. In the future it will include
helper functions and classes as well.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

The current `keyboard` module stores key constants which make it easier to
construct keypress reports for a keyboard device.

.. code-block:: python

    import usb_hid
    import adafruit_hid.keyboard as kbd
    import time

    report = bytearray(8) # Keyboard reports are always 8 bytes.

    # Devices are initialized earlier so find the one for the keyboard.
    keyboard = None
    for device in usb_hid.devices:
        if device.usage_page is 0x1 and device.usage is 0x06:
            keyboard = device
            break

    # The first byte of the report includes a bitfield indicating which
    # modifiers are pressed. Their bit position is their code's difference from
    # 0xE0.
    report[0] |= 1 << (kbd.LEFT_SHIFT - 0xE0)
    # Normal keys are simply their byte code in bytes 2-7. When fewer than six
    # keys are pressed then the trailing bytes are zero.
    report[2] = kbd.A
    keyboard.send_report(report)

    time.sleep(0.1)

    # Clear the key presses and send another report.
    report[0] = 0
    report[2] = 0
    keyboard.send_report(report)

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_hid/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

API Reference
=============

.. toctree::
   :maxdepth: 2

   api
