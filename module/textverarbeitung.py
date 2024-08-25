import re

def extrahiere_texte(inhalt):
    # Regex zum Finden von Textblöcken, einschließlich mehrzeiliger Blöcke
    return re.findall(r'"(.*?)"', inhalt, re.DOTALL)

def ersetze_texte(englischer_inhalt, deutsche_texte):
    englische_texte = extrahiere_texte(englischer_inhalt)
    if len(deutsche_texte) != len(englische_texte):
        print(f"Warnung: Die Anzahl der Texte in den deutschen und englischen Dateien stimmt nicht überein. Datei wird übersprungen.")
        return englischer_inhalt, False
    
    for eng_text, deu_text in zip(englische_texte, deutsche_texte):
        englischer_inhalt = englischer_inhalt.replace(f'"{eng_text}"', f'"{deu_text}"')
    
    return englischer_inhalt, True
