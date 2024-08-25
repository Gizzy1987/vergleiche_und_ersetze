from tkinter import Tk, Text, Button, Label, Scrollbar, END, StringVar
from tkinter.ttk import Progressbar

def erstelle_gui(ersetze_text, ueberspringe_text, ignoriere_datei, ignoriere_ordner, stoppe_script):
    root = Tk()
    root.title("Text Ersetzung")

    Label(root, text="Deutscher Source").grid(row=0, column=0)
    Label(root, text="Englischer Source").grid(row=0, column=1)
    Label(root, text="Verarbeitete Datei").grid(row=0, column=2)

    # Scrollbars hinzufügen
    deutsche_scrollbar = Scrollbar(root)
    englische_scrollbar = Scrollbar(root)
    aktualisierte_scrollbar = Scrollbar(root)

    deutsche_textbox = Text(root, width=60, height=25, wrap="none", yscrollcommand=deutsche_scrollbar.set)
    deutsche_textbox.grid(row=1, column=0)
    deutsche_scrollbar.config(command=lambda *args: yview(*args, deutsche_textbox, englische_textbox, aktualisierte_textbox))
    deutsche_scrollbar.grid(row=1, column=0, sticky='nse')

    englische_textbox = Text(root, width=60, height=25, wrap="none", yscrollcommand=englische_scrollbar.set)
    englische_textbox.grid(row=1, column=1)
    englische_scrollbar.config(command=lambda *args: yview(*args, deutsche_textbox, englische_textbox, aktualisierte_textbox))
    englische_scrollbar.grid(row=1, column=1, sticky='nse')

    aktualisierte_textbox = Text(root, width=60, height=25, wrap="none", yscrollcommand=aktualisierte_scrollbar.set)
    aktualisierte_textbox.grid(row=1, column=2)
    aktualisierte_scrollbar.config(command=lambda *args: yview(*args, deutsche_textbox, englische_textbox, aktualisierte_textbox))
    aktualisierte_scrollbar.grid(row=1, column=2, sticky='nse')

    datei_label = Label(root, text="")
    datei_label.grid(row=2, column=0, columnspan=3)

    Button(root, text="Ersetzen", command=ersetze_text).grid(row=3, column=0)
    Button(root, text="Überspringen", command=ueberspringe_text).grid(row=3, column=1)
    Button(root, text="Abbrechen", command=stoppe_script).grid(row=3, column=2)
    Button(root, text="Datei Ignorieren", command=ignoriere_datei).grid(row=3, column=3)
    Button(root, text="Ordner Ignorieren", command=ignoriere_ordner).grid(row=3, column=4)

    fortschritt_var = StringVar()
    fortschritt_balken = Progressbar(root, orient="horizontal", length=400, mode="determinate", variable=fortschritt_var)
    fortschritt_balken.grid(row=4, column=0, columnspan=5)

    return root, deutsche_textbox, englische_textbox, aktualisierte_textbox, datei_label, fortschritt_var

def yview(*args, deutsche_textbox, englische_textbox, aktualisierte_textbox):
    deutsche_textbox.yview(*args)
    englische_textbox.yview(*args)
    aktualisierte_textbox.yview(*args)
