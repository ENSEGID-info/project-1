###Modèle 3D code 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import csv

def lectureMesures(nomFich):
    f = open(nomFich) #lecture du fichier
    fcsv = csv.reader(f, delimiter=';') #format csv
    for E in fcsv:
        break
    x = []
    y = []
    z = []
    for ligne in fcsv:
        x.append(ligne[0])
        y.append(ligne[1])
        z.append(ligne[2])
    x = [float(a.replace(',', '.')) for a in x]
    y = [float(b.replace(',', '.')) for b in y]
    z = [float(c.replace(',', '.')) for c in z]  
    return x, y, z

x,y,z=lectureMesures('ODMgogogo.csv')
facteur=100

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot(x, y, [r*facteur for r in z], label='Courbe') #exagération sur z (multiplie tout par un facteur r)

#nomme les axes
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z (exagérée)")

plt.tight_layout()
plt.show() #affiche le graphe