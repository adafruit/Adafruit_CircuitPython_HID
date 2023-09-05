Simple test
------------

Ensure your device works with this simple test.

.. literalinclude:: ../examples/hid_simpletest.py
    :caption: examples/hid_simpletest.py
    :linenos:

Keyboard Shortcuts
-------------------

Send ALT+Tab for swapping windows, and CTRL+K for searching in a browser.

.. literalinclude:: ../examples/hid_keyboard_shortcuts.py
    :caption: examples/hid_keyboard_shortcuts.py
    :linenos:

Keyboard Layout
---------------

While the ``Keyboard`` class itself provides easy way for sending key shortcuts, for writing more
complex text you may want to use a ``KeyboardLayout`` and a ``.write()`` method.

It is also possible to adjust the typing speed by specifying ``delay`` between key presses.

.. literalinclude:: ../examples/hid_keyboard_layout.py
    :caption: examples/hid_keyboard_layout.py
    :emphasize-lines: 12-13,29,33
    :linenos:

Simple Gamepad
---------------

Send gamepad buttons and joystick to the host.

.. literalinclude:: ../examples/hid_simple_gamepad.py
    :caption: examples/hid_simple_gamepad.py
    :linenos:

HID Joywing
------------

Use Joy FeatherWing to drive Gamepad.

.. literalinclude:: ../examples/hid_joywing_gamepad.py
    :caption: examples/hid_joywing_gamepad.py
    :linenos:

Consumer Control Brightness
----------------------------

Send brightness up and down consumer codes to the host.

.. literalinclude:: ../examples/hid_consumer_control_brightness.py
    :caption: examples/hid_consumer_control_brightness.py
    :linenos:
