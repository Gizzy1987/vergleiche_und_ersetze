import argparse
import os
import sys
import subprocess
import time
from threading import Timer
sys.path.append(os.path.join(os.path.dirname(__file__), 'module'))
from tkinter import Tk, Text, Button, Label, Scrollbar, END, StringVar
from tkinter.ttk import Progressbar
from dateioperationen import lese_datei, schreibe_datei
from ignorierlisten import lese_ignorierlisten, soll_ignorieren
from textverarbeitung import extrahiere_texte, ersetze_texte
from verzeichnisoperationen import kopiere_verzeichnis
from gui import erstelle_gui, yview
from vergleichsliste import speichere_vergleichsliste, lade_vergleichsliste, scanne_dateien

# Arbeitsordner erstellen
arbeitsordner = 'arbeitsordner'
if not os.path.exists(arbeitsordner):
    os.makedirs(arbeitsordner)

# Pfade anpassen
kopiertes_englisches_verzeichnis = os.path.join(arbeitsordner, 'kopierter_source')
vergleichsliste_pfad = os.path.join(arbeitsordner, 'vergleichsliste.json')
log_dateipfad = os.path.join(arbeitsordner, 'ersetzungs_log.txt')

# Liste der Vergleichstreffer
vergleichsliste = []
aktueller_index = 0

# Globale Variablen für Inhalte
deutscher_inhalt = ""
englischer_inhalt = ""
aktualisierter_englischer_inhalt = ""
englische_dateipfad = ""

def neustarten():
    python = sys.executable
    os.execl(python, python, *['"' + arg + '"' for arg in sys.argv])

def verarbeite_naechste_datei():
    global aktueller_index, englischer_inhalt, deutscher_inhalt, aktualisierter_englischer_inhalt, englische_dateipfad
    if aktueller_index < len(vergleichsliste):
        englische_dateipfad, deutsche_dateipfad = vergleichsliste[aktueller_index]
        englischer_inhalt = lese_datei(englische_dateipfad)
        deutscher_inhalt = lese_datei(deutsche_dateipfad)
        
        deutsche_texte = extrahiere_texte(deutscher_inhalt)
        aktualisierter_englischer_inhalt, erfolg = ersetze_texte(englischer_inhalt, deutsche_texte)
        
        if erfolg:
            aktualisiere_textboxen(englische_textbox, deutsche_textbox, aktualisierte_textbox, datei_label, englischer_inhalt, deutscher_inhalt, aktualisierter_englischer_inhalt, englische_dateipfad)
        else:
            aktueller_index += 1
            verarbeite_naechste_datei()
    else:
        print("Keine weiteren Treffer gefunden.")

def aktualisiere_textboxen(englische_textbox, deutsche_textbox, aktualisierte_textbox, datei_label, englischer_inhalt, deutscher_inhalt, aktualisierter_englischer_inhalt, dateipfad):
    englische_textbox.delete(1.0, END)
    deutsche_textbox.delete(1.0, END)
    aktualisierte_textbox.delete(1.0, END)
    
    englische_textbox.insert(END, englischer_inhalt)
    deutsche_textbox.insert(END, deutscher_inhalt)
    aktualisierte_textbox.insert(END, aktualisierter_englischer_inhalt)
    
    datei_label.config(text=dateipfad)

    # Markiere den zu verändernden Text
    englische_texte = extrahiere_texte(englischer_inhalt)
    deutsche_texte = extrahiere_texte(deutscher_inhalt)
    for eng_text, deu_text in zip(englische_texte, deutsche_texte):
        start_idx = englischer_inhalt.find(f'"{eng_text}"')
        end_idx = start_idx + len(f'"{eng_text}"')
        englische_textbox.tag_add("highlight", f"1.0+{start_idx}c", f"1.0+{end_idx}c")
        englische_textbox.tag_config("highlight", background="yellow")

        start_idx = deutscher_inhalt.find(f'"{deu_text}"')
        end_idx = start_idx + len(f'"{deu_text}"')
        deutsche_textbox.tag_add("highlight", f"1.0+{start_idx}c", f"1.0+{end_idx}c")
        deutsche_textbox.tag_config("highlight", background="yellow")

def ersetze_text():
    global aktueller_index, aktualisierter_englischer_inhalt, englische_dateipfad
    schreibe_datei(englische_dateipfad, aktualisierter_englischer_inhalt)
    with open(log_dateipfad, 'a', encoding='utf-8') as log_datei:
        log_datei.write(f"{englische_dateipfad}\n")
    aktueller_index += 1
    speichere_vergleichsliste(vergleichsliste_pfad, vergleichsliste[aktueller_index:])
    verarbeite_naechste_datei()
    root.update_idletasks()

def ueberspringe_text():
    global aktueller_index
    aktueller_index += 1
    speichere_vergleichsliste(vergleichsliste_pfad, vergleichsliste[aktueller_index:])
    verarbeite_naechste_datei()
    root.update_idletasks()

def ignoriere_datei():
    global aktueller_index, englische_dateipfad
    with open('ignorierliste.txt', 'a', encoding='utf-8') as datei:
        datei.write(f"FILE:{os.path.basename(englische_dateipfad)}\n")
    aktueller_index += 1
    speichere_vergleichsliste(vergleichsliste_pfad, vergleichsliste[aktueller_index:])
    verarbeite_naechste_datei()
    root.update_idletasks()

def ignoriere_ordner():
    global aktueller_index, englische_dateipfad
    ordner = os.path.dirname(englische_dateipfad)
    with open('ignorierliste.txt', 'a', encoding='utf-8') as datei:
        datei.write(f"DIR:{ordner}\n")
    aktueller_index += 1
    speichere_vergleichsliste(vergleichsliste_pfad, vergleichsliste[aktueller_index:])
    verarbeite_naechste_datei()
    root.update_idletasks()

def stoppe_script():
    root.destroy()

def pruefe_textboxen():
    if not englische_textbox.get(1.0, END).strip():
        print("Textboxen sind leer. Neustart des Programms.")
        neustarten()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extrahiere und ersetze Dialogblöcke in Quelldateien.')
    parser.add_argument('englisches_verzeichnis', type=str, help='Pfad zum Verzeichnis mit den englischen Quelldateien')
    parser.add_argument('deutsches_verzeichnis', type=str, help='Pfad zum Verzeichnis mit den deutschen Quelldateien')
    args = parser.parse_args()

    # Kopiere das englische Verzeichnis in einen neuen Ordner
    kopiertes_englisches_verzeichnis = os.path.join(arbeitsordner, 'kopierter_source')
    deutsches_verzeichnis = args.deutsches_verzeichnis

    # Initialisiere die Ignorierlisten
    IGNORIER_VERZEICHNISSE, IGNORIER_DATEIEN = lese_ignorierlisten('ignorierliste.txt')

    # Lade die Vergleichsliste oder scanne die Dateien, wenn die Liste nicht existiert
    vergleichsliste = lade_vergleichsliste(vergleichsliste_pfad)
    if not vergleichsliste:
        scanne_dateien(kopiertes_englisches_verzeichnis, deutsches_verzeichnis, IGNORIER_VERZEICHNISSE, IGNORIER_DATEIEN)

    # Erstelle die GUI
    root, deutsche_textbox, englische_textbox, aktualisierte_textbox, datei_label, fortschritt_var = erstelle_gui(ersetze_text, ueberspringe_text, ignoriere_datei, ignoriere_ordner, stoppe_script)

    if not os.path.exists(kopiertes_englisches_verzeichnis):
        kopiere_verzeichnis(args.englisches_verzeichnis, kopiertes_englisches_verzeichnis, fortschritt_var)
    verarbeite_naechste_datei()

    # Warte 1,5 Sekunden und prüfe dann die Textboxen
    Timer(1.5, pruefe_textboxen).start()

    root.mainloop()
