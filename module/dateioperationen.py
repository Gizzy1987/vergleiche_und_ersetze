import os

def lese_datei(dateipfad):
    with open(dateipfad, 'r', encoding='utf-8') as datei:
        return datei.read()

def schreibe_datei(dateipfad, inhalt):
    with open(dateipfad, 'w', encoding='utf-8') as datei:
        datei.write(inhalt)
