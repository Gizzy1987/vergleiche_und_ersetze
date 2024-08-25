import os
import json
from module.ignorierlisten import soll_ignorieren

def speichere_vergleichsliste(dateipfad, liste):
    with open(dateipfad, 'w', encoding='utf-8') as datei:
        json.dump(liste, datei)

def lade_vergleichsliste(dateipfad):
    if os.path.exists(dateipfad):
        with open(dateipfad, 'r', encoding='utf-8') as datei:
            return json.load(datei)
    return []

def scanne_dateien(englisches_verzeichnis, deutsches_verzeichnis, ignorierverzeichnisse, ignorierdateien):
    vergleichsliste = []
    for root, _, files in os.walk(englisches_verzeichnis):
        for file in files:
            if file.endswith('.asm'):
                englische_dateipfad = os.path.join(root, file)
                deutsche_dateipfad = os.path.join(deutsches_verzeichnis, os.path.relpath(englische_dateipfad, englisches_verzeichnis))
                
                print(f"Überprüfe Datei: {englische_dateipfad}")
                
                if soll_ignorieren(englische_dateipfad, ignorierverzeichnisse, ignorierdateien):
                    print(f"Ignoriere Datei: {englische_dateipfad}")
                    continue
                
                if os.path.exists(deutsche_dateipfad):
                    vergleichsliste.append((englische_dateipfad, deutsche_dateipfad))
                    print(f"Gefundene Datei: {englische_dateipfad} -> {deutsche_dateipfad}")
    
    speichere_vergleichsliste('arbeitsordner/vergleichsliste.json', vergleichsliste)
    print(f"Vergleichsliste gespeichert: {vergleichsliste}")
