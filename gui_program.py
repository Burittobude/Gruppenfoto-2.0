"""
Gruppenfoto 2.0 Arranging your group photo the best way.
Copyright (C) 2020
Andreas Schellenberger, Matthias Schellenberger  

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/
Contact: mt.schellenberger@hotmail.de
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import tkinter.font as tkFont
from tkinter import ttk
from ttkthemes import ThemedTk
import webbrowser
from backend_gf import program
import os
import sys

#WICHTIG: pyinstaller mit environment pyinstall ausführen, damit ist Größe 10 mal kleiner. 
#https://stackoverflow.com/questions/43886822/pyinstaller-with-pandas-creates-over-500-mb-exe
#https://stackoverflow.com/questions/37815371/pyinstaller-failed-to-execute-script-pyi-rth-pkgres-and-missing-packages
#Konsolenbefehl für Erstellen der .exe Datei mit gewünschtem icon.
#pyinstaller --onefile -w -i logo.ico --add-data "logo.ico;." --hidden-import pkg_resources.py2_warn "gui_program.py"
def add_sep():
    ttk.Separator(window).pack(anchor="nw", pady=5, fill='x',padx=20)

#------------
#Code für Buttons
#------------
def Button_Ordner_clicked():
    """
    Öffnet ein Dialogfenster zum Auswählen eines Ordners.
    """
    direct.delete(0,'end')
    foldername = tk.filedialog.askdirectory(initialdir = "/",title="Wählen Sie den Ordner mit den Bildern ...")
    direct.insert(0,foldername)

def Button_DINA4_clicked():
    """
    Setzt die Werte für das Ausgabeformat.
    """
    d_w.delete(0,'end')
    d_h.delete(0,'end')
    d_w.insert(0,"2480")
    d_h.insert(0,"3508")

def Button_square_clicked():
    """
    Setzt die Werte für das Ausgabeformat.
    """
    d_w.delete(0,'end')
    d_h.delete(0,'end')
    d_w.insert(0,"2000")
    d_h.insert(0,"2000")

def Button_hilfe_clicked():
    """
    Öffnet die Hilfeseite von Gruppenfoto 2.0 im Internet.
    """
    webbrowser.open("http://gruppenfoto20.bityarts.de/?page_id=71")

def Button_clicked():
    """
    Fragt nach dem Speicherort für das fertige Bild und führt die Programmroutine aus.
    """
    try:
        w, h = int(d_w.get()), int(d_h.get())
        ratio = float(r_b.get())/float(r_h.get())
        filename = tk.filedialog.asksaveasfilename(initialdir = "/", title = "Wählen Sie einen Speicherort ...", defaultextension=".png", filetypes = (("PNG","*.png"),("JPG","*.jpg")))
        program(w,h,ratio,os.path.join(direct.get()),os.path.join(filename))
    except Exception as e:
        messagebox.showerror(title="Fehler",message="Fehler! Überprüfe deine Eingaben.")
        print(e)
    try:
        os.startfile(filename)
    except:
        messagebox.showwarning(title="Warnung",message="Fehler beim Öffnen des erzeugten Bildes.")

#Von folgender Webseite, damit ein Programmicon angezeigt werden kann
#https://stackoverflow.com/questions/51060894/adding-a-data-file-in-pyinstaller-using-the-onefile-option
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#------------
#Erzeugung der GUI
#------------

#Erstellt das Fenster mit dem gewünschten Aussehen
window = ThemedTk(theme='arc')
window.resizable(0,0)
window.title("Gruppenfoto 2.0")
window.configure(bg='white')

#Läd das Programmicon
window.iconbitmap(resource_path('logo.ico')) 

#Definiert die gewünschten Schriftarten und Stile der Benutzeroberfläche
fontStyle = tkFont.Font(size=12, family= "Calibri")
fontStyle_label = tkFont.Font(size=15, family='Calibri Light')
ttk.Style().configure(".", padding=6, relief="flat",
   foreground="black", background="white", font=fontStyle)
ttk.Style().configure("TLabel", font=fontStyle_label)
ttk.Style().configure("TEntry", font=fontStyle)
fontStyle_2 = tkFont.Font(size=25, family='Calibri Light')

#-----------
#Definieren und setzen der Elemente
#-----------

ttk.Label(window,text="Gruppenfoto 2.0", font=fontStyle_2).pack()
add_sep()
frame_format = tk.Frame(window, background="white")
ttk.Label(frame_format, text="Formatvorlagen").pack(pady=1)
ttk.Button(frame_format, text="DIN A4", command =Button_DINA4_clicked).pack(pady=1, side="left")
ttk.Button(frame_format, text="Quadratisch", command =Button_square_clicked).pack(pady=1,side="right")
frame_format.pack()
add_sep()

ttk.Label(window,text="Breite des Gesamtbildes in Pixeln").pack(pady=1)
d_w = ttk.Entry(window, font=fontStyle)
d_w.pack(pady=1)
add_sep()

ttk.Label(window,text="Höhe des Gesamtbildes in Pixeln").pack(pady=1)
d_h = ttk.Entry(window, font=fontStyle)
d_h.pack(pady=1)
add_sep()

ttk.Label(window,text="Verhältnis der Einzelbilder (Format: Breite : Höhe)").pack(pady=1, padx=5)
frame_ratio = tk.Frame(window, background="white")
r_b = ttk.Entry(frame_ratio, font=fontStyle, width=5)
r_h = ttk.Entry(frame_ratio, font=fontStyle,width= 5)
r_b.pack(pady=1,side="left")
ttk.Label(frame_ratio, text=":").pack(pady=1, padx=5,side="left")
r_h.pack(pady=1,side="left")
frame_ratio.pack()
add_sep()

ttk.Label(window,text="Ordner mit den Einzelbildern").pack(pady=1)
ttk.Button(window, text = "Ordner auswählen", command = Button_Ordner_clicked).pack(pady=1)
direct = ttk.Entry(window, font=fontStyle)
direct.pack(pady=1, padx=20, fill='x')
add_sep()

ttk.Button(window, text="Gesamtbild erzeugen", command = Button_clicked).pack(pady=5)
add_sep()

ttk.Button(window, text="Hilfe", command = Button_hilfe_clicked).pack(pady=5)

#Startet das Fenster
window.mainloop()