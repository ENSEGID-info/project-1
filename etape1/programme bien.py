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


#PANEDWINDOW conteneur qui peut contenir autant de panneaux que nécessaire disposé horizontalement ou verticalement.
p = PanedWindow(fenetre, orient=HORIZONTAL)
p.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)
p.add(Label(p, text='Volet 1', background='blue', anchor=CENTER))
p.add(Label(p, text='Volet 2', background='white', anchor=CENTER) )
p.add(Label(p, text='Volet 3', background='red', anchor=CENTER) )
p.pack()

fenetre['bg']='white'

# 2 frame = 2 zones conteneurs qui permettent de séparer des éléments, les cartes
Frame1 = Frame(fenetre, borderwidth=2, relief=GROOVE)
Frame1.pack(side=LEFT, padx=30, pady=30)

Frame2 = Frame(fenetre, borderwidth=2, relief=GROOVE)
Frame2.pack(side=LEFT, padx=30, pady=30)


#titre frame
l = LabelFrame(fenetre, text="carte 2D", padx=20, pady=20)
l.pack(fill="both", expand="yes")
 
Label(l, text="A l'intérieure de la frame 2").pack()

l = LabelFrame(fenetre, text="carte 3D", padx=20, pady=20)
l.pack(fill="both", expand="yes")
 
Label(l, text="A l'intérieure de la frame").pack()


##fin du pgm, affiche la fenêtre finale
fenetre.mainloop()