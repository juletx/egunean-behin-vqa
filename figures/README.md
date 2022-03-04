# Egunean behin figurak

## **Nola erabili**

### **1.** Ingurune birtuala sortu
Deskargatu kode hau eta sortu [virtualenv](https://virtualenv.pypa.io/en/latest/) bat
karpetan bertan, horrela zure sistemako python ingurunea ez duzu kakaztuko.
```bash
    $ python3 -m venv myvenv
```
### **2.** Ingurune birtuala aktibatu

```bash
    $ source myvenv/bin/activate 
```

### **3.** Dependentziak instalatu

```bash
    $ pip install -r requirements.txt
```

### **4.** Programaren exekuzioa

```bash
   $ python sortu_figurak.py
   $ cp figurak/* examples/.
   $ python sortu_galderak.py
```

Programaren emaitza, galderak.csv fitxategia eta figurak karpeta izango dira.

## **Galderen izaera**

Mugikorrean ondo ikusiko den tamaina bateko irudiak sortzea da gakoa (600 x 400 pixeleko ohial bat, adibidez), eta bertan zenbait figura geometriko sartu, kolore desberdinetakoak. Galderek eskatzen dute forma bateko edo besteko figurak kontatzea, erantzun zuzenaz gain, bi oker ere eskainiz,. Ikusi emaitzen adibidea, galderak.csv

## **Figurak sortzeko programa**

Galdera hauek sortzeko pythoneko PIL (Python Image Library) libreria sortu dugu.
Hasiera aldagai lokal bezala egingo dugun irudiaren (oihalaren) tamaina definituko dugu (600,400) eta figurek izango dute hiru kolore posibleak, gorria, berdea eta urdina.
Irudi mota bakoitzak bere funtzioa izango, marrazt_borobola, marraztu_karratua eta marraztu_triangelua.
Funtzioek 4 parametro jasoko dituzte, oihala(draw), posizioa(x,y) eta tamaina.
Funtzio honek tamaina jakin horretako poligonoa marraztuko du esandako tokian, eta ausazko kolore batekin.

marraztu_galdera funtzioak ausaz hiru funtzio hauen artean aukeratu eta n_x bider n_y figura marraztuko ditu.
Eta marraztu ahala, zein koloretako zein figura marraztu duen apuntatuko du, gero zenbat dauden jakiteko.
Horretarako bi zifratako identifikadore bat erabiliko dugu non lehengo zifra figura izango den eta bigarrena kolorea:

0 - Hirukia, 1 - Laukia, 2 - Borobila
0 - Gorria, 1 - Berdea, 2 - Urdina

Beraz :
00 - Hiruki gorria,
01 - Hiruki berdea,
...
22 - Borobil urdina

Fitxategia gordetzerakoan ordenean bakoitzeko zenbat sortu ditugun jarriko dugu fitxategiaren izenean gero datubasera kargatzerako orduan jakiteko irudi horretan zenbat figura/kolore ditugun.

![Adibide irudia](https://github.com/egunean-behin/egunean_behin_figurak/blob/master/examples/fig_2_2_2_4_0_7_2_3_2.png?raw=true)

Adibidez, honako irudi honek fitxategi izen hau dauka:

fig_2_2_2_4_0_7_2_3_2.png

Izeneko zenbaki bakoitzak, bere posizio zehatzean, esangura zehatz bat dauka. Kasu honetan:

1. posizioan, 2: bi hiruki gorri
2. Posizioan, 2: bi hiruki berde
3. Posizioan, 2: bi hiruki urdin
4. Posizioan, 4: 4 lauki gorri
5. Posizioan, 0: 0 lauki berde
6. Posizioan, 7: 7 lauki urdin
7. Posizioan, 2: 2 borobil gorri
8. Posizioan, 3: 3 borobil berde
9. Posizioan, 2: 2 borobil urdin

## **Irudi fitxategietatik galderetara**

sortu_figurak.py programaren bidez, beraz, sortzen ditugu, adibidez eta kopuru bat ematearren, 20 irudi. Irudi fitxategi bakoitzak du, bere izenean, figura kopuruen gakoa.

Orduan, zerrenda hau daukagu,

fig_2_5_2_4_0_6_2_3_2.png

fig_2_2_2_4_0_7_2_3_2.png

...

Eta zerrenda horri, aplikatzen diogularik idatzi dugun beste programa, sortu_galderak.py.

Programa honek /examples karpetako irudiak rekorritzen ditu eta bakoitzarekin galdera bat sortzen du. Aleatorioki aukeratzen du zein kolore eta zein figuragatik galdetuko duen, lehenago azaldu dugun bezala, irudiaren fitxategi izenetik irakurtzen du kolore hortako zenbat figura dauden.

Beste funtzio batek, aleatorioki erantzun okerrak sortzen ditu, erantzun zuzenarekin koinziditzen ez dutenak.
Datu guzti hauek zerrenda batean sartu eta zerrenda hori .csv fitxategi batean idazten du, gero Egunean Behineko datu basera kargatu ahal izateko.