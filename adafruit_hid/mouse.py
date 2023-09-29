# SPDX-FileCopyrightText: 2017 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_hid.mouse.Mouse`
====================================================

* Author(s): Dan Halbert
"""
import time

from . import find_device

try:
    from typing import Sequence, Callable
    import usb_hid
except ImportError:
    pass


class Mouse:
    """Send USB HID mouse reports."""

    LEFT_BUTTON = 1
    """Left mouse button."""
    RIGHT_BUTTON = 2
    """Right mouse button."""
    MIDDLE_BUTTON = 4
    """Middle mouse button."""

    def __init__(self, devices: Sequence[usb_hid.Device], timeout: int = None) -> None:
        """Create a Mouse object that will send USB mouse HID reports.

        :param timeout: Time in seconds to wait for USB to become ready before timing out.
        Defaults to None to wait indefinitely.

        Devices can be a sequence of devices that includes a keyboard device or a keyboard device
        itself. A device is any object that implements ``send_report()``, ``usage_page`` and
        ``usage``.
        """
        self._mouse_device = find_device(
            devices, usage_page=0x1, usage=0x02, timeout=timeout
        )

        # Reuse this bytearray to send mouse reports.
        # report[0] buttons pressed (LEFT, MIDDLE, RIGHT)
        # report[1] x movement
        # report[2] y movement
        # report[3] wheel movement
        self.report = bytearray(4)

    def press(self, buttons: int) -> None:
        """Press the given mouse buttons.

        :param buttons: a bitwise-or'd combination of ``LEFT_BUTTON``,
            ``MIDDLE_BUTTON``, and ``RIGHT_BUTTON``.

        Examples::

            # Press the left button.
            m.press(Mouse.LEFT_BUTTON)

            # Press the left and right buttons simultaneously.
            m.press(Mouse.LEFT_BUTTON | Mouse.RIGHT_BUTTON)
        """
        self.report[0] |= buttons
        self._send_no_move()

    def release(self, buttons: int) -> None:
        """Release the given mouse buttons.

        :param buttons: a bitwise-or'd combination of ``LEFT_BUTTON``,
            ``MIDDLE_BUTTON``, and ``RIGHT_BUTTON``.
        """
        self.report[0] &= ~buttons
        self._send_no_move()

    def release_all(self) -> None:
        """Release all the mouse buttons."""
        self.report[0] = 0
        self._send_no_move()

    def click(self, buttons: int) -> None:
        """Press and release the given mouse buttons.

        :param buttons: a bitwise-or'd combination of ``LEFT_BUTTON``,
            ``MIDDLE_BUTTON``, and ``RIGHT_BUTTON``.

        Examples::

            # Click the left button.
            m.click(Mouse.LEFT_BUTTON)

            # Double-click the left button.
            m.click(Mouse.LEFT_BUTTON)
            m.click(Mouse.LEFT_BUTTON)
        """
        self.press(buttons)
        self.release(buttons)

    def _move_relative(self, x: int = 0, y: int = 0, wheel: int = 0) -> None:
        # Send multiple reports if necessary to move or scroll requested amounts.
        while x != 0 or y != 0 or wheel != 0:
            partial_x = self._limit(x)
            partial_y = self._limit(y)
            partial_wheel = self._limit(wheel)
            self.report[1] = partial_x & 0xFF
            self.report[2] = partial_y & 0xFF
            self.report[3] = partial_wheel & 0xFF
            self._mouse_device.send_report(self.report)
            x -= partial_x
            y -= partial_y
            wheel -= partial_wheel

    @staticmethod
    def _progress(
        duration: float,
        easing_function: Callable = None,
    ):
        start_time = time.monotonic()

        while (current_time := time.monotonic()) < start_time + duration:
            progress = (current_time - start_time) / duration

            if easing_function:
                progress = easing_function(progress)

            yield progress

        yield 1

    def move(
        self,
        x: int = 0,
        y: int = 0,
        wheel: int = 0,
        *,
        duration: float = 0,
        easing_function: "Callable" = None,
    ) -> None:
        """Move the mouse and turn the wheel as directed.

        :param x: Move the mouse along the x axis. Negative is to the left, positive
            is to the right.
        :param y: Move the mouse along the y axis. Negative is upwards on the display,
            positive is downwards.
        :param wheel: Rotate the wheel this amount. Negative is toward the user, positive
            is away from the user. The scrolling effect depends on the host.
        :param duration: If ``0`` (the default), move the mouse and turn the wheel as quickly as
            possible. Otherwise, move and turn the wheel over ``duration`` seconds.

        Examples::

            # Move 100 to the left. Do not move up and down. Do not roll the scroll wheel.
            m.move(-100, 0, 0)
            # Same, with keyword arguments.
            m.move(x=-100)

            # Move diagonally to the upper right.
            m.move(50, -20)
            # Same.
            m.move(x=50, y=-20)

            # Roll the mouse wheel away from the user.
            m.move(wheel=1)

            # Move 100 to the left during 2 seconds.
            m.move(x=-100, duration=2)
        """
        if duration == 0:
            self._move_relative(x, y, wheel)
            return

        last_x = last_y = last_wheel = 0

        for progress in self._progress(duration, easing_function):
            current_x = int(x * progress)
            current_y = int(y * progress)
            current_wheel = int(wheel * progress)

            self._move_relative(
                current_x - last_x, current_y - last_y, current_wheel - last_wheel
            )
            last_x, last_y, last_wheel = current_x, current_y, current_wheel

    def _send_no_move(self) -> None:
        """Send a button-only report."""
        self.report[1] = 0
        self.report[2] = 0
        self.report[3] = 0
        self._mouse_device.send_report(self.report)

    @staticmethod
    def _limit(dist: int) -> int:
        return min(127, max(-127, dist))
