# ============================================================
# BITKEZELÉS - TANULÁSI JEGYZET
# ============================================================

# ------------------------------------------------------------
# 1. BIT ÉS BYTE
# ------------------------------------------------------------

# A bit két értéket vehet fel:
#
# 0
# 1
#
# 8 bit = 1 byte
#
# Példa:
#
# 10110010
#
# A bináris számrendszer helyiértékei jobbról balra:
#
# bit:       7   6   5   4   3   2   1   0
# érték:    128  64  32  16   8   4   2   1
#
# Például:
#
# 10110010
#
# = 128 + 32 + 16 + 2
# = 178


# ------------------------------------------------------------
# 2. BINÁRIS SZÁMOK PYTHONBAN
# ------------------------------------------------------------

# Pythonban a 0b előtag jelzi, hogy bináris számot írunk.

adat = 0b10110010

print(adat)

# Eredmény:
# 178
#
# Fontos:
# A 0b nem része magának a bináris számnak.
#
# 0b101 = binárisan 101 = decimálisan 5


# ------------------------------------------------------------
# 3. BIT SORSZÁMOZÁSA
# ------------------------------------------------------------

# A biteket JOBBRÓL BALRA számozzuk, 0-tól:
#
# 0 0 1 0 0 0 0 0
#     ^
#    bit5
#
# bit0 =   1
# bit1 =   2
# bit2 =   4
# bit3 =   8
# bit4 =  16
# bit5 =  32
# bit6 =  64
# bit7 = 128


# ------------------------------------------------------------
# 4. BALRA TOLÁS: <<
# ------------------------------------------------------------

# A << operátor balra tolja a biteket.

ertek = 1 << 3

print(ertek)

# Gondolatban:
#
# 00000001
#       << 3
# 00001000
#
# Ez decimálisan 8.


# Pozitív egész számnál egy hellyel balra tolás
# az értéket kétszerezi.

print(5 << 1)

# 5 = 00000101
#
# 00000101 << 1
# 00001010
#
# Eredmény: 10


# Két hellyel:

print(3 << 2)

# 3 = 00000011
#
# 00000011 << 2
# 00001100
#
# Eredmény: 12


# ------------------------------------------------------------
# 5. JOBBRA TOLÁS: >>
# ------------------------------------------------------------

# A >> operátor jobbra tolja a biteket.

print(8 >> 1)

# 8 = 00001000
#
# 00001000 >> 1
# 00000100
#
# Eredmény: 4


print(5 >> 1)

# 5 = 00000101
#
# 00000101 >> 1
# 00000010
#
# Eredmény: 2
#
# A jobb szélen kieső bit elveszik.


print(13 >> 2)

# 13 = 00001101
#
# 00001101 >> 2
# 00000011
#
# Eredmény: 3


# ------------------------------------------------------------
# 6. BITENKÉNTI VAGY: |
# ------------------------------------------------------------

# A | a bitenkénti VAGY (OR) operátor.
#
# Szabály:
#
# 0 | 0 = 0
# 0 | 1 = 1
# 1 | 0 = 1
# 1 | 1 = 1
#
# Ha legalább az egyik bit 1, az eredmény 1.


a = 0b00000110
b = 0b00100000

eredmeny = a | b

print(eredmeny)

# Binárisan:
#
#   00000110
# | 00100000
# -----------
#   00100110
#
# A VAGY azért hasznos, mert egy új 1 bitet
# hozzá tudunk adni úgy, hogy a már meglévő
# 1 biteket nem töröljük.


# ------------------------------------------------------------
# 7. BITENKÉNTI ÉS: &
# ------------------------------------------------------------

# A & a bitenkénti ÉS (AND) operátor.
#
# Szabály:
#
# 0 & 0 = 0
# 0 & 1 = 0
# 1 & 0 = 0
# 1 & 1 = 1
#
# Csak akkor lesz 1 az eredmény,
# ha MINDKÉT bit 1.


adat = 0b10110110
maszk = 0b00000100

eredmeny = adat & maszk

print(eredmeny)

# Binárisan:
#
#   10110110
# & 00000100
# -----------
#   00000100
#
# Ez azt mutatja, hogy a bit2 értéke 1.


# ------------------------------------------------------------
# 8. BITMASZK KÉSZÍTÉSE
# ------------------------------------------------------------

# Nem kell kézzel ilyeneket írnunk:
#
# 00100000
#
# A megfelelő maszkot előállíthatjuk eltolással.

bit_sorszama = 5

maszk = 1 << bit_sorszama

print(maszk)

# 00000001 << 5
#
# =
#
# 00100000
#
# decimálisan 32


# ------------------------------------------------------------
# 9. EGY BIT ELLENŐRZÉSE
# ------------------------------------------------------------

adat = 0b10110110
bit_sorszama = 5

maszk = 1 << bit_sorszama

if adat & maszk:
    print("A bit 1")
else:
    print("A bit 0")


# Miért működik?
#
# Pythonban:
#
# 0           -> False
# nem nulla   -> True
#
# Tehát ha az AND eredménye például:
#
# 00100000
#
# az decimálisan 32, ami nem nulla, ezért True.
#
# Ha az eredmény:
#
# 00000000
#
# akkor 0, tehát False.


# ------------------------------------------------------------
# 10. ÚJ BIT ELHELYEZÉSE EGY MEGADOTT HELYEN
# ------------------------------------------------------------

ertek = 0b00000110

bit = 1
bit_sorszam = 5

ertek = ertek | (bit << bit_sorszam)

print(ertek)

# Lépések:
#
# bit:
#
# 00000001
#
# Először a megfelelő helyre toljuk:
#
# 00000001 << 5
#
# =
#
# 00100000
#
# Majd VAGY művelettel hozzáadjuk:
#
#   00000110
# | 00100000
# -----------
#   00100110


# Ugyanez rövidebben:

ertek = 0b00000110
bit = 1
bit_sorszam = 5

ertek |= bit << bit_sorszam

print(ertek)

# A |= rövidítés:
#
# ertek |= valami
#
# ugyanaz, mint:
#
# ertek = ertek | valami


# ------------------------------------------------------------
# 11. MI TÖRTÉNIK, HA AZ ÚJ BIT 0?
# ------------------------------------------------------------

ertek = 0b00000110

bit = 0
bit_sorszam = 4

ertek |= bit << bit_sorszam

print(ertek)

# A 0 eltolva is 0:
#
# 00000000 << 4
#
# =
#
# 00000000
#
# Ezután:
#
#   00000110
# | 00000000
# -----------
#   00000110
#
# Tehát a meglévő érték nem változik.


# ------------------------------------------------------------
# 12. TÖBB BIT ÖSSZERAKÁSA - MSB FIRST PÉLDA
# ------------------------------------------------------------

# Ezt tanulási példaként használtuk:
#
# Ha a legnagyobb helyiértékű bit érkezne először,
# minden új bit előtt balra tolhatnánk az eddigi értéket.

bitek = [1, 0, 1, 1]

ertek = 0

for bit in bitek:
    ertek <<= 1
    ertek |= bit

print(ertek)

# Lépések:
#
# 1        -> 1
# 1,0      -> 10
# 1,0,1    -> 101
# 1,0,1,1  -> 1011
#
# 1011 binárisan = 11
#
# FONTOS:
# A PS/2 adatbitek NEM ebben a sorrendben érkeznek.
# Ez csak a bitműveletek megértéséhez volt példa.


# ------------------------------------------------------------
# 13. LSB FIRST
# ------------------------------------------------------------

