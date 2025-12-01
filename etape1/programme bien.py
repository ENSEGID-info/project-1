# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from tkinter import *

#ouvre une fenêtre
fenetre = Tk()

#affiche du texte
label = Label(fenetre, text="Rentrez le nom du point gps")
label.pack() #permet de le faire apparaître

# entrée
value = StringVar() 
value.set("texte par défaut")
entree = Entry(fenetre, textvariable="string", width=30)
entree.pack()

# bouton
bouton=Button(fenetre, text="Tracer", command=print('graph'))
bouton.pack()

##fin du pgm, affiche la fenêtre finale
fenetre.mainloop()