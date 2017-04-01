# The MIT License (MIT)
#
# Copyright (c) 2017 Scott Shawcroft for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

"""
:mod:`adafruit_hid.Keyboard`
====================================================

* Author(s): Scott Shawcroft, Dan Halbert
"""

from micropython import const
import usb_hid

class Keyboard:
    """Send HID keyboard reports. You can send low-level raw keycodes, or send ASCII strings.

    Constants for non-printing and a few printing keys are defined here for convenience.
    Constants for the printing keys (a, comma, etc.) are not included to save memory space.
    Use the unshifted ASCII character instead. So to indicate the ``A`` key, use 'a' (not 'A').
    Likewise, for example, for the comma key, use ',', not '<'.

    USB keycodes are defined in  http://www.usb.org/developers/hidpage/Hut1_12v2.pdf#page=58.

    Remember that keycodes are the names for key *positions* on a US keyboard, and may
    not correspond to the character that you mean to send if you want to emulate non-US keyboard.
    For instance, on a French keyboard (AZERTY instead of QWERTY),
    the keycode for 'q' is used to indicate an 'a'. Likewise, 'y' represents 'z' on
    a German keyboard. This is historical: the idea was that the keycaps could be changed
    without changing the keycodes sent, so that different firmware was not needed for
    different variations of a keyboard.
    """

    ENTER = 0x28
    """Keycode for Return (Enter)"""
    RETURN = ENTER
    """Alias for Enter"""
    ESCAPE = 0x29
    BACKSPACE = 0x2A
    """Delete backward (Backspace)"""
    TAB = 0x2B
    SPACEBAR = 0x2C

    CAPS_LOCK = 0x39
    """Caps Lock"""

    F1 = 0x3A
    """Function key F1"""
    F2 = 0x3B
    """etc."""
    F3 = 0x3C
    F4 = 0x3D
    F5 = 0x3E
    F6 = 0x3F
    F7 = 0x40
    F8 = 0x41
    F9 = 0x42
    F10 = 0x43
    F11 = 0x44
    F12 = 0x45

    PRINT_SCREEN = 0x46
    """Print Screen (SysRq)"""
    SCROLL_LOCK = 0x47
    PAUSE = 0x48
    """Pause (Break)"""
    INSERT = 0x49
    HOME = 0x4A
    PAGE_UP = 0x4B
    DELETE = 0x4C
    """Delete forward"""
    END = 0x4D
    PAGE_DOWN = 0x4E
    RIGHT_ARROW = 0x4F
    LEFT_ARROW = 0x50
    DOWN_ARROW = 0x51
    UP_ARROW = 0x52

    KEYPAD_NUMLOCK = 0x53
    """Num Lock (Clear on some keyboards)"""
    KEYPAD_FORWARD_SLASH = 0x54
    KEYPAD_ASTERISK = 0x55
    KEYPAD_MINUS = 0x56
    KEYPAD_PLUS = 0x57
    KEYPAD_ENTER = 0x58
    KEYPAD_ONE = 0x59
    """Keypad ``1`` and End"""
    KEYPAD_TWO = 0x5A
    """Keypad ``2`` and Down Arrow"""
    KEYPAD_THREE = 0x5B
    """Keypad ``3`` and PgDn"""
    KEYPAD_FOUR = 0x5C
    """Keypad ``4`` and Left Arrow"""
    KEYPAD_FIVE = 0x5D
    KEYPAD_SIX = 0x5E
    """Keypad ``6`` and Right Arrow"""
    KEYPAD_SEVEN = 0x5F
    """Keypad ``7`` and Home"""
    KEYPAD_EIGHT = 0x60
    """Keypad ``8`` and Up Arrow"""
    KEYPAD_NINE = 0x61
    """Keypad ``9`` and PgUp"""
    KEYPAD_ZERO = 0x62
    """Keypad ``0`` and Ins"""
    KEYPAD_PERIOD = 0x63
    """Keypad ``.`` and Del"""
    KEYPAD_BACKSLASH = 0x64
    """Keypad ``\\`` and ``|`` (Non-US)"""

    APPLICATION = 0x65
    """Application (104-key keyboard)"""

    LEFT_CONTROL = 0xE0
    """Control modifier left of the spacebar."""
    CONTROL = LEFT_CONTROL
    """Convenient alias for LEFT_CONTROL."""
    LEFT_SHIFT = 0xE1
    """Shift modifier left of the spacebar."""
    SHIFT = LEFT_SHIFT
    """Alias for LEFT_SHIFT."""
    LEFT_ALT = 0xE2
    """Alt modifier left of the spacebar."""
    ALT = LEFT_ALT
    """Alias for LEFT_ALT"""
    LEFT_GUI = 0xE3
    """GUI modifier (aka Windows key, Option or Meta) left of the spacebar."""
    GUI = LEFT_GUI
    """Alias for LEFT_GUI"""
    RIGHT_CONTROL = 0xE4
    """Control modifier right of the spacebar."""
    RIGHT_SHIFT = 0xE5
    """Shift modifier right of the spacebar."""
    RIGHT_ALT = 0xE6
    """Alt modifier right of the spacebar."""
    RIGHT_GUI = 0xE7
    """GUI modifier (aka Windows key, Option or Meta) right of the spacebar."""

    # The ASCII_TO_KEYCODE bytes object is used as a table to maps ASCII 0-127
    # to the corresponding # keycode on a US 104-key keyboard.
    # The user should not normally need to use this table,
    # but it is not marked as private.
    #
    # Because the table only goes to 127, we use the top bit of each byte (ox80) to indicate
    # that the shift key should be pressed. So any values 0x{8,9,a,b}* are shifted characters.
    #
    # The Python compiler will concatenate all these bytes literals into a single bytes object.
    # Micropython/CircuitPython will store the resulting bytes constant in flash memory
    # if it's in a .mpy file, so it doesn't use up valuable RAM.
    #
    # \x00 entries have no keyboard key and so won't be sent.
    SHIFT_FLAG = 0x80
    ASCII_TO_KEYCODE = (
        b'\x00'    # NUL
        b'\x00'    # SOH
        b'\x00'    # STX
        b'\x00'    # ETX
        b'\x00'    # EOT
        b'\x00'    # ENQ
        b'\x00'    # ACK
        b'\x00'    # BEL \a
        b'\x2a'    # BS BACKSPACE \b (called DELETE in the usb.org document)
        b'\x2b'    # TAB \t
        b'\x28'    # LF \n (called Return or ENTER in the usb.org document)
        b'\x00'    # VT \v
        b'\x00'    # FF \f
        b'\x00'    # CR \r
        b'\x00'    # SO
        b'\x00'    # SI
        b'\x00'    # DLE
        b'\x00'    # DC1
        b'\x00'    # DC2
        b'\x00'    # DC3
        b'\x00'    # DC4
        b'\x00'    # NAK
        b'\x00'    # SYN
        b'\x00'    # ETB
        b'\x00'    # CAN
        b'\x00'    # EM
        b'\x00'    # SUB
        b'\x29'    # ESC
        b'\x00'    # FS
        b'\x00'    # GS
        b'\x00'    # RS
        b'\x00'    # US
        b'\x2c'    # SPACE
        b'\x9e'    # ! x1e|SHIFT_FLAG (shift 1)
        b'\xb4'    # " x34|SHIFT_FLAG (shift ')
        b'\xa0'    # # x20|SHIFT_FLAG (shift 3)
        b'\xa1'    # $ x21|SHIFT_FLAG (shift 4)
        b'\xa2'    # % x22|SHIFT_FLAG (shift 5)
        b'\xa4'    # & x24|SHIFT_FLAG (shift 7)
        b'\x34'    # '
        b'\xa6'    # ( x26|SHIFT_FLAG (shift 9)
        b'\xa7'    # ) x27|SHIFT_FLAG (shift 0)
        b'\xa5'    # * x25|SHIFT_FLAG (shift 8)
        b'\xae'    # + x2e|SHIFT_FLAG (shift =)
        b'\x36'    # ,
        b'\x2d'    # -
        b'\x37'    # .
        b'\x38'    # /
        b'\x27'    # 0
        b'\x1e'    # 1
        b'\x1f'    # 2
        b'\x20'    # 3
        b'\x21'    # 4
        b'\x22'    # 5
        b'\x23'    # 6
        b'\x24'    # 7
        b'\x25'    # 8
        b'\x26'    # 9
        b'\xb3'    # : x33|SHIFT_FLAG (shift ;)
        b'\x33'    # ;
        b'\xb6'    # < x36|SHIFT_FLAG (shift ,)
        b'\x2e'    # =
        b'\xb7'    # > x37|SHIFT_FLAG (shift .)
        b'\xb8'    # ? x38|SHIFT_FLAG (shift /)
        b'\x9f'    # @ x1f|SHIFT_FLAG (shift 2)
        b'\x84'    # A x04|SHIFT_FLAG (shift a)
        b'\x85'    # B x05|SHIFT_FLAG (etc.)
        b'\x86'    # C x06|SHIFT_FLAG
        b'\x87'    # D x07|SHIFT_FLAG
        b'\x88'    # E x08|SHIFT_FLAG
        b'\x89'    # F x09|SHIFT_FLAG
        b'\x8a'    # G x0a|SHIFT_FLAG
        b'\x8b'    # H x0b|SHIFT_FLAG
        b'\x8c'    # I x0c|SHIFT_FLAG
        b'\x8d'    # J x0d|SHIFT_FLAG
        b'\x8e'    # K x0e|SHIFT_FLAG
        b'\x8f'    # L x0f|SHIFT_FLAG
        b'\x90'    # M x10|SHIFT_FLAG
        b'\x91'    # N x11|SHIFT_FLAG
        b'\x92'    # O x12|SHIFT_FLAG
        b'\x93'    # P x13|SHIFT_FLAG
        b'\x94'    # Q x14|SHIFT_FLAG
        b'\x95'    # R x15|SHIFT_FLAG
        b'\x96'    # S x16|SHIFT_FLAG
        b'\x97'    # T x17|SHIFT_FLAG
        b'\x98'    # U x18|SHIFT_FLAG
        b'\x99'    # V x19|SHIFT_FLAG
        b'\x9a'    # W x1a|SHIFT_FLAG
        b'\x9b'    # X x1b|SHIFT_FLAG
        b'\x9c'    # Y x1c|SHIFT_FLAG
        b'\x9d'    # Z x1d|SHIFT_FLAG
        b'\x2f'    # [
        b'\x31'    # \ backslash
        b'\x30'    # ]
        b'\xa3'    # ^ x23|SHIFT_FLAG (shift 6)
        b'\xad'    # _ x2d|SHIFT_FLAG (shift -)
        b'\x35'    # `
        b'\x04'    # a
        b'\x05'    # b
        b'\x06'    # c
        b'\x07'    # d
        b'\x08'    # e
        b'\x09'    # f
        b'\x0a'    # g
        b'\x0b'    # h
        b'\x0c'    # i
        b'\x0d'    # j
        b'\x0e'    # k
        b'\x0f'    # l
        b'\x10'    # m
        b'\x11'    # n
        b'\x12'    # o
        b'\x13'    # p
        b'\x14'    # q
        b'\x15'    # r
        b'\x16'    # s
        b'\x17'    # t
        b'\x18'    # u
        b'\x19'    # v
        b'\x1a'    # w
        b'\x1b'    # x
        b'\x1c'    # y
        b'\x1d'    # z
        b'\xaf'    # { x2f|SHIFT_FLAG (shift [)
        b'\xb1'    # | x31|SHIFT_FLAG (shift \)
        b'\xb0'    # } x30|SHIFT_FLAG (shift ])
        b'\xb5'    # ~ x35|SHIFT_FLAG (shift `)
        b'\x4c'    # DEL DELETE (called Forward Delete in usb.org document)
    )

    # No more than _MAX_KEYPRESSES regular keys may be pressed at once.
    _MAX_KEYPRESSES = 6

    def __init__(self):
        """Create a Keyboard object that will send USB keyboard HID reports."""
        self.keyboard = None
        for device in usb_hid.devices:
            if device.usage_page is 0x1 and device.usage is 0x06:
                self.keyboard = device
                break
        if not self.keyboard:
            raise IOError("Could not find an HID keyboard device.")

        # Reuse this bytearray to send keyboard reports.
        self.report = bytearray(8)

        # report[0] modifiers
        # report[1] unused
        # report[2:8] regular key presses

        # View onto byte 0 in report.
        self.report_modifier = memoryview(self.report)[0:1]

        # List of regular keys currently pressed.
        # View onto bytes 2-7 in report.
        self.report_keys = memoryview(self.report)[2:]

    def press_keys(self, *keys):
        """Send a report indicating that the given keys have been pressed.

        Keys may be keycodes or strings of ASCII characters, which are translated into
        appropriate keycodes. The keycodes may be a modifier or regular keys.
        No more than six regular keys may be pressed simultaneously.

        Examples:
            # Press ctrl-x.
            kbd.press_keys(Keyboard.LEFT_CONTROL, 'x')

            # Or, more conveniently, use the CONTROL alias for LEFT_CONTROL:
            kbd.press_keys(Keyboard.CONTROL, 'x')

            # Press a, b, c keys all at once.
            kbd.press_keys('abc')
        """
        for item in keys:
            if isinstance(item, int):
                self._add_keycode_to_report(item)
            elif isinstance(item, str):
                for char in item:
                    keycode = self._char_to_keycode(char)
                    # If this is a shifted char, clear the SHIFT flag and press the SHIFT key.
                    if keycode & self.SHIFT_FLAG:
                        keycode &= ~self.SHIFT_FLAG
                        self._add_keycode_to_report(self.LEFT_SHIFT)
                    self._add_keycode_to_report(keycode)
            else:
                raise ValueError("Argument is not a keycode or a string")

            self.keyboard.send_report(self.report)

    def release_keys(self, *keys):
        """Send a USB HID report indicating that the given keys have been released.

        Each argument is either a keycode or a string of ASCII characters.
        For all the characters in a string, release the corresponding keycode.
        If a character requires a shift key, the LEFT_SHIFT key is also released.
        If a key that was not pressed is listed, it is ignored.

        Examples:
            # release keys LEFT_CONTROL, a, LEFT_SHIFT (implied by capital 'A'), and b.
            kbd.release_keys(keycodes.LEFT_CONTROL, 'Ab')

        """
        for item in keys:
            if isinstance(item, int):
                self._remove_keycode_from_report(item)
            elif isinstance(item, str):
                for char in item:
                    keycode = self._char_to_keycode(char)
                    # If this is a shifted char, clear the SHIFT flag and release the Shift key.
                    if keycode & self.SHIFT_FLAG:
                        keycode &= ~self.SHIFT_FLAG
                        self._remove_keycode_from_report(self.LEFT_SHIFT)
                    self._remove_keycode_from_report(keycode)
            else:
                raise ValueError("Argument is not a keycode or a string.")

            self.keyboard.send_report(self.report)

    def release_all(self):
        """Release all pressed keys."""
        for i in range(8):
            self.report[i] = 0
        self.keyboard.send_report(self.report)

    def type(self, *items):
        """Simulate typing. Send characters and collections of keycodes as separate keypresses.

        Examples:
            # Send "abcDEF" as a sequence of separate keypresses.
            kbd.type("abc", "DEF")

            # Press and release ctrl-B, then "h", then "i", then backspace.
            kbd.type((Keyboard.CONTROL, 'b'), "hi", Keyboard.BACKSPACE)
        """
        for item in items:
            if isinstance(item, str):
                # A string. Press and release each char in sequence.
                for char in item:
                    self.press_keys(char)
                    self.release_all()
            elif isinstance(item, int):
                # Press and release a single keycode
                self.press_keys(item)
                self.release_all()
            else:
                # Assume it's a collection of keycodes or chars.Press and release them all.
                self.press_keys(*item)
                self.release_all()

    def _char_to_keycode(self, char):
        """Return the HID keycode for the given ASCII character, with the SHIFT_FLAG possibly set.

        If the character requires pressing the Shift key, the SHIFT_FLAG bit is set.
        You must clear this bit before passing the keycode in a USB report."""
        char_val = ord(char)
        if char_val > 128:
            raise ValueError("Not an ASCII character.")
        keycode = self.ASCII_TO_KEYCODE[char_val]
        if keycode == 0:
            raise ValueError("No keycode available for character.")
        return keycode

    def _add_keycode_to_report(self, keycode):
        """Add a single keycode to the USB HID report."""
        #  Distinguish between modifiers and regular keycodes.
        if keycode >= 0xe0:
            # Turn on the bit for this modifier.
            self.report_modifier[0] |= 1 << (keycode - 0xe0)
        else:
            # Don't press twice.
            # (I'd like to use 'not in self.report_keys' here, but that's not implemented.)
            for i in range(const(self._MAX_KEYPRESSES)):
                if self.report_keys[i] == keycode:
                    # Already pressed.
                    return
            # Put keycode in first unused slot.
            for i in range(const(self._MAX_KEYPRESSES)):
                if self.report_keys[i] == 0:
                    self.report_keys[i] = keycode
                    return
            # All slots are filled.
            raise ValueError("Trying to press more than six keys at once.")

    def _remove_keycode_from_report(self, keycode):
        """Remove a single keycode from the report."""
        #  Distinguish between modifiers and regular keycodes.
        if keycode >= 0xe0:
            # Turn off the bit for this modifier.
            self.report_modifier[0] &= ~(1 << (keycode - 0xe0))
        elif keycode not in self.report_keys:
            # Check all the slots, just in case there's a duplicate. (There should not be.)
            for i in range(const(self._MAX_KEYPRESSES)):
                if self.report_keys[i] == keycode:
                    self.report_keys[i] = 0
