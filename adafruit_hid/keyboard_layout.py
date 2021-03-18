# SPDX-FileCopyrightText: 2017 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_hid.keyboard_layout_us.KeyboardLayoutUS`
=======================================================

* Author(s): Dan Halbert, AngainorDev
"""

from .keycode import Keycode


class KeyboardLayout:
    """Map ASCII characters to appropriate keypresses on a standard US PC keyboard.

    Non-ASCII characters and most control characters will raise an exception.
    """
    # We use the top bit of each byte (0x80) to indicate
    # that the shift key should be pressed, and an extra 9th bit 0x100 for AltGr
    SHIFT_FLAG = 0x80
    ALTGR_FLAG = 0x100
    ASCII_TO_KEYCODE = ()
    NEED_ALTGR = ""

    def __init__(self, keyboard):
        """Specify the layout for the given keyboard.

        :param keyboard: a Keyboard object. Write characters to this keyboard when requested.

        Example::

            kbd = Keyboard(usb_hid.devices)
            layout = KeyboardLayoutUS(kbd)
        """

        self.keyboard = keyboard

    def write(self, string):
        """Type the string by pressing and releasing keys on my keyboard.

        :param string: A string of ASCII characters.
        :raises ValueError: if any of the characters are not ASCII or have no keycode
            (such as some control characters).

        Example::

            # Write abc followed by Enter to the keyboard
            layout.write('abc\\n')
        """
        for char in string:
            keycode = self._char_to_keycode(char)
            if char in self.NEED_ALTGR:
                # Add altgr modifier
                self.keyboard.press(Keycode.RIGHT_ALT)
            # If this is a shifted char, clear the SHIFT flag and press the SHIFT key.
            if keycode & self.SHIFT_FLAG:
                keycode &= ~self.SHIFT_FLAG
                self.keyboard.press(Keycode.SHIFT)
            self.keyboard.press(keycode)
            self.keyboard.release_all()

    def keycodes(self, char):
        """Return a tuple of keycodes needed to type the given character.

        :param char: A single ASCII character in a string.
        :type char: str of length one.
        :returns: tuple of Keycode keycodes.
        :raises ValueError: if ``char`` is not ASCII or there is no keycode for it.

        Examples::

            # Returns (Keycode.TAB,)
            keycodes('\t')
            # Returns (Keycode.A,)
            keycodes('a')
            # Returns (Keycode.SHIFT, Keycode.A)
            keycodes('A')
            # Raises ValueError because it's a accented e and is not ASCII
            keycodes('é')
        """
        keycode = self._char_to_keycode(char)
        if keycode & self.SHIFT_FLAG:
            return (Keycode.SHIFT, keycode & ~self.SHIFT_FLAG)
        if char in self.NEED_ALTGR:
            return (Keycode.RIGHT_ALT, keycode)

        return (keycode,)

    def _above128charval_to_keycode(self, char_val):
        raise ValueError("Not an ASCII character.")

    def _char_to_keycode(self, char):
        """Return the HID keycode for the given ASCII character, with the SHIFT_FLAG possibly set.

        If the character requires pressing the Shift key, the SHIFT_FLAG bit is set.
        You must clear this bit before passing the keycode in a USB report.
        """
        char_val = ord(char)
        if char_val > 128:
            return self._above128charval_to_keycode(char)
        keycode = self.ASCII_TO_KEYCODE[char_val]
        if keycode == 0:
            raise ValueError("No keycode available for character.")
        return keycode
