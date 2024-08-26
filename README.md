# Vergleiche und Ersetze

## Beschreibung
Dieses Programm durchsucht zwei Pfade, die über die Kommandozeile übermittelt werden. Diese Pfade enthalten Assembler-Source-Codes für .gb-Spiele, wobei einer auf Deutsch und der andere auf Englisch ist. Das Programm schreibt die Texte der deutschen Version an die richtigen Stellen der englischen Version, ohne den eigentlichen Code zu verändern.

## Installation
1. Klone das Repository:
    ```bash
    git clone https://github.com/Gizzy1987/vergleiche_und_ersetze.git
    ```
2. Installiere die Abhängigkeiten:
    ```bash
    pip install -r requirements.txt
    ```

## Nutzung
```bash
python main.py <german_path> <english_path>
```

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