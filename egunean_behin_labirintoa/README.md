# Egunean behin labirintoa

```
python laberintoenIrudiTaGalderakSortu.py
```

Labirinto bat ausaz sortuko da, ertz bakoitzak kolore bat izango du (koloreekin gehiengoarentzat problema errazten den arren, erantzunetan IE, HE, IM eta HM etiketen laguntzak jarriko dira ikusmen hurritasunen bat dutenek galdera erantzun dezaten), eta lau ertzetako batetik abiatuta, beste ertz bakarrerako bidea egongo da, jokalariak hura topatu beharko du. 

![Adibide irudia](maze.svg)

Ertz berdetik (I-M) abiatuta topatu gertueneko irteera.: [Irudia 600x400, svg formatuan]

-Urdina (I-E)

-Gorria (H-M) (Z)

-Horia (H-E)

horrela, nahi adina galdera sor litezke.

Hobekuntza posibleak:

nahi izanez gero, labirintoaren tamaina ere handitu daiteke, galderaren zailtasuna handitzeko (tamaina handitzearekin batera, puntuen kokapena eta tamaina egokitu behar da.)

Ulermena erraztearren, beti ertz berdinetik hasiko gara, honek erantzuna topatzea erraztuko luke. Hau kendu liteke, zailtasuna haunditzeko.




Irudiak png formatuan nahiko balira, hau egin liteke linuxen:
```
inkscape -z -e out.png -w 600 -h 400 maze.svg
```
bestalde, kodean aldaketa txikiren bat sortu beharko litzateke.
