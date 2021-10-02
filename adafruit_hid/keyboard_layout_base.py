# SPDX-FileCopyrightText: 2017 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_hid.keyboard_layout_base.KeyboardLayoutBase`
=======================================================

* Author(s): Dan Halbert, AngainorDev, Neradoc
"""


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_HID.git"


class KeyboardLayoutBase:
    """Base class for keyboard layouts. Uses the tables defined in the subclass
    to map UTF-8 characters to appropriate keypresses.

    Non-supported characters and most control characters will raise an exception.
    """

    # We use the top bit of each byte (0x80) to indicate
    # that the shift key should be pressed
    SHIFT_FLAG = 0x80
    ALTGR_FLAG = 0x80
    SHIFT_CODE = 0xE1
    RIGHT_ALT_CODE = 0xE6
    ASCII_TO_KEYCODE = ()
    NEED_ALTGR = ""
    HIGHER_ASCII = {}
    COMBINED_KEYS = {}

    def __init__(self, keyboard):
        """Specify the layout for the given keyboard.

        :param keyboard: a Keyboard object. Write characters to this keyboard when requested.

        Example::

            kbd = Keyboard(usb_hid.devices)
            layout = KeyboardLayout(kbd)
        """
        self.keyboard = keyboard

    def _write(self, keycode, altgr=False):
        """Type a key combination based on shift bit and altgr bool

        :param keycode: int value of the keycode, with the shift bit.
        :param altgr: bool indicating if the altgr key should be pressed too.
        """
        # Add altgr modifier if needed
        if altgr:
            self.keyboard.press(self.RIGHT_ALT_CODE)
        # If this is a shifted char, clear the SHIFT flag and press the SHIFT key.
        if keycode & self.SHIFT_FLAG:
            keycode &= ~self.SHIFT_FLAG
            self.keyboard.press(self.SHIFT_CODE)
        self.keyboard.press(keycode)
        self.keyboard.release_all()

    def write(self, string):
        """Type the string by pressing and releasing keys on my keyboard.

        :param string: A string of ASCII characters.
        :raises ValueError: if any of the characters has no keycode
            (such as some control characters).

        Example::

            # Write abc followed by Enter to the keyboard
            layout.write('abc\\n')
        """
        for char in string:
            # find easy ones first
            keycode = self._char_to_keycode(char)
            if keycode > 0:
                self._write(keycode, char in self.NEED_ALTGR)
            # find combined keys
            elif ord(char) in self.COMBINED_KEYS:
                # first key (including shift bit)
                cchar = self.COMBINED_KEYS[ord(char)]
                self._write(cchar >> 8, cchar & self.ALTGR_FLAG)
                # second key (removing the altgr bit)
                char = chr(cchar & 0xFF & (~self.ALTGR_FLAG))
                keycode = self._char_to_keycode(char)
                # assume no altgr needed for second key
                self._write(keycode, False)
            else:
                raise ValueError(
                    "No keycode available for character {letter} ({num}/0x{num:02x}).".format(
                        letter=repr(char), num=ord(char)
                    )
                )

    def keycodes(self, char):
        """Return a tuple of keycodes needed to type the given character.

        :param char: A single UTF8 character in a string.
        :type char: str of length one.
        :returns: tuple of Keycode keycodes.
        :raises ValueError: if there is no keycode for ``char``.

        Examples::

            # Returns (Keycode.TAB,)
            keycodes('\t')
            # Returns (Keycode.A,)
            keycode('a')
            # Returns (Keycode.SHIFT, Keycode.A)
            keycode('A')
            # Raises ValueError with a US layout because it's an unknown character
            keycode('é')
        """
        keycode = self._char_to_keycode(char)
        if keycode == 0:
            raise ValueError(
                "No keycode available for character {letter} ({num}/0x{num:02x}).".format(
                    letter=repr(char), num=ord(char)
                )
            )

        codes = []
        if char in self.NEED_ALTGR:
            codes.append(self.RIGHT_ALT_CODE)
        if keycode & self.SHIFT_FLAG:
            codes.extend((self.SHIFT_CODE, keycode & ~self.SHIFT_FLAG))
        else:
            codes.append(keycode)

        return codes

    def _above128char_to_keycode(self, char):
        """Return keycode for above 128 ascii codes.

        A character can be indexed by the char itself or its int ord() value.

        :param char_val: ascii char value
        :return: keycode, with modifiers if needed
        """
        if ord(char) in self.HIGHER_ASCII:
            return self.HIGHER_ASCII[ord(char)]
        if char in self.HIGHER_ASCII:
            return self.HIGHER_ASCII[char]
        return 0

    def _char_to_keycode(self, char):
        """Return the HID keycode for the given ASCII character, with the SHIFT_FLAG possibly set.

        If the character requires pressing the Shift key, the SHIFT_FLAG bit is set.
        You must clear this bit before passing the keycode in a USB report.
        """
        char_val = ord(char)
        if char_val > len(self.ASCII_TO_KEYCODE):
            return self._above128char_to_keycode(char)
        keycode = self.ASCII_TO_KEYCODE[char_val]
        return keycode
