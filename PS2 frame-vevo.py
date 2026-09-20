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
start_hiba_db = 0
parity_hiba_db = 0
stop_hiba_db = 0
PUFFER_MERET = 16
MAX_OLVASAS = 4
puffer = [None] * PUFFER_MERET
aktualis_csomag = []


'''
IRQ:
- CLOCK lefutó él történt
- DATA azonnali kiolvasása
- ha START-ra várunk → START ellenőrzés
- ha frame-et fogadunk → D0–D7 / parity / STOP
- sikeres frame → kész byte jelzése
'''

def clock_esemeny(pin):
    global ertek, bit_sorszam, allapot, idle, ir_index, szamlalo, tulcsordulas_db,start_hiba_db,parity_hiba_db,stop_hiba_db
    bit = data.value()
    if allapot == "start várás":
        if bit_sorszam == 0:
            if bit == 0:
                allapot = "frame fogadás"
                bit_sorszam += 1
            else:
                allapot = "szinkron keresés"
                start_hiba_db += 1
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
                parity_hiba_db += 1
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
                stop_hiba_db += 1
                idle = False

def allapotbyte_ervenyes(byte):
    ervenyes = (byte & (1 << 3)) != 0
    return ervenyes

def gombok_kiolvasasa(csomag):
    allapot_byte = csomag[0]

    bal_gomb = (allapot_byte & (1 << 0)) != 0
    jobb_gomb = (allapot_byte & (1 << 1)) != 0
    kozepso_gomb = (allapot_byte & (1 << 2)) != 0

    return bal_gomb, jobb_gomb, kozepso_gomb

def tulcsordulas(byte):
    x_tulcsordulas = (byte & (1 << 6)) != 0
    y_tulcsordulas = (byte & (1 << 7)) != 0

    return x_tulcsordulas, y_tulcsordulas

def elojelesse_alakit(byte, negativ):
    if negativ:
        byte = byte - 256

    return byte

def mozgas_kiolvasasa(csomag):
    allapot_byte = csomag[0]

    x_tulcsordulas, y_tulcsordulas = tulcsordulas(allapot_byte)

    if x_tulcsordulas or y_tulcsordulas:
        return None, None

    x_negativ = (allapot_byte & (1 << 4)) != 0
    y_negativ = (allapot_byte & (1 << 5)) != 0

    x = elojelesse_alakit(csomag[1], x_negativ)
    y = elojelesse_alakit(csomag[2], y_negativ)

    return x, y

def csomag_feldolgozas(csomag):
    bal_gomb, jobb_gomb, kozepso_gomb = gombok_kiolvasasa(csomag)
    x, y = mozgas_kiolvasasa(csomag)

    return bal_gomb, jobb_gomb, kozepso_gomb, x, y

def byte_feldolgozas(byte):
    global aktualis_csomag

    if len(aktualis_csomag) == 0:
        if not allapotbyte_ervenyes(byte):
            return None

    aktualis_csomag.append(byte)

    if len(aktualis_csomag) == 3:
        kesz_csomag = aktualis_csomag
        aktualis_csomag = []
        return kesz_csomag

    return None

def pufferbol_olvas():
    global olvas_index
    irq_allapot = machine.disable_irq()
    byte = None
    if ir_index!=olvas_index:    
        byte = puffer[olvas_index]
        puffer[olvas_index] = None 
        olvas_index = (olvas_index + 1) % PUFFER_MERET
    machine.enable_irq(irq_allapot)
    return byte
    
def puffer_feldolgozas():
    for i in range(MAX_OLVASAS):
        byte=pufferbol_olvas()
        if byte is None:
            break
        kesz_csomag = byte_feldolgozas(byte)
        if kesz_csomag is not None:
            print(csomag_feldolgozas(kesz_csomag))


clock.irq(
    trigger=Pin.IRQ_FALLING,
    handler=clock_esemeny
)

while True:
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
        
    puffer_feldolgozas()
    
        
    irq_allapot = machine.disable_irq()
    
    start_hibak = start_hiba_db
    parity_hibak = parity_hiba_db
    stop_hibak = stop_hiba_db
    tulcsordulas = tulcsordulas_db
    start_hiba_db = 0
    parity_hiba_db = 0
    stop_hiba_db = 0
    tulcsordulas_db = 0

    machine.enable_irq(irq_allapot)
        
    if start_hibak > 0:
        print(f"START hiba: {start_hibak}")

    if parity_hibak > 0:
        print(f"Parity hiba: {parity_hibak}")

    if stop_hibak > 0:
        print(f"STOP hiba: {stop_hibak}")

    if tulcsordulas > 0:
        print(f"Puffer túlcsordulás: {tulcsordulas}")
