import time
import usb.device
from usb.device.mouse import MouseInterface

eger = MouseInterface()
usb.device.get().init(eger, builtin_driver=True)

while not eger.is_open():
    time.sleep_ms(100)
    
time.sleep_ms(2000)
eger.move_by(100, 0)

time.sleep_ms(500)
eger.click_right(True)

time.sleep_ms(200)
eger.click_right(False)
