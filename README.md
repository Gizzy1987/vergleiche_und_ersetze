# Assembler Source Code Translator

## Beschreibung
Dieses Programm durchsucht zwei Pfade, die über die Kommandozeile übermittelt werden. Diese Pfade enthalten Assembler-Source-Codes für .gb-Spiele, wobei einer auf Deutsch und der andere auf Englisch ist. Das Programm schreibt die Texte der deutschen Version an die richtigen Stellen der englischen Version, ohne den eigentlichen Code zu verändern.

## Installation
1. Klone das Repository:
    ```bash
    git clone <repository-url>
    ```
2. Installiere die Abhängigkeiten:
    ```bash
    pip install -r requirements.txt
    ```

## Nutzung
```bash
python main.py <german_path> <english_path>


vergleiche_und_ersetze/
│
├── Module/
│   ├── __init__.py
│   ├── file_handler.py
│   ├── text_processor.py
│   ├── gui.py
│   ├── logger.py
│
├── Logs/
│   ├── error.log
│   ├── operations.log
│   ├── changes.log
│   ├── missing_texts.log
│
├── main.py
├── ignorieren.txt
└── README.md


GUI
Die GUI bietet verschiedene Buttons und Funktionen zum Bearbeiten und Übersetzen der Texte.

Buttons
Ersetzen: Schreibt eine Änderung in die kopierte englische Datei.
Überspringen: Nimmt die nächste Datei und ändert die aktuelle Datei nicht.
Abbrechen: Beendet das Programm.
Datei Ignorieren: Schreibt die aktuelle Datei auf die ignorieren.txt.
Ordner Ignorieren: Schreibt den aktuellen Ordner auf die ignorieren.txt.
Linken: Ermöglicht das Verlinken von deutschen und englischen Dateien zur manuellen Textübertragung.
Logs
Logs werden im Ordner “Logs” erstellt:

Fehlerlogs (error.log)
Betriebslogs (operations.log)
Änderungslogs (changes.log)
Logs für fehlende Texte (missing_texts.log)
Funktionen
Textersetzung
Die Funktion replace_text ersetzt die Texte in den englischen Dateien durch die deutschen Texte und führt eine Syntaxprüfung durch, um sicherzustellen, dass die Änderungen die Syntax nicht beschädigen.

Verlinkung von Dateien
Die Funktion link_files ermöglicht es, zwei Dateien (eine deutsche und eine englische) auszuwählen und Textstellen manuell zu verlinken. Der markierte Text in der englischen Datei wird durch den markierten Text in der deutschen Datei ersetzt.

Ignorieren von Dateien und Ordnern
Die Funktionen ignore_file und ignore_folder ermöglichen es, bestimmte Dateien und Ordner zu ignorieren, indem sie zur ignorieren.txt hinzugefügt werden.

Syntaxprüfung
Die Funktion validate_syntax überprüft die grundlegende Syntax der Assembler-Dateien, um sicherzustellen, dass die Änderungen die Syntax nicht beschädigen.

Fortschrittsanzeige
Eine Fortschrittsanzeige (Progressbar) zeigt den Fortschritt des Kopiervorgangs an.

Schlüsselwörter-Datenbank
Eine Schlüsselwörter-Datenbank speichert alle bekannten und neuen Schlüsselwörter, die durch die “Linken”-Funktion hinzugefügt werden.

Hinweise
Nur .asm Dateien werden einbezogen.
Wenn eine .asm Datei keine nutzbaren Texte (Schlüsselwörter) enthält, wird diese übersprungen.
Beispiel
python main.py /path/to/german/source /path/to/english/source


### Zusammenfassung
- **Textersetzung**: Die Funktion `replace_text` ersetzt die Texte in den englischen Dateien durch die deutschen Texte und führt eine Syntaxprüfung durch.
- **Verlinkung von Dateien**: Die Funktion `link_files` ermöglicht es, zwei Dateien auszuwählen und Textstellen manuell zu verlinken.
- **Ignorieren von Dateien und Ordnern**: Die Funktionen `ignore_file` und `ignore_folder` ermöglichen es, bestimmte Dateien und Ordner zu ignorieren.
- **Syntaxprüfung**: Die Funktion `validate_syntax` überprüft die grundlegende Syntax der Assembler-Dateien.
- **Fortschrittsanzeige**: Eine Fortschrittsanzeige zeigt den Fortschritt des Kopiervorgangs an.
- **Schlüsselwörter-Datenbank**: Eine Schlüsselwörter-Datenbank speichert alle bekannten und neuen Schlüsselwörter.
- **Übersetzungsdienste: Die Funktion translate_text integriert Google Translate, ChatGPT und Copilot für die Übersetzung von Texten.