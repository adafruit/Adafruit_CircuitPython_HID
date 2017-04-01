
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-hid/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/hid/en/latest/
    :alt: Documentation Status

.. image :: https://badges.gitter.im/adafruit/circuitpython.svg
    :target: https://gitter.im/adafruit/circuitpython?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
    :alt: Gitter

This driver simulates USB HID devices, such as keyboard, mouse, and joystick.
Right now only keyboard is implemented.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

The ``keyboard`` module defines keycode constants and a ``Keyboard`` class to
construct and send keypress reports for a USB keyboard device.

.. code-block:: python

    from adafruit_hid.keyboard import Keyboard

    # Find a keyboard device to talk to.
    kbd = Keyboard()

    # Simulate typing. Press and release the A key (not shifted),
    # then the B key, then c, then the Enter key.
    # Type "abc" followed by return.
    kbd.type("abc\n")

    # Type control-x, then "Abc", then backspace.
    kbd.type((Keyboard.CONTROL, 'x'), 'Abc', Keyboard.BACKSPACE)

    # Press and hold left-hand Control and right-hand Alt.
    kbd.press_keys(Keyboard.CONTROL, Keyboard.ALT)

    # Press and hold the A and B keys (lower case, not shifted).
    kbd.press_keys('ab')

    # Press and hold the A and B keys (same effect as above).
    kbd.press_keys('a', 'b')

    # Press capital C. This implies pressing left Shift as well,
    # because the character is capitalized.
    kbd.press_keys('C')

    # Release the B key.
    kbd.release_keys('b')

    # Release all keys.
    kbd.release_all()

    # Press '5' on the keypad and the F8 key.
    kbd.press_keys(Keyboard.KEYPAD_FIVE, Keyboard.F8)

    # Press the shifted '1' key to get '!' (exclamation mark).
    kbd.press_keys(Keyboard.SHIFT, '1')

    # Same effect as above. The '!' implies pressing Shift and '1'.
    kbd.press_keys('!').



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