# PS/2-ben a 8 adatbit LSB FIRST sorrendben érkezik.
#
# Ez azt jelenti:
#
# D0 érkezik először,
# majd D1,
# majd D2,
# ...
# végül D7.
#
# Például:
#
# A kész byte:
#
# 10110010
#
# Normál leírásban:
#
# D7 D6 D5 D4 D3 D2 D1 D0
#  1  0  1  1  0  0  1  0
#
# PS/2-n viszont ebben a sorrendben érkezik:
#
# D0 D1 D2 D3 D4 D5 D6 D7
#  0  1  0  0  1  1  0  1


# ------------------------------------------------------------
# 14. LSB FIRST BITEK ÖSSZERAKÁSA
# ------------------------------------------------------------

bitek = [0, 1, 0, 0, 1, 1, 0, 1]

ertek = 0

for bit_sorszam, bit in enumerate(bitek):
    ertek = ertek | (bit << bit_sorszam)

print(ertek)

# Rövidebben:
#
# ertek |= bit << bit_sorszam
#
# Az enumerate() itt egyszerre adja:
#
# bit_sorszam -> 0, 1, 2, 3, ...
# bit         -> az adott helyen lévő 0 vagy 1
#
#
# A végeredmény:
#
# 10110010
#
# =
#
# 128 + 32 + 16 + 2
#
# =
#
# 178


# ------------------------------------------------------------
# 15. PS/2 - DATA ÉS CLOCK
# ------------------------------------------------------------

# A PS/2 kommunikációban két fontos jelvezetékünk van:
#
# DATA  -> MIT olvasunk (0 vagy 1)
# CLOCK -> MIKOR olvassuk
#
# A CLOCK HIGH és LOW között váltakozik.
#
# Rising edge / felfutó él:
#
# 0 -> 1
#
# Falling edge / lefutó él:
#
# 1 -> 0
#
# A tanulási példánkban a Pico a CLOCK
# lefutó élét figyeli.


# Egyszerű polling elv:

elozo_clock = 1

# Valódi programban ez egy while True ciklusban történne:
#
# aktualis_clock = clock.value()
#
# if elozo_clock == 1 and aktualis_clock == 0:
#     bit = data.value()
#
# elozo_clock = aktualis_clock
#
#
# Vagyis:
#
# CLOCK 1 -> 0
#       ↓
# lefutó él
#       ↓
# DATA vezeték kiolvasása
#       ↓
# kapunk egy bitet


# ------------------------------------------------------------
# 16. PS/2 KERET
# ------------------------------------------------------------

# Egy PS/2 keret összesen 11 bitből áll:
#
# START | 8 DATA bit | PARITY | STOP
#
# Pontosabban:
#
# START | D0 D1 D2 D3 D4 D5 D6 D7 | PARITY | STOP
#
#   0   |        hasznos adat       | ellenőrzés | 1
#
#
# START:
# - értéke mindig 0
# - jelzi az új keret kezdetét
# - nem része a hasznos 8 bites adatnak
#
#
# D0-D7:
# - ez a 8 hasznos adatbit
# - PS/2-ben D0 érkezik először
#
#
# PARITY:
# - egyszerű hibaészlelés
# - nem része a hasznos adatnak
#
#
# STOP:
# - értéke mindig 1
# - jelzi a keret végét
# - nem része a hasznos adatnak


# ------------------------------------------------------------
# 17. PS/2 PARITY - PÁRATLAN PARITÁS
# ------------------------------------------------------------

# A PS/2 ODD PARITY-t, vagyis páratlan paritást használ.
#
# A szabály:
#
# A 8 DATA bit + PARITY bit között az 1-ek
# száma összesen páratlan legyen.
#
#
# Példa:
#
# adat:
#
# 00000111
#
# Ebben 3 db 1 van.
# 3 már páratlan.
#
# Ezért:
#
# PARITY = 0
#
#
# Másik példa:
#
# 00000101
#
# Ebben 2 db 1 van.
# 2 páros.
#
# Ezért:
#
# PARITY = 1
#
# Így összesen 3 db 1 lesz.


# A korábbi 178-as példánk:

