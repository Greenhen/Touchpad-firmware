
import time

teszt_frame = [ 0,1,1,0,1,0,0,1,0,1,1]
teszt_frame_2 = [0,0,0,1,0,1,0,0,0,1,1]

bit_sorszam = 0
allapot = "start várás"
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


def bit_feldolgozas(bit):
    global ertek, bit_sorszam, allapot, idle, ir_index, szamlalo, tulcsordulas_db,start_hiba_db,parity_hiba_db,stop_hiba_db
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
                
                
for i in range(7):
    for bit in teszt_frame:
        bit_feldolgozas(bit)
    #allapot="start várás"
    for bit in teszt_frame_2:
        bit_feldolgozas(bit)
    #allapot="start várás"
def pufferbol_olvas():
    global olvas_index
    if ir_index==olvas_index:
        return
    else:
        byte = puffer[olvas_index]
        puffer[olvas_index] = None 
        olvas_index = (olvas_index + 1) % PUFFER_MERET
        return byte
    
def puffer_feldolgozas():
    for i in range(MAX_OLVASAS):
        byte=pufferbol_olvas()
        if byte is None:
            break
        print(f"bit érték: {byte}")
    
puffer_feldolgozas()    
for i in range(2):
    for bit in teszt_frame:
        bit_feldolgozas(bit)
    allapot="start várás"
    for bit in teszt_frame_2:
        bit_feldolgozas(bit)
    allapot="start várás"

print(f"olvas index: {olvas_index}")
print(f"ír index: {ir_index}")
print(f"érték: {ertek}")
print(f"start hiba: {start_hiba_db}")
print(f"parity hiba: {parity_hiba_db}")
print(f"stop hiba: {stop_hiba_db}")
print(f"puffer: {puffer}")
print(f"túlcsordulás: {tulcsordulas_db}")
