from .keycode import Keycode

# Verbatim copy from keyboard_layout_us, only rewritten the ASCII_TO_KEYCODE table to match the Dvorak keycodes.
class KeyboardLayoutUSDVO:
    """Map ASCII characters to appropriate keypresses on a standard US PC keyboard.
    Non-ASCII characters and most control characters will raise an exception.
    """

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
        b"\x00"  # NUL
        b"\x00"  # SOH
        b"\x00"  # STX
        b"\x00"  # ETX
        b"\x00"  # EOT
        b"\x00"  # ENQ
        b"\x00"  # ACK
        b"\x00"  # BEL \a
        b"\x2a"  # BS BACKSPACE \b (called DELETE in the usb.org document)
        b"\x2b"  # TAB \t
        b"\x28"  # LF \n (called Return or ENTER in the usb.org document)
        b"\x00"  # VT \v
        b"\x00"  # FF \f
        b"\x00"  # CR \r
        b"\x00"  # SO
        b"\x00"  # SI
        b"\x00"  # DLE
        b"\x00"  # DC1
        b"\x00"  # DC2
        b"\x00"  # DC3
        b"\x00"  # DC4
        b"\x00"  # NAK
        b"\x00"  # SYN
        b"\x00"  # ETB
        b"\x00"  # CAN
        b"\x00"  # EM
        b"\x00"  # SUB
        b"\x29"  # ESC
        b"\x00"  # FS
        b"\x00"  # GS
        b"\x00"  # RS
        b"\x00"  # US
        b"\x2c"  # SPACE
        b"\x9e"  # !
        b"\x94"  # "
        b"\xa0"  # #
        b"\xa1"  # $
        b"\xa2"  # %
        b"\xa4"  # &
        b"\x14"  # '
        b"\xa6"  # (
        b"\xa7"  # )
        b"\xa5"  # *
        b"\xb0"  # +
        b"\x1a"  # ,
        b"\x34"  # -
        b"\x08"  # .
        b"\x2f"  # /
        b"\x27"  # 0
        b"\x1e"  # 1
        b"\x1f"  # 2
        b"\x20"  # 3
        b"\x21"  # 4
        b"\x22"  # 5
        b"\x23"  # 6
        b"\x24"  # 7
        b"\x25"  # 8
        b"\x26"  # 9
        b"\x9d"  # :
        b"\x1d"  # ;
        b"\x9a"  # <
        b"\x30"  # =
        b"\x88"  # >
        b"\xaf"  # ?
        b"\x9f"  # @
        b"\x84"  # A
        b"\x91"  # B
        b"\x8c"  # C
        b"\x8b"  # D
        b"\x87"  # E
        b"\x9c"  # F
        b"\x98"  # G
        b"\x8d"  # H
        b"\x8a"  # I
        b"\x86"  # J
        b"\x99"  # K
        b"\x93"  # L
        b"\x90"  # M
        b"\x8f"  # N
        b"\x96"  # O
        b"\x95"  # P
        b"\x92"  # R
        b"\x9b"  # Q
        b"\xb3"  # S
        b"\x8e"  # T
        b"\x89"  # U
        b"\xb7"  # V
        b"\xb6"  # W
        b"\x85"  # X
        b"\x97"  # Y
        b"\xb8"  # Z
        b"\x2d"  # [
        b"\x31"  # \ backslash
        b"\x2e"  # ]
        b"\xa3"  # ^
        b"\xb4"  # _
        b"\x35"  # `
        b"\x04"  # a
        b"\x11"  # b
        b"\x0c"  # c
        b"\x0b"  # d
        b"\x07"  # e
        b"\x1c"  # f
        b"\x18"  # g
        b"\x0d"  # h
        b"\x0a"  # i
        b"\x06"  # j
        b"\x19"  # k
        b"\x13"  # l
        b"\x10"  # m
        b"\x0f"  # n
        b"\x16"  # o
        b"\x15"  # p
        b"\x1b"  # q
        b"\x12"  # r
        b"\x33"  # s
        b"\x0e"  # t
        b"\x09"  # u
        b"\x37"  # v
        b"\x36"  # w
        b"\x05"  # x
        b"\x17"  # y
        b"\x38"  # z
        b"\xad"  # {
        b"\xb1"  # |
        b"\xae"  # }
        b"\xb5"  # ~
        b"\x4c"  # DEL DELETE (called Forward Delete in usb.org document)
    )

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
            keycode('a')
            # Returns (Keycode.SHIFT, Keycode.A)
            keycode('A')
            # Raises ValueError because it's a accented e and is not ASCII
            keycode('é')
        """
        keycode = self._char_to_keycode(char)
        if keycode & self.SHIFT_FLAG:
            return (Keycode.SHIFT, keycode & ~self.SHIFT_FLAG)

        return (keycode,)

    def _char_to_keycode(self, char):
        """Return the HID keycode for the given ASCII character, with the SHIFT_FLAG possibly set.
        If the character requires pressing the Shift key, the SHIFT_FLAG bit is set.
        You must clear this bit before passing the keycode in a USB report.
        """
        char_val = ord(char)
        if char_val > 128:
            raise ValueError("Not an ASCII character.")
        keycode = self.ASCII_TO_KEYCODE[char_val]
        if keycode == 0:
            raise ValueError("No keycode available for character.")
        return keycode