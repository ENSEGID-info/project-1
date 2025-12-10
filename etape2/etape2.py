###Modèle 3D code 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd

def modele3D():
    df = pd.read_csv(
        "M:/projet/programation/7ODM.txt",
        comment='#',
        sep="\s+",
        names=["Decimal_YY","East","North","Vert","col5","col6","col7","col8","col9","Time"]
    ) #Lecture du fichier
    
    x,y,z=df["East"],df["North"],df["Vert"] #récupération des données utiles : longitude, latitude et altitude  

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d') #création de l'espace vide pouvant accueillir le graphique (un carré donc une ligne et une colonne)
    
    ax.plot(x, y, z, label='Courbe') #création du graphique dans l'espace vide

    #nomme les axes
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Altitude")
    
    plt.title("Représentation 3D du déplacement d'une station dans le temps") #donne le titre

    plt.tight_layout()
    plt.show() #affiche le graphe 3D 
    
"""
pour faire tourner le graphique dans spyder : Tools -> Preferences -> IPython console -> Graphics -> Backend -> Qt5
"""