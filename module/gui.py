import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from .file_handler import read_file, write_file, list_asm_files, read_ignore_list
from .text_processor import extract_texts, replace_texts, validate_syntax
from .translator import google_translate, chatgpt_translate, copilot_translate
from .logger import error_logger, changes_logger

class App:
    def __init__(self, root, german_path, english_path):
        self.root = root
        self.root.title("Vergleiche und Ersetze by Gizmo")
        self.german_path = german_path
        self.english_path = english_path
        self.ignore_dirs, self.ignore_files = read_ignore_list('ignorieren.txt')
        self.current_file_index = 0
        self.asm_files = list_asm_files(english_path, self.ignore_dirs, self.ignore_files)
        self.create_widgets()
        self.load_next_file()

    def create_widgets(self):
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(expand=True, fill='both')

        self.german_path_label = tk.Label(self.text_frame, text="Deutscher Pfad: Keine")
        self.german_path_label.pack(side='top')

        self.german_text_box = tk.Text(self.text_frame, wrap='word', width=40)
        self.german_text_box.pack(side='left', expand=True, fill='both')

        self.english_path_label = tk.Label(self.text_frame, text="Englischer Pfad: Keine")
        self.english_path_label.pack(side='top')

        self.english_text_box = tk.Text(self.text_frame, wrap='word', width=40)
        self.english_text_box.pack(side='left', expand=True, fill='both')

        self.preview_text_box = tk.Text(self.text_frame, wrap='word', width=40)
        self.preview_text_box.pack(side='left', expand=True, fill='both')

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side='bottom', fill='x')

        self.create_button(self.button_frame, 'Ersetzen', self.replace_text, "Ersetzt den Text in der aktuellen Datei")
        self.create_button(self.button_frame, 'Überspringen', self.skip_file, "Überspringt die aktuelle Datei")
        self.create_button(self.button_frame, 'Abbrechen', self.root.quit, "Beendet das Programm")
        self.create_button(self.button_frame, 'Datei Ignorieren', self.ignore_file, "Ignoriert die aktuelle Datei")
        self.create_button(self.button_frame, 'Ordner Ignorieren', self.ignore_folder, "Ignoriert den aktuellen Ordner")
        self.create_button(self.button_frame, 'Linken', self.link_files, "Verlinkt zwei Dateien")
        self.create_button(self.button_frame, 'Übersetzen', self.translate_text, "Übersetzt den ausgewählten Text")

        self.progress = Progressbar(self.root, orient='horizontal', length=100, mode='determinate')
        self.progress.pack(side='bottom', fill='x')

    def create_button(self, frame, text, command, tooltip_text):
        button = tk.Button(frame, text=text, command=command)
        button.pack(side='left')
        self.create_tooltip(button, tooltip_text)

    def create_tooltip(self, widget, text):
        tooltip = tk.Toplevel(widget)
        tooltip.withdraw()
        tooltip.overrideredirect(True)
        tooltip_label = tk.Label(tooltip, text=text, background="yellow", relief="solid", borderwidth=1)
        tooltip_label.pack()

        def show_tooltip(event):
            tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            tooltip.deiconify()

        def hide_tooltip(event):
            tooltip.withdraw()

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def load_next_file(self):
        if self.current_file_index < len(self.asm_files):
            english_file_path = os.path.join(self.english_path, self.asm_files[self.current_file_index])
            german_file_path = os.path.join(self.german_path, self.asm_files[self.current_file_index])
            english_lines = read_file(english_file_path)
            
            try:
                german_lines = read_file(german_file_path)
            except FileNotFoundError:
                german_lines = []

            self.update_text_boxes(english_lines, german_lines, english_file_path, german_file_path)
            self.current_file_index += 1
        else:
            messagebox.showinfo("Info", "Alle Dateien wurden bearbeitet.")

    def update_text_boxes(self, english_lines, german_lines, english_file_path, german_file_path):
        self.english_text_box.delete(1.0, tk.END)
        self.english_text_box.insert(tk.END, ''.join(english_lines))
        self.german_text_box.delete(1.0, tk.END)
        self.german_text_box.insert(tk.END, ''.join(german_lines))
        self.english_path_label.config(text=f"Englischer Pfad: {english_file_path}")
        self.german_path_label.config(text=f"Deutscher Pfad: {german_file_path}")

        german_texts = extract_texts(german_lines)
        english_texts = extract_texts(english_lines)
        new_english_lines = replace_texts(english_lines, german_texts, english_texts, self.ignore_files)
        self.preview_text_box.delete(1.0, tk.END)
        self.preview_text_box.insert(tk.END, ''.join(new_english_lines))

        self.mark_texts(self.german_text_box, german_texts)
        self.mark_texts(self.preview_text_box, german_texts)

    def mark_texts(self, text_box, texts):
        for text in texts:
            start = '1.0'
            while True:
                start = text_box.search(text, start, stopindex=tk.END)
                if not start:
                    break
                end = f"{start}+{len(text)}c"
                text_box.tag_add("highlight", start, end)
                text_box.tag_config("highlight", background="yellow")
                start = end

    def replace_text(self):
        try:
            english_file_path = os.path.join(self.english_path, self.asm_files[self.current_file_index - 1])
            english_lines = read_file(english_file_path)
            german_file_path = os.path.join(self.german_path, self.asm_files[self.current_file_index - 1])
            german_lines = read_file(german_file_path)

            german_texts = extract_texts(german_lines)
            english_texts = extract_texts(english_lines)
            new_english_lines = replace_texts(english_lines, german_texts, english_texts, self.ignore_files)

            syntax_check = validate_syntax(new_english_lines)
            if syntax_check is not True:
                raise SyntaxError(syntax_check)

            write_file(english_file_path, new_english_lines)
            changes_logger.info(f"Texte in Datei {english_file_path} erfolgreich ersetzt.")
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
            current_file = self.asm_files[self.current_file_index - 1]
            self.ignore_files.append(current_file)
            with open('ignorieren.txt', 'a', encoding='utf-8') as file:
                file.write(f"FILE:{current_file}\n")
            self.load_next_file()
        except Exception as e:
            error_logger.error(f"Fehler beim Ignorieren der Datei: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Ignorieren der Datei: {e}")

    def ignore_folder(self):
        try:
            current_folder = os.path.dirname(self.asm_files[self.current_file_index - 1])
            self.ignore_dirs.append(current_folder)
            with open('ignorieren.txt', 'a', encoding='utf-8') as file:
                file.write(f"DIR:{current_folder}\n")
            self.asm_files = [f for f in self.asm_files if not f.startswith(current_folder)]
            self.load_next_file()
        except Exception as e:
            error_logger.error(f"Fehler beim Ignorieren des Ordners: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Ignorieren des Ordners: {e}")

    def link_files(self):
        try:
            german_file_path = filedialog.askopenfilename(title="Deutsche Datei auswählen", filetypes=[("ASM Dateien", "*.asm")])
            if not german_file_path:
                return

            english_file_path = filedialog.askopenfilename(title="Englische Datei auswählen", filetypes=[("ASM Dateien", "*.asm")])
            if not english_file_path:
                return

            german_lines = read_file(german_file_path)
            english_lines = read_file(english_file_path)

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
                    german_selected_text = german_text_box.get(tk.SEL_FIRST, tk.SEL_LAST)
                    english_selected_text = english_text_box.get(tk.SEL_FIRST, tk.SEL_LAST)

                    new_english_lines = [line.replace(english_selected_text, german_selected_text) for line in english_lines]

                    syntax_check = validate_syntax(new_english_lines)
                    if syntax_check is not True:
                        raise SyntaxError(syntax_check)

                    write_file(english_file_path, new_english_lines)
                    changes_logger.info(f"Texte in Datei {english_file_path} erfolgreich ersetzt.")
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
            selected_text = self.german_text_box.get(tk.SEL_FIRST, tk.SEL_LAST)
            if not selected_text:
                messagebox.showinfo("Info", "Bitte wählen Sie einen Text zum Übersetzen aus.")
                return

            translate_window = tk.Toplevel(self.root)
            translate_window.title("Übersetzungsoptionen")

            def google_translate_text():
                translated_text = google_translate(selected_text, target_language='en')
                self.preview_text_box.insert(tk.INSERT, translated_text)
                translate_window.destroy()

            def chatgpt_translate_text():
                api_key = "YOUR_OPENAI_API_KEY"
                translated_text = chatgpt_translate(selected_text, target_language='en', api_key=api_key)
                self.preview_text_box.insert(tk.INSERT, translated_text)
                translate_window.destroy()

            def copilot_translate_text():
                translated_text = copilot_translate(selected_text, target_language='en')
                self.preview_text_box.insert(tk.INSERT, translated_text)
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

def start_gui(german_path, english_path):
    root = tk.Tk()
    root.title("Vergleiche und Ersetze by Gizmo")
    app = App(root, german_path, english_path)
    root.mainloop()
