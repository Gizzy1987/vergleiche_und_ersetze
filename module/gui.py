import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from .file_handler import read_file, write_file, list_asm_files, read_ignore_list
from .text_processor import extract_texts, replace_texts, validate_syntax, update_charmap
from .translator import google_translate, chatgpt_translate, copilot_translate
from .logger import error_logger, operations_logger, changes_logger, missing_texts_logger

class App:
    def __init__(self, root, german_path, english_path):
        self.root = root
        self.german_path = german_path
        self.english_path = english_path
        self.ignore_list = read_ignore_list('ignorieren.txt')
        self.create_widgets()
        self.current_file_index = 0
        self.asm_files = list_asm_files(english_path)
        self.load_next_file()

    def create_widgets(self):
        self.text_box = tk.Text(self.root, wrap='word')
        self.text_box.pack(expand=True, fill='both')

        self.replace_button = tk.Button(self.root, text='Ersetzen', command=self.replace_text)
        self.replace_button.pack(side='left')

        self.skip_button = tk.Button(self.root, text='Überspringen', command=self.skip_file)
        self.skip_button.pack(side='left')

        self.cancel_button = tk.Button(self.root, text='Abbrechen', command=self.root.quit)
        self.cancel_button.pack(side='left')

        self.ignore_file_button = tk.Button(self.root, text='Datei Ignorieren', command=self.ignore_file)
        self.ignore_file_button.pack(side='left')

        self.ignore_folder_button = tk.Button(self.root, text='Ordner Ignorieren', command=self.ignore_folder)
        self.ignore_folder_button.pack(side='left')

        self.link_button = tk.Button(self.root, text='Linken', command=self.link_files)
        self.link_button.pack(side='left')

        self.translate_button = tk.Button(self.root, text='Übersetzen', command=self.translate_text)
        self.translate_button.pack(side='left')

        self.progress = Progressbar(self.root, orient='horizontal', length=100, mode='determinate')
        self.progress.pack(side='bottom', fill='x')

    def load_next_file(self):
        if self.current_file_index < len(self.asm_files):
            file_path = os.path.join(self.english_path, self.asm_files[self.current_file_index])
            lines = read_file(file_path)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, ''.join(lines))
            self.current_file_index += 1
        else:
            messagebox.showinfo("Info", "Alle Dateien wurden bearbeitet.")

    def replace_text(self):
        try:
            # Aktuelle Datei laden
            english_file_path = os.path.join(self.english_path, self.asm_files[self.current_file_index - 1])
            english_lines = read_file(english_file_path)

            # Deutsche Datei laden
            german_file_path = os.path.join(self.german_path, self.asm_files[self.current_file_index - 1])
            german_lines = read_file(german_file_path)

            # Texte extrahieren
            german_texts = extract_texts(german_lines)
            english_texts = extract_texts(english_lines)

            # Texte ersetzen
            new_english_lines = replace_texts(english_lines, german_texts, english_texts, self.ignore_list)

            # Syntaxprüfung
            syntax_check = validate_syntax(new_english_lines)
            if syntax_check is not True:
                raise SyntaxError(syntax_check)

            # Änderungen in die Datei schreiben
            write_file(english_file_path, new_english_lines)

            # GUI aktualisieren
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, ''.join(new_english_lines))

            # Loggen der erfolgreichen Änderung
            changes_logger.info(f"Texte in Datei {english_file_path} erfolgreich ersetzt.")

            # Nächste Datei laden
            self.load_next_file()

        except SyntaxError as e:
            error_logger.error(f"Syntaxfehler: {e}")
            messagebox.showerror("Syntaxfehler", f"Syntaxfehler: {e}")
        except Exception as e:
            error_logger.error(f"Fehler beim Ersetzen der Texte: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Ersetzen der Texte: {e}")

    def skip_file(self):
        self.load_next_file()

    def ignore_file(self):
        try:
            with open('ignorieren.txt', 'a', encoding='utf-8') as file:
                file.write(self.asm_files[self.current_file_index - 1] + '\n')
            self.load_next_file()
        except Exception as e:
            error_logger.error(f"Fehler beim Ignorieren der Datei: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Ignorieren der Datei: {e}")

    def ignore_folder(self):
        try:
            folder_path = os.path.dirname(os.path.join(self.english_path, self.asm_files[self.current_file_index - 1]))
            with open('ignorieren.txt', 'a', encoding='utf-8') as file:
                file.write(folder_path + '\n')
            self.load_next_file()
        except Exception as e:
            error_logger.error(f"Fehler beim Ignorieren des Ordners: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Ignorieren des Ordners: {e}")

    def link_files(self):
        try:
            # Deutsche Datei auswählen
            german_file_path = filedialog.askopenfilename(title="Deutsche Datei auswählen", filetypes=[("ASM Dateien", "*.asm")])
            if not german_file_path:
                return

            # Englische Datei auswählen
            english_file_path = filedialog.askopenfilename(title="Englische Datei auswählen", filetypes=[("ASM Dateien", "*.asm")])
            if not english_file_path:
                return

            # Deutsche Datei laden
            german_lines = read_file(german_file_path)

            # Englische Datei laden
            english_lines = read_file(english_file_path)

            # Neue Fenster für die Dateien erstellen
            link_window = tk.Toplevel(self.root)
            link_window.title("Dateien verlinken")

            german_text_box = tk.Text(link_window, wrap='word')
            german_text_box.pack(side='left', expand=True, fill='both')
            german_text_box.insert(tk.END, ''.join(german_lines))

            english_text_box = tk.Text(link_window, wrap='word')
            english_text_box.pack(side='right', expand=True, fill='both')
            english_text_box.insert(tk.END, ''.join(english_lines))

            def replace_linked_text():
                try:
                    # Markierten Text aus beiden Textboxen holen
                    german_selected_text = german_text_box.get(tk.SEL_FIRST, tk.SEL_LAST)
                    english_selected_text = english_text_box.get(tk.SEL_FIRST, tk.SEL_LAST)

                    # Texte ersetzen
                    new_english_lines = [line.replace(english_selected_text, german_selected_text) for line in english_lines]

                    # Syntaxprüfung
                    syntax_check = validate_syntax(new_english_lines)
                    if syntax_check is not True:
                        raise SyntaxError(syntax_check)

                    # Änderungen in die Datei schreiben
                    write_file(english_file_path, new_english_lines)

                    # Loggen der erfolgreichen Änderung
                    changes_logger.info(f"Texte in Datei {english_file_path} erfolgreich ersetzt.")

                    # Fenster schließen
                    link_window.destroy()

                except SyntaxError as e:
                    error_logger.error(f"Syntaxfehler: {e}")
                    messagebox.showerror("Syntaxfehler", f"Syntaxfehler: {e}")
                except Exception as e:
                    error_logger.error(f"Fehler beim Verlinken der Texte: {e}")
                    messagebox.showerror("Fehler", f"Fehler beim Verlinken der Texte: {e}")

            replace_button = tk.Button(link_window, text='Ersetzen', command=replace_linked_text)
            replace_button.pack(side='bottom')

        except Exception as e:
            error_logger.error(f"Fehler beim Verlinken der Dateien: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Verlinken der Dateien: {e}")

    def translate_text(self):
        try:
            selected_text = self.text_box.get(tk.SEL_FIRST, tk.SEL_LAST)
            if not selected_text:
                messagebox.showinfo("Info", "Bitte wählen Sie einen Text zum Übersetzen aus.")
                return

            # Übersetzungsoptionen anzeigen
            translate_window = tk.Toplevel(self.root)
            translate_window.title("Übersetzungsoptionen")

            def google_translate_text():
                translated_text = google_translate(selected_text, target_language='en')
                self.text_box.insert(tk.INSERT, translated_text)
                translate_window.destroy()

            def chatgpt_translate_text():
                api_key = "YOUR_OPENAI_API_KEY"  # Ersetze durch deinen OpenAI API-Schlüssel
                translated_text = chatgpt_translate(selected_text, target_language='en', api_key=api_key)
                self.text_box.insert(tk.INSERT, translated_text)
                translate_window.destroy()

            def copilot_translate_text():
                translated_text = copilot_translate(selected_text, target_language='en')
                self.text_box.insert(tk.INSERT, translated_text)
                translate_window.destroy()

            google_button = tk.Button(translate_window, text='Google Translate', command=google_translate_text)
            google_button.pack(side='left')

            chatgpt_button = tk.Button(translate_window, text='ChatGPT Translate', command=chatgpt_translate_text)
            chatgpt_button.pack(side='left')

            copilot_button = tk.Button(translate_window, text='Copilot Translate', command=copilot_translate_text)
            copilot_button.pack(side='left')

        except Exception as e:
            error_logger.error(f"Fehler bei der Übersetzung: {e}")
            messagebox.showerror("Fehler", f"Fehler bei der Übersetzung: {e}")
