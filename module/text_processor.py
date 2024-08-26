import re

def extract_texts(content):
    # Regex zum Finden von Textblöcken, einschließlich mehrzeiliger Blöcke
    return re.findall(r'"(.*?)"', content, re.DOTALL)

def replace_texts(english_content, german_texts, ignore_list):
    english_texts = extract_texts(english_content)
    if len(german_texts) != len(english_texts):
        print(f"Warnung: Die Anzahl der Texte in den deutschen und englischen Dateien stimmt nicht überein. Datei wird übersprungen.")
        return english_content, False
    
    for eng_text, deu_text in zip(english_texts, german_texts):
        if eng_text not in ignore_list:
            english_content = english_content.replace(f'"{eng_text}"', f'"{deu_text}"')
    
    return english_content, True

def validate_syntax(content):
    # Beispielhafte Syntaxprüfung
    if not content:
        return "Inhalt ist leer"
    if '"' in content:
        return True
    return "Syntaxfehler: Ungültige Zeichen gefunden"
