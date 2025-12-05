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
entree = Entry(fenetre, textvariable=value, width=30)
entree.pack()

#fonction qui récupère le pts gps rentré par l'utilisateur et lance les fonctions qui vont faire les graphs et les cartes 
def tracer():
    texte = value.get()      # on récupère ce que l’utilisateur a écrit
    print("graph", texte)  # A REMPLACER  par les fonctions qui tracent les graph
    ## ajoute comment mettre les graph dans les fenêtres
    
# bouton
bouton=Button(fenetre, text="Tracer", command=tracer)
bouton.pack()


#PANEDWINDOW conteneur qui peut contenir autant de panneaux que nécessaire disposé horizontalement ou verticalement.
p = PanedWindow(fenetre, orient=HORIZONTAL)
p.pack(side=TOP, expand=Y, fill=BOTH, pady=10, padx=2)
p.add(Label(p, text='graph, déplacement en fonction de x', anchor=CENTER, relief=GROOVE) )
p.add(Label(p, text='graph, déplacement en fonction de y', anchor=CENTER, relief=GROOVE) )
p.add(Label(p, text='graph, déplacement en fonction de z', anchor=CENTER, relief=GROOVE) )
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
 
Label(l, text="la carte 2D").pack()

l = LabelFrame(fenetre, text="carte 3D", padx=20, pady=20)
l.pack(fill="both", expand="yes")
 
Label(l, text="la carte 3D").pack()


##fin du pgm, affiche la fenêtre finale
fenetre.mainloop()