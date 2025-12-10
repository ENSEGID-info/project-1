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
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(x, y, z, label='Courbe') 

    #nomme les axes
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Altitude")
    
    plt.title("Représentation 3D du déplacement d'une station dans le temps")

    plt.tight_layout()
    plt.show() #affiche le graphe 3D 
    