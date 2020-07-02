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

import math
import numpy as np
from os import listdir
from PIL import Image


def get_error(i_w,i_h,n_w,n_h,d_w,d_h):
    """
    Gibt den Fehler zurück, sprich den freibleibenden
    Bereich des Ausgabeformats.
    Parameter
    ---------
    i_w :
        Breite eines Bildes
    i_h :
        Höhe eines Bildes
    n_w :
        Anzahl der Spalten
    n_h :
        Anzahl der Zeilen
    d_w :
        Breite des Ausgabeformats
    d_h :
        Höhe des Ausgabeformats
    Ausgabe [Delta_w, Delta_h]
    ---
    Delta_w :
        Freibleibender Platz in der Breite
    Delta_h :
        Freibleibender Platz in der Höhe
    """
    Delta_w = d_w - i_w*n_w
    Delta_h = d_h - i_h*n_h
    return [round(Delta_w,2),round(Delta_h,2)]

def solve_problem(d_w, d_h, n, r):
    """
    Gibt die optimale Bildanordnung anhand der gegebenen Parameter aus.
    Parameter
    ---------
    d_w :
        Breite des Ausgabeformats
    d_h :
        Höhe des Ausgabeformats
    n :
        Anzahl der Bilder
    r :
        Verhältnis der Bilder
    Ausgabe [n_w, n_h, i_w, i_h, Delta_w, Delta_h]
    ---
    n_w :
        Anzahl der Spalten
    n_h :
        Anzahl der Zeilen
    i_w :
        Breite eines Bildes
    i_h :
        Höhe eines Bildes
    Delta_w :
        Freibleibender Platz in der Breite
    Delta_h :
        Freibleibender Platz in der Höhe
    """
    n_h = math.sqrt(d_h*n*r/d_w)
    n_h = round(n_h)
    n_w = math.ceil(n/n_h)
    i_w = d_w/n_w
    i_h = i_w/r
    if i_h*n_h > d_h: #Falls das Bild zu groß für das Ausgabeformat werden würde, wird die Höhe eines Bildes angepasst.
        i_h = d_h/n_h
        i_w = i_h * r
    [Delta_w, Delta_h] = get_error(i_w,i_h,n_w,n_h,d_w,d_h)
    return [n_w,n_h, round(i_w,2), round(i_h,2), Delta_w, Delta_h]

def solve_problem_optimized(d_w,d_h,n,r):
    """
    Löst das Problem zweimal mit zueinander vertauschten Breiten und Höhen. 
    Die Lösung mit dem kleineren Fehler wird ausgegeben. 
    Parameter
    ---------
    d_w :
        Breite des Ausgabeformats
    d_h :
        Höhe des Ausgabeformats
    n :
        Anzahl der Bilder
    r :
        Verhältnis der Bilder
    Ausgabe [n_w, n_h, i_w, i_h, Delta_w, Delta_h]
    ---
    n_w :
        Anzahl der Spalten
    n_h :
        Anzahl der Zeilen
    i_w :
        Breite eines Bildes
    i_h :
        Höhe eines Bildes
    Delta_w :
        Freibleibender Platz in der Breite
    Delta_h :
        Freibleibender Platz in der Höhe
    """
    result_wh = solve_problem(d_w,d_h,n,r)
    result_hw = solve_problem(d_h,d_w,n,1/r)
    if result_wh[4] * result_wh[4] <= result_hw[4] * result_hw[4]:
        [n_w, n_h, i_w, i_h, Delta_w, Delta_h] = result_wh
    else:
        [n_h, n_w, i_h, i_w, Delta_h, Delta_w] = result_wh #Aufpassen! Hier ist jetzt alles gedreht, da die Variablen oben vertauscht wurden.

def program(d_w, d_h, r, folder, saving_location):
    """
    Routine, die die gegebenen Bilder einliest, anordnet und als Gesamtbild speichert.
    Parameter
    ---------
    d_w :
        Breite des Ausgabeformats
    d_h :
        Höhe des Ausgabeformats
    r :
        Verhältnis der Bilder
    folder :
        Pfad des Ordners in dem sich die Bilder befinden
    saving_location :
        Pfad in den das fertige Gesamtbild gespeichert werden soll
    """
    bilderliste = listdir(folder) #Alle Bilder im Ordner einlesen
    [n_w, n_h, i_w, i_h, Delta_w, Delta_h] = solve_problem(d_w,d_h,len(bilderliste),r)
    pixelbilderliste = []
    #Nacheinander werden alle Bilder eingelesen und in die pixelbilderliste gespeichert
    for name in bilderliste:
        im = Image.open(folder +"/"+name)
        im.putalpha(255) #Für jpg Dateien wird ein alphakanal hinzugefügt
        im = im.resize((int(i_w),int(i_h))) #Bild wird in die richtige Größe skaliert
        arrim = np.asarray(im) #Bild wird in zweidimensionalen Array umgewandelt
        pixelbilderliste.append(arrim)
    #Hier sollte lieber die Anzahl der Bilderliste verwendet werden, statt n_h um Fehler zu vermeiden
    zeilen = [np.concatenate(pixelbilderliste[i*n_w:(i+1)*n_w], axis = 1) for i in range(math.ceil(len(bilderliste)/n_w))] 
    #Die letzte Zeile wird in der Breite zu einer vollen Zeile ergänzt
    freespacel = math.ceil((n_w * int(i_w) - np.array(zeilen[-1]).shape[1])/2)
    freespacer = math.floor((n_w * int(i_w) - np.array(zeilen[-1]).shape[1])/2)
    #Links und Rechts von den Bildern der letzten Zeile wird weißer Hintergrund hinzugefügt
    temp = np.append(zeilen[-1], np.zeros((int(i_h),freespacel,4)), axis=1) 
    temp = np.append(np.zeros((int(i_h),freespacer,4)), temp, axis=1)
    zeilen[-1] = temp.astype(np.int)
    square = np.concatenate(zeilen, axis = 0)
    finalim = Image.fromarray(square.astype(np.uint8)) #Umwandlung in Bildformat
    finalim.save(saving_location)


