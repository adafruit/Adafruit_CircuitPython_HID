import time
from adafruit_hid.mouse import Mouse
import board
import digitalio

# Sleep for a bit to avoid a race condition on some systems
# when creating a HID instance
time.sleep(1)

mouse = Mouse()

# define buttons. these can be any physical switches/buttons, but the values
# here work out-of-the-box with a CircuitPlayground Express' A and B buttons.
up = digitalio.DigitalInOut(board.D4)
up.direction = digitalio.Direction.INPUT
up.pull = digitalio.Pull.DOWN

down = digitalio.DigitalInOut(board.D5)
down.direction = digitalio.Direction.INPUT
down.pull = digitalio.Pull.DOWN

while True:
    # scroll up one unit (varies with host/OS)
    if up.value:
        mouse.move(wheel=1)

    # scroll down one unit (varies with host/OS)
    elif down.value:
        mouse.move(wheel=-1)

    time.sleep(0.1)
