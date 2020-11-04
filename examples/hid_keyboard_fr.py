from time import sleep
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_fr import KeyboardLayoutFR

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutFR(keyboard)  # Nous sommes en france :)

#You must have twitter open and the browser windows focus
def send_tweet(tweet):
    keyboard_layout.write("n")
    sleep(0.1)
    keyboard_layout.write(tweet)
    sleep(0.1)
    keyboard.press(Keycode.LEFT_CONTROL)
    keyboard.press(Keycode.ENTER)
    keyboard.release_all()

#Test the layout (CIRCUMFLEX not available for now... :( )
def layout_test():
    keyboard_layout.write("àçèéù€°!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~~")

sleep(5)
#send_tweet("hé Salut le monde! @circuitpython")
#layout_test()

#
#àçèéù€°!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_àbcdefghijklmnopqrstuvwxyz{|}~~







