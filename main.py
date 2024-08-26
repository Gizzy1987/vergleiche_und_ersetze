import os
import shutil
from module import file_handler, text_processor, gui, logger

def main():
    # Pfade von der Kommandozeile einlesen
    import argparse
    parser = argparse.ArgumentParser(description='Assembler Source Code Translator')
    parser.add_argument('german_path', type=str, help='Pfad zur deutschen Source')
    parser.add_argument('english_path', type=str, help='Pfad zur englischen Source')
    args = parser.parse_args()

    # Sicherungskopie der englischen Dateien erstellen
    backup_path = 'backup'
    ignore_dirs, ignore_files = file_handler.read_ignore_list('ignorieren.txt')
    file_handler.backup_files(args.english_path, backup_path, ignore_dirs, ignore_files)

    # GUI starten
    gui.start_gui(args.german_path, backup_path)

if __name__ == '__main__':
    main()
