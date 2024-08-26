import re

def extract_texts(lines):
    texts = []
    for line in lines:
        matches = re.findall(r'"(.*?)"', line)
        texts.extend(matches)
    return texts

def replace_texts(lines, german_texts, english_texts, ignore_list):
    for i, line in enumerate(lines):
        for german, english in zip(german_texts, english_texts):
            if german in line and german not in ignore_list:
                lines[i] = line.replace(german, english)
    return lines

def validate_syntax(lines):
    """
    Diese Funktion überprüft die grundlegende Syntax der Assembler-Dateien.
    """
    try:
        for line in lines:
            # Beispielhafte Syntaxprüfung: Überprüfen, ob jede Zeile mit einem gültigen Befehl beginnt
            if not re.match(r'^\s*(\w+:)?\s*(\w+)?\s*', line):
                raise SyntaxError(f"Syntaxfehler in Zeile: {line.strip()}")
        return True
    except SyntaxError as e:
        return str(e)

def update_charmap(charmap_path):
    # Implementiere die Logik zur Aktualisierung der charmap.asm Datei
    pass
