def lese_ignorierlisten(dateipfad):
    ignorier_verzeichnisse = []
    ignorier_dateien = []
    with open(dateipfad, 'r', encoding='utf-8') as datei:
        for zeile in datei:
            zeile = zeile.strip()
            if zeile.startswith('DIR:'):
                ignorier_verzeichnisse.append(zeile[4:])
            elif zeile.startswith('FILE:'):
                ignorier_dateien.append(zeile[5:])
    return ignorier_verzeichnisse, ignorier_dateien

def soll_ignorieren(pfad, ignorier_verzeichnisse, ignorier_dateien):
    for ignorier_verzeichnis in ignorier_verzeichnisse:
        if ignorier_verzeichnis in pfad:
            return True
    for ignorier_datei in ignorier_dateien:
        if pfad.endswith(ignorier_datei):
            return True
    return False
