from machine import Pin
import machine
import time

clock = Pin(14, Pin.IN, Pin.PULL_UP)
data = Pin(15, Pin.IN, Pin.PULL_UP)

bit_sorszam = 0
allapot = "szinkron keresés"
szamlalo = 0
ir_index = 0
olvas_index = 0
ertek = 0
idle = False
tulcsordulas_db = 0
PUFFER_MERET = 4
puffer = [None] * PUFFER_MERET


'''
IRQ:
- CLOCK lefutó él történt
- DATA azonnali kiolvasása
- ha START-ra várunk → START ellenőrzés
- ha frame-et fogadunk → D0–D7 / parity / STOP
- sikeres frame → kész byte jelzése
'''

def clock_esemeny(pin):
    global ertek, bit_sorszam, allapot, idle, ir_index, szamlalo, tulcsordulas_db
    bit = data.value()
    if allapot == "start várás":
        if bit_sorszam == 0:
            if bit == 0:
                allapot = "frame fogadás"
                bit_sorszam += 1
            else:
                allapot = "szinkron keresés"
                idle = False
    elif allapot == "frame fogadás":
        if bit_sorszam > 0 and bit_sorszam < 9:
            ertek |= bit << (bit_sorszam - 1)
            if bit == 1:
                szamlalo += 1
            bit_sorszam += 1
        elif bit_sorszam == 9:
            if (szamlalo + bit) % 2 != 0:
                bit_sorszam += 1
            else:
                allapot = "szinkron keresés"
                bit_sorszam = 0
                szamlalo = 0
                ertek = 0
                idle = False
        elif bit_sorszam == 10:
            if bit == 1:
                allapot = "start várás"
                bit_sorszam = 0
                szamlalo = 0
                kovetkezo_ir_index = (ir_index + 1) % PUFFER_MERET
                if kovetkezo_ir_index != olvas_index:
                    puffer[ir_index] = ertek
                    ir_index = kovetkezo_ir_index
                else:
                    tulcsordulas_db += 1
                ertek=0
            else:
                allapot = "szinkron keresés"
                bit_sorszam = 0
                szamlalo = 0
                ertek = 0
                idle = False


clock.irq(
    trigger=Pin.IRQ_FALLING,
    handler=clock_esemeny
)

while True:
    byte = None
    aktualis_clock = clock.value()
    aktualis_data = data.value()
    if allapot == "szinkron keresés":
        if aktualis_clock == 1 and aktualis_data == 1 and not idle:
            kezdet = time.ticks_us()
            idle = True
        if idle:
            if aktualis_clock == 1 and aktualis_data == 1:
                most = time.ticks_us()
                eltelt = time.ticks_diff(most, kezdet)
                if eltelt >= 150:
                    allapot = "start várás"
                    idle = False
        if aktualis_clock == 0 or aktualis_data == 0:
            idle = False
    irq_allapot = machine.disable_irq()
    if ir_index != olvas_index:
        byte = puffer[olvas_index]
        olvas_index = (olvas_index + 1) % PUFFER_MERET
    tulcsordulas = tulcsordulas_db
    tulcsordulas_db = 0
    machine.enable_irq(irq_allapot)
    if byte is not None:
        print(byte)
    if tulcsordulas > 0:
        print(f"Puffer túlcsordulás {tulcsordulas} alkalommal")