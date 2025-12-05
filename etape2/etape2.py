import
import math as m
import matplotlib.pyplot as plt

lat1=-0.209536
long1=0.640302
lat2=-0.005106
long2= 0.003700
tps1=41045400.00
tps2=816479850.00
# Programme 1 projet : afficher la flèche et le point pour une station donnée 

#calcul de la vitesse en adaptant la distance parcourut à la surface sphérique de la Terre


def vitesse (lat1,lat2,long1,long2,tps1,tps2):
    lat1,lat2,long1,long2=m.radians(lat1),m.radians(lat2),m.radians(long1),m.radians(long2)
    R=6371000
    dlat=R*(lat2-lat1)
    dlong=R*m.cos(lat1)*(long2-long1)
    v=(m.sqrt(dlong**2+dlat**2))/(tps2-tps1)
    return v,dlat,dlong

# positionner le point de la station et la flèche


plt.figure(figsize=(6, 6)) #le graph
plt.scatter(long1, lat1, color='red', label='Station GPS') #le point

k=0.05 #♣coeff d'échelle à ajuster

v,dlat,dlong=vitesse(lat1,lat2,long1,long2,tps1,tps2)

arrow_dlong = dlong *v*k

arrow_dlat = dlat *v*k

plt.arrow(long1,lat1,arrow_dlong,arrow_dlat,head_width=0.02,head_length=0.03,length_includes_head=True,color='red')

plt.xlabel("Longitude (°)")
plt.ylabel("Latitude (°)")
plt.title("Position GPS sur le plan Latitude = f(Longitude)")
plt.legend()
plt.grid(True)
plt.show()



def etape2_main(data):
    print("Exécution de l'étape 2...")
    # Exemple : traitement de la donnée
    result = max(data)
    return result

#Modèle 3 D code 

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import csv


# # Création d'un tableau de 100 points entre -4*pi et 4*pi 
# #ils veulent tracer une sorte de spirale à partir d'une sorte d'équation
# theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
# z = np.linspace(-2, 2, 100)  # Création du tableau de l'axe z entre -2 et 2
# r = z**2 + 1
# x = r * np.sin(theta)  # Création du tableau de l'axe x
# y = r * np.cos(theta)  # Création du tableau de l'axe y

#réccupération des données et lecture du fichier
def lectureMesures(nomFich):
# Lecture d'un fichier
    f = open(nomFich)
# Format csv
    fcsv = csv.reader(f, delimiter=';')
# Récupération des entêtes
    for E in fcsv:
        break
# Récupération de la matrice des données quantitatives
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
    
    
        
    # for a in x :
    #     a=a.replace(",", ".")
    #     a=float(a)
        
    # for b in y :
    #     b=b.replace(",", ".")
    #     b=float(b)
        
    # for c in z :
    #     c=c.replace(",", ".")
    #     c=float(c)
        
    return x, y, z

        
#     #     L = []
#     #     m = len(ligne)
#     #     for i in range(m):
#     #         L.append(ligne[i])
#     #     Q.append(ligne[m-1])
#     #     LL.append(L)
#     # #M = np.array(LL, dtype='int')
#     # #Q = np.array(Q)
# # Fermeture du fichier
#     f.close()


# #pour nous ce sera plutôt les tableaux de données réccuprés par le premier sous-groupe
# x=[0.640316,0.640806,0.644217,0.645285,0.638222,0.638222,0.638477,0.637248] #longitude
# y=[-0.209482,-0.207993,-0.208426,-0.200717,-0.204820,-0.204820,-0.201947,-0.205605] #latitude
# z=[0.005802,0.008184 ,-0.010232,0.007881,0.019003,0.019003,0.042073 ,0.040877] #altitude

x,y,z=lectureMesures('ODMgogogo.csv')
facteur=1



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot(x, y, [r*facteur for r in z], label='Courbe')

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z (exagérée)")

plt.tight_layout()
plt.show()