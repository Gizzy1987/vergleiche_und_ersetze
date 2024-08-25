import os
import shutil
from tqdm import tqdm

def kopiere_verzeichnis(src, dest, fortschritt_var):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    gesamt_dateien = sum([len(files) for r, d, files in os.walk(src)])
    with tqdm(total=gesamt_dateien, desc="Kopiere Dateien", unit="Dateien") as pbar:
        for root, dirs, files in os.walk(src):
            for dir in dirs:
                os.makedirs(os.path.join(dest, os.path.relpath(os.path.join(root, dir), src)), exist_ok=True)
            for file in files:
                src_datei = os.path.join(root, file)
                dest_datei = os.path.join(dest, os.path.relpath(src_datei, src))
                shutil.copy2(src_datei, dest_datei)
                pbar.update(1)
                fortschritt_var.set(pbar.n / gesamt_dateien * 100)
