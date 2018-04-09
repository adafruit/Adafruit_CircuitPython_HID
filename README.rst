
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-hid/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/hid/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.org/adafruit/Adafruit_CircuitPython_HID.svg?branch=master
    :target: https://travis-ci.org/adafruit/Adafruit_CircuitPython_HID
    :alt: Build Status


This driver simulates USB HID devices. Currently keyboard and mouse are implemented.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

.. note::

   A "startup race" condition can occur when using HID on some systems. The use of
   a pause (``time.sleep()``) before creating a HID instance in your code will allow
   the host system to finish setting up the device on the USB bus.

The ``Keyboard`` class sends keypress reports for a USB keyboard device to the host.

The ``Keycode`` class defines USB HID keycodes to send using ``Keyboard``.

.. code-block:: python

    import time
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode

    # Sleep for a bit to avoid a race condition on some systems
    # when creating a HID instance
    time.sleep(1)

    # Set up a keyboard device.
    kbd = Keyboard()

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

    import time
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

    # Sleep for a bit to avoid a race condition on some systems
    # when creating a HID instance
    time.sleep(1)

    kbd = Keyboard()
    layout = KeyboardLayoutUS(kbd)

    # Type 'abc' followed by Enter (a newline).
    layout.write('abc\n')

    # Get the keycodes needed to type a '$'.
    # The method will return (Keycode.SHIFT, Keycode.FOUR).
    keycodes = layout.keycodes('$')

The ``Mouse`` class simulates a three-button mouse with a scroll wheel.

.. code-block:: python

    import time
    from adafruit_hid.mouse import Mouse

    # Sleep for a bit to avoid a race condition on some systems
    # when creating a HID instance
    time.sleep(1)

    m = Mouse()

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

*New in CircuitPython 3.0.*

.. code-block:: python

    import time
    from adafruit_hid.consumer_control import ConsumerControl
    from adafruit_hid.consumer_control_code import ConsumerControlCode

    # Sleep for a bit to avoid a race condition on some systems
    # when creating a HID instance
    time.sleep(1)

    cc = ConsumerControl()

    # Raise volume.
    cc.send(ConsumerCode.VOLUME_INCREMENT)

    # Pause or resume playback.
    cc.send(ConsumerCode.PLAY_PAUSE)

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_hid/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Building locally
================

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

    source .env/bin/activate

Then run the build:

.. code-block:: shell

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-hid --library_location .

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.
