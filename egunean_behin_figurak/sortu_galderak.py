import os
import random
import csv
from random import choice


path='./examples/'
galdera_oinarria = 'Zenbat %s %s?'

figurak = ['hiruki', 'lauki', 'borobil']
koloreak = ['gorri', 'berde', 'urdin']

def galderak_idatzi():
    galderak=sortu_galderak()
    with open('galderak.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Galdera','Erantzun zuzena', 'Erantzun okerra 1','Erantzun okerra 2','Fitxategia'])
        for galdera in galderak:
            spamwriter.writerow(galdera)


def erantzun_okerrak(zuzena):
    erantzunak=[int(zuzena)]
    erantzunak.append(choice([i for i in range(1,10) if i not in erantzunak]))
    erantzunak.append(choice([i for i in range(1,10) if i not in erantzunak]))
    return erantzunak[1:] #Erantzun okerrak soilik bueltatu

def sortu_galderak():
    irudiak = os.listdir(path)
    galderak_list=[]

    for izena in irudiak:
        figura = random.randint(0,2)
        kolorea = random.randint(0,2)
        kolorea_txt = koloreak[kolorea]
        figura_txt = figurak[figura]
        posizioa = (figura*3)+kolorea
        kopuruak = izena.split('.')[0].split('_')[1:]
        galdera = galdera_oinarria%(figura_txt,kolorea_txt)
        zuzena = kopuruak[posizioa]
        okerrak = erantzun_okerrak(zuzena)
        galderak_list.append([galdera, zuzena, okerrak[0],okerrak[1],izena])
    return galderak_list

if __name__ == '__main__':
    galderak_idatzi()