# 10110010
#
# Ebben 4 db 1 van.
#
# Ezért:
#
# PARITY = 1
#
# Így:
#
# 4 + 1 = 5
#
# ami páratlan.


# ------------------------------------------------------------
# 18. MIRE JÓ A PARITY?
# ------------------------------------------------------------

# Tegyük fel, hogy ezt küldték:
#
# 10110010
#
# parity = 1
#
# Az adatban 4 db 1 van.
# A parity-vel együtt 5.
#
# Ez szabályos.


# Ha egy bit hibásan megváltozik:
#
# küldött:
#
# 10110010
#
# fogadott:
#
# 10110011
#
# A fogadott adatban már 5 db 1 van.
#
# A parity továbbra is 1:
#
# 5 + 1 = 6
#
# A 6 páros.
#
# A Pico tudja, hogy valamilyen átviteli hiba történt.


# FONTOS:
#
# A parity nem garantálja, hogy minden adat hibátlan.
#
# Egyetlen bit megváltozását észreveszi,
# de például két bit egyidejű megváltozását
# nem feltétlenül.
#
# Ez tehát egyszerű HIBADETEKTÁLÁS.


# ------------------------------------------------------------
# 19. A PS/2 KERET POZÍCIÓINAK KÖVETÉSE
# ------------------------------------------------------------

# Minden CLOCK lefutó élnél egy új bitet olvasunk.
#
# Egy számlálóval nyomon követhetjük,
# hogy a keret melyik részénél járunk.
#
# bit_sorszam:
#
#  0 -> START
#  1 -> D0
#  2 -> D1
#  3 -> D2
#  4 -> D3
#  5 -> D4
#  6 -> D5
#  7 -> D6
#  8 -> D7
#  9 -> PARITY
# 10 -> STOP


# Például a START bit ellenőrzése:

bit_sorszam = 0
bit = 0

if bit_sorszam == 0:
    if bit == 0:
        print("Érvényes START")


# ------------------------------------------------------------
# 20. FONTOS KÜLÖNBSÉG: KERETPOZÍCIÓ ÉS ADATBIT
# ------------------------------------------------------------

# A bit_sorszam jelenleg a TELJES PS/2 keretben
# elfoglalt helyet jelenti.
#
# Emiatt például:
#
# bit_sorszam = 6
#
# nem D6-ot jelent, hanem D5-öt:
#
# 0 -> START
# 1 -> D0
# 2 -> D1
# 3 -> D2
# 4 -> D3
# 5 -> D4
# 6 -> D5
#
# Ennek oka, hogy a START bit elfoglalja
# a keret 0. pozícióját.


# ============================================================
# EDDIGI ÖSSZEFOGLALÁS
# ============================================================

# Eddig tudjuk:
#
# - mi a bit
# - mi a byte
# - hogyan működik a bináris számrendszer
# - hogyan számozzuk a biteket
# - 0b bináris literál
#
# Bitműveletek:
#
# <<  balra tolás
# >>  jobbra tolás
# |   bitenkénti VAGY
# &   bitenkénti ÉS
#
# Tudunk:
#
# - bitmaszkot készíteni
# - egy adott bitet ellenőrizni
# - egy bitet adott pozícióra tenni
# - több bitből számot felépíteni
# - LSB-first adatot összerakni
#
# PS/2-ből eddig tudjuk:
#
# DATA  = mit olvasunk
# CLOCK = mikor olvasunk
#
# és a keret:
#
# START | D0 D1 D2 D3 D4 D5 D6 D7 | PARITY | STOP
#
# START = 0
# STOP  = 1
#
# D0-D7 = hasznos 8 bites adat
#
# PS/2 = LSB first
#
# PARITY = páratlan paritású egyszerű hibaellenőrzés
#
# Következő lépés:
#
# Megtanulni programból külön kezelni:
#
# START
# DATA
# PARITY
# STOP
#
# attól függően, hogy a 11 bites keret
# melyik pozíciójánál tartunk.