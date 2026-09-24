import time
import usb.device
from usb.device.keyboard import KeyboardInterface
from usb.device.mouse import MouseInterface

kbd = KeyboardInterface()

eger = MouseInterface()

usb.device.get().init(eger, kbd, builtin_driver=True)

while not kbd.is_open() or not eger.is_open():
    time.sleep(0.1)

time.sleep(3)

eger.move_by(0,50)

kbd.send_keys([0x04])
kbd.send_keys([])

