# Use Joy FeatherWing to drive Gamepad.

import time

import board
import busio
from micropython import const
import adafruit_seesaw
from adafruit_hid.gamepad import Gamepad

def range_map(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

BUTTON_RIGHT = const(6)
BUTTON_DOWN = const(7)
BUTTON_LEFT = const(9)
BUTTON_UP = const(10)
BUTTON_SEL = const(14)
button_mask = const((1 << BUTTON_RIGHT) |
                    (1 << BUTTON_DOWN) |
                    (1 << BUTTON_LEFT) |
                    (1 << BUTTON_UP) |
                    (1 << BUTTON_SEL))

i2c = busio.I2C(board.SCL, board.SDA)

ss = adafruit_seesaw.Seesaw(i2c)

ss.pin_mode_bulk(button_mask, ss.INPUT_PULLUP)

last_game_x = 0
last_game_y = 0

g = Gamepad()

while True:
    x = ss.analog_read(2)
    y = ss.analog_read(3)

    game_x = range_map(x, 0, 1023, -127, 127)
    game_y = range_map(y, 0, 1023, -127, 127)
    if last_game_x != game_x or last_game_y != game_y:
        last_game_x = game_x
        last_game_y = game_y
        print(game_x, game_y)
        g.move_joysticks(x=game_x, y=game_y)

    buttons = (BUTTON_RIGHT, BUTTON_DOWN, BUTTON_LEFT, BUTTON_UP, BUTTON_SEL)
    button_state = [False] * len(buttons)
    for i, button in enumerate(buttons):
        buttons = ss.digital_read_bulk(button_mask)
        if not (buttons & (1 << button) and not button_state[i]):
            g.press_buttons(i+1)
            print("Press", i+1)
            button_state[i] = True
        elif button_state[i]:
            g.release_buttons(i+1)
            print("Release", i+1)
            button_state[i] = False

    time.sleep(.01)
