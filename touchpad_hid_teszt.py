import time
import usb.device
from usb.device.mouse import MouseInterface
import touchpad_ps2

elozo_bal_gomb = False
elozo_jobb_gomb = False
elozo_kozepso_gomb = False

eger = MouseInterface()
usb.device.get().init(eger, builtin_driver=True)

while not eger.is_open():
    time.sleep_ms(100)

def touchpad_eredmeny_kuldes(eger, eredmeny):
    global elozo_bal_gomb, elozo_jobb_gomb, elozo_kozepso_gomb
    
    bal_gomb, jobb_gomb, kozepso_gomb, x, y = eredmeny
    
    if elozo_bal_gomb != bal_gomb:
        eger.click_left(bal_gomb)
        elozo_bal_gomb = bal_gomb
    if elozo_jobb_gomb != jobb_gomb:
        eger.click_right(jobb_gomb)
        elozo_jobb_gomb = jobb_gomb
    if elozo_kozepso_gomb != kozepso_gomb:
        eger.click_middle(kozepso_gomb)
        elozo_kozepso_gomb = kozepso_gomb
    if x is not None and y is not None:
        x = max(-127, min(x, 127))
        y = max(-127, min(y, 127))
        eger.move_by(x, y)


while True:
    eredmenyek = touchpad_ps2.touchpad_frissites()
    for eredmeny in eredmenyek:
        touchpad_eredmeny_kuldes(eger, eredmeny)

        
        
    