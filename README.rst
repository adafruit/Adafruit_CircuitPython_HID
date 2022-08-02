
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-hid/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/hid/en/latest/
    :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_HID/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_HID/actions/
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black


This driver simulates USB HID devices. Currently keyboard and mouse are implemented.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Additional Layouts
====================
This library has an en-US layout. Please check out and expand `the library from Neradoc <https://github.com/Neradoc/Circuitpython_Keyboard_Layouts>`_ for additional layouts.

Usage Example
=============

The ``Keyboard`` class sends keypress reports for a USB keyboard device to the host.

The ``Keycode`` class defines USB HID keycodes to send using ``Keyboard``.

.. code-block:: python

    import usb_hid
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode

    # Set up a keyboard device.
    kbd = Keyboard(usb_hid.devices)

    # Type lowercase 'a'. Presses the 'a' key and releases it.
    kbd.send(Keycode.A)

    # Type capital 'A'.
    kbd.send(Keycode.SHIFT, Keycode.A)

    # Type control-x.
    kbd.send(Keycode.CONTROL, Keycode.X)

    # You can also control press and release actions separately.
    kbd.press(Keycode.CONTROL, Keycode.X)
    kbd.release_all()

    # Press and hold the shifted '1' key to get '!' (exclamation mark).
    kbd.press(Keycode.SHIFT, Keycode.ONE)
    # Release the ONE key and send another report.
    kbd.release(Keycode.ONE)
    # Press shifted '2' to get '@'.
    kbd.press(Keycode.TWO)
    # Release all keys.
    kbd.release_all()

The ``KeyboardLayoutUS`` sends ASCII characters using keypresses. It assumes
the host is set to accept keypresses from a US keyboard.

If the host is expecting a non-US keyboard, the character to key mapping provided by
``KeyboardLayoutUS`` will not always be correct.
Different keypresses will be needed in some cases. For instance, to type an ``'A'`` on
a French keyboard (AZERTY instead of QWERTY), ``Keycode.Q`` should be pressed.

Currently this package provides only ``KeyboardLayoutUS``. More ``KeyboardLayout``
classes could be added to handle non-US keyboards and the different input methods provided
by various operating systems.

.. code-block:: python

    import usb_hid
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)

    # Type 'abc' followed by Enter (a newline).
    layout.write('abc\n')

    # Get the keycodes needed to type a '$'.
    # The method will return (Keycode.SHIFT, Keycode.FOUR).
    keycodes = layout.keycodes('$')

The ``Mouse`` class simulates a three-button mouse with a scroll wheel.

.. code-block:: python

    import usb_hid
    from adafruit_hid.mouse import Mouse

    m = Mouse(usb_hid.devices)

    # Click the left mouse button.
    m.click(Mouse.LEFT_BUTTON)

    # Move the mouse diagonally to the upper left.
    m.move(-100, -100, 0)

    # Roll the mouse wheel away from the user one unit.
    # Amount scrolled depends on the host.
    m.move(0, 0, -1)

    # Keyword arguments may also be used. Omitted arguments default to 0.
    m.move(x=-100, y=-100)
    m.move(wheel=-1)

    # Move the mouse while holding down the left button. (click-drag).
    m.press(Mouse.LEFT_BUTTON)
    m.move(x=50, y=20)
    m.release_all()       # or m.release(Mouse.LEFT_BUTTON)

The ``ConsumerControl`` class emulates consumer control devices such as
remote controls, or the multimedia keys on certain keyboards.

.. code-block:: python

    import usb_hid
    from adafruit_hid.consumer_control import ConsumerControl
    from adafruit_hid.consumer_control_code import ConsumerControlCode

    cc = ConsumerControl(usb_hid.devices)

    # Raise volume.
    cc.send(ConsumerControlCode.VOLUME_INCREMENT)

    # Pause or resume playback.
    cc.send(ConsumerControlCode.PLAY_PAUSE)

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/hid/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_hid/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
