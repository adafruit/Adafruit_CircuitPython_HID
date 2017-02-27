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
"""
:mod:`adafruit_hid.keyboard`
====================================================

USB keyboard related constants.

* Author(s): Scott Shawcroft
"""

# Usage codes from here: http://www.usb.org/developers/hidpage/Hut1_12v2.pdf

A = 0x04
"""``a``"""
B = 0x05
"""``b``"""
C = 0x06
"""``c``"""
D = 0x07
"""``d``"""
E = 0x08
"""``e``"""
F = 0x09
"""``f``"""
G = 0x0A
"""``g``"""
H = 0x0B
"""``h``"""
I = 0x0C
"""``i``"""
J = 0x0D
"""``j``"""
K = 0x0E
"""``k``"""
L = 0x0F
"""``l``"""
M = 0x10
"""``m``"""
N = 0x11
"""``n``"""
O = 0x12
"""``o``"""
P = 0x13
"""``p``"""
Q = 0x14
"""``q``"""
R = 0x15
"""``r``"""
S = 0x16
"""``s``"""
T = 0x17
"""``t``"""
U = 0x18
"""``u``"""
V = 0x19
"""``v``"""
W = 0x1A
"""``w``"""
X = 0x1B
"""``x``"""
Y = 0x1C
"""``y``"""
Z = 0x1D
"""``z``"""
ONE = 0x1E
"""``1``"""
TWO = 0x1F
"""``2``"""
THREE = 0x20
"""``3``"""
FOUR = 0x21
"""``4``"""
FIVE = 0x22
"""``5``"""
SIX = 0x23
"""``6``"""
SEVEN = 0x24
"""``7``"""
EIGHT = 0x25
"""``8``"""
NINE = 0x26
"""``9``"""
ZERO = 0x27
"""``0``"""
RETURN = 0x28
"""Moves the cursor to the next line. Also known as enter."""
ESCAPE = 0x29
"""Escape."""
BACKSPACE = 0x2A
"""Deletes a character to the left of the cursor."""
TAB = 0x2B
"""A tab character. It is whitespace."""
SPACEBAR = 0x2C
"""`` ``"""
MINUS = 0x2D
"""``-``"""
EQUALS = 0x2E
"""``=``"""
LEFT_BRACKET = 0x2F
"""``[``"""
RIGHT_BRACKET = 0x30
"""``]``"""
BACKSLASH = 0x31
"""``\``"""
POUND = 0x32
"""``#``"""
SEMICOLON = 0x33
"""``;``"""
QUOTE = 0x34
"""``'``"""
GRAVE_ACCENT = 0x35
r""":literal:`\``"""
COMMA = 0x36
"""``,``"""
PERIOD = 0x37
"""``.``"""
FORWARD_SLASH = 0x38
"""``/``"""

DELETE = 0x4C
"""Deletes a character to the right of the cursor."""

RIGHT_ARROW = 0x4F
"""Moves the cursor right."""
LEFT_ARROW = 0x50
"""Moves the cursor left."""
DOWN_ARROW = 0x51
"""Moves the cursor down."""
UP_ARROW = 0x52
"""Moves the cursor up."""

LEFT_CONTROL = 0xE0
"""Control modifier left of the spacebar."""
LEFT_SHIFT = 0xE1
"""Shift modifier left of the spacebar."""
LEFT_ALT = 0xE2
"""Alt modifier left of the spacebar."""
LEFT_GUI = 0xE3
"""GUI modifier (aka Windows key, Option or Meta) left of the spacebar."""
RIGHT_CONTROL = 0xE4
"""Control modifier right of the spacebar."""
RIGHT_SHIFT = 0xE5
"""Shift modifier right of the spacebar."""
RIGHT_ALT = 0xE6
"""Alt modifier right of the spacebar."""
RIGHT_GUI = 0xE7
"""GUI modifier (aka Windows key, Option or Meta) right of the spacebar."""
