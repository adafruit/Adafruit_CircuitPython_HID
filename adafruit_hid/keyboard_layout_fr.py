# SPDX-FileCopyrightText: 2022 Inemajo for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_hid.keyboard_layout_fr.KeyboardLayoutFR`
=======================================================

* Author(s): Inemajo
"""

from .keyboard_layout_base import KeyboardLayoutBase

SHIFT_FLAG = KeyboardLayoutBase.SHIFT_FLAG
CIRCUMFLEX_DEAD_KEY = 0x2f
TWODOTS_DEAD_KEY = CIRCUMFLEX_DEAD_KEY | SHIFT_FLAG


class KeyboardLayoutFR(KeyboardLayoutBase):
    """Map ASCII characters to appropriate keypresses on a standard FR PC keyboard.

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
        b"\x38"  # ! 0x38
        b"\x20"  # "
        b"\x20"  # # (NEED_ALTGR)
        b"\x30"  # $
        b"\xb4"  # % 0x31|SHIFT_FLAG
        b"\x1e"  # &
        b"\x21"  # '
        b"\x22"  # (
        b"\x2d"  # )
        b"\x32"  # *
        b"\xae"  # + 0x2e|SHIFT_FLAG (shift =)
        b"\x10"  # ,
        b"\x23"  # -
        b"\xb6"  # .
        b"\xb7"  # /
        b"\xa7"  # 0 0x27|SHIFT_FLAG
        b"\x9e"  # 1 0x1e|SHIFT_FLAG
        b"\x9f"  # 2 0x1f|SHIFT_FLAG
        b"\xa0"  # 3 0x20|SHIFT_FLAG
        b"\xa1"  # 4 0x21|SHIFT_FLAG
        b"\xa2"  # 5 0x22|SHIFT_FLAG
        b"\xa3"  # 6 0x23|SHIFT_FLAG
        b"\xa4"  # 7 0x24|SHIFT_FLAG
        b"\xa5"  # 8 0x25|SHIFT_FLAG
        b"\xa6"  # 9 0x26|SHIFT_FLAG
        b"\x37"  # :
        b"\x36"  # ;
        b"\x64"  # <
        b"\x2e"  # =
        b"\xe4"  # > x64|SHIFT_FLAG (shift <)
        b"\x90"  # ? x10|SHIFT_FLAG (shift /)
        b"\x27"  # @
        b"\x94"  # A x14|SHIFT_FLAG  (shift a)
        b"\x85"  # B x05|SHIFT_FLAG (etc.)
        b"\x86"  # C x06|SHIFT_FLAG
        b"\x87"  # D x07|SHIFT_FLAG
        b"\x88"  # E x08|SHIFT_FLAG
        b"\x89"  # F x09|SHIFT_FLAG
        b"\x8a"  # G x0a|SHIFT_FLAG
        b"\x8b"  # H x0b|SHIFT_FLAG
        b"\x8c"  # I x0c|SHIFT_FLAG
        b"\x8d"  # J x0d|SHIFT_FLAG
        b"\x8e"  # K x0e|SHIFT_FLAG
        b"\x8f"  # L x0f|SHIFT_FLAG
        b"\xb3"  # M x10|SHIFT_FLAG
        b"\x91"  # N x11|SHIFT_FLAG
        b"\x92"  # O x12|SHIFT_FLAG
        b"\x93"  # P x13|SHIFT_FLAG
        b"\x84"  # Q x04|SHIFT_FLAG
        b"\x95"  # R x15|SHIFT_FLAG
        b"\x96"  # S x16|SHIFT_FLAG
        b"\x97"  # T x17|SHIFT_FLAG
        b"\x98"  # U x18|SHIFT_FLAG
        b"\x99"  # V x19|SHIFT_FLAG
        b"\x9d"  # W x1d|SHIFT_FLAG
        b"\x9b"  # X x1b|SHIFT_FLAG
        b"\x9c"  # Y x1c|SHIFT_FLAG
        b"\x9a"  # Z x1a|SHIFT_FLAG
        b"\x22"  # [ (NEED_ALTGR)
        b"\x25"  # \ (NEED_ALTGR)
        b"\x2d"  # ] (NEED_ALTGR)
        b"\x26"  # ^
        b"\x25"  # _
        b"\x24"  # ` (NEED_ALTGR)
        b"\x14"  # a
        b"\x05"  # b
        b"\x06"  # c
        b"\x07"  # d
        b"\x08"  # e
        b"\x09"  # f
        b"\x0a"  # g
        b"\x0b"  # h
        b"\x0c"  # i
        b"\x0d"  # j
        b"\x0e"  # k
        b"\x0f"  # l
        b"\x33"  # m
        b"\x11"  # n
        b"\x12"  # o
        b"\x13"  # p
        b"\x04"  # q
        b"\x15"  # r
        b"\x16"  # s
        b"\x17"  # t
        b"\x18"  # u
        b"\x19"  # v
        b"\x1d"  # w
        b"\x1b"  # x
        b"\x1c"  # y
        b"\x1a"  # z
        b"\x21"  # { (NEED_ALTGR)
        b"\x23"  # | (NEED_ALTGR)
        b"\x2e"  # } (NEED_ALTGR)
        b"\x1f"  # ~
        b"\x4c"  # DEL DELETE (called Forward Delete in usb.org document)
    )

    NEED_ALTGR = "~#{[|`\\^@]}€"

    HIGHER_ASCII = {
        233: 0x1f,  # é
        231: 0x26,  # ç
        232: 0x24,  # è
        224: 0x27,  # à
        8364: 0x38,  # €

        249: 0x34, # ù
        176: 0x2d | SHIFT_FLAG, # °
        167: 0x38 | SHIFT_FLAG,  # §
        181: 0x31 | SHIFT_FLAG,  # µ
    }

    SEVERAL_KEYCODE = {
        234: (CIRCUMFLEX_DEAD_KEY, 0x08),  # ê
        202: (CIRCUMFLEX_DEAD_KEY, 0x08 | SHIFT_FLAG), # Ê
        235: (TWODOTS_DEAD_KEY, 0x08), # ë
        203: (TWODOTS_DEAD_KEY, 0x08 | SHIFT_FLAG), # Ë

        226: (CIRCUMFLEX_DEAD_KEY, 0x14), # â
        194: (CIRCUMFLEX_DEAD_KEY, 0x14 | SHIFT_FLAG), # Â
        228: (TWODOTS_DEAD_KEY, 0x14), # ä
        196: (TWODOTS_DEAD_KEY, 0x14 | SHIFT_FLAG), # Ä

        244: (CIRCUMFLEX_DEAD_KEY, 0x12), # ô
        212: (CIRCUMFLEX_DEAD_KEY, 0x12 | SHIFT_FLAG), # Ô
        246: (TWODOTS_DEAD_KEY, 0x12), # ö
        214: (TWODOTS_DEAD_KEY, 0x12 | SHIFT_FLAG), # Ö
    }


KeyboardLayout = KeyboardLayoutFR
