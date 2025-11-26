# ===============================
# Projet Informatique
# Structure du programme principal
# ===============================

# Import des modules écrits par les sous-groupes
import etape1
import etape2
import etape3

def main():
    print("=== Début du programme ===")
    
    # Étape 1 – Préparation ou lecture de données
    print("\n--- Étape 1 : Lecture ou préparation ---")
    data = etape1.etape1_main()
    
    # Étape 2 – Traitement ou analyse
    print("\n--- Étape 2 : Traitement principal ---")
    result = etape2.etape2_main(data)
    
    # Étape 3 – Résultats ou affichage final
    print("\n--- Étape 3 : Résultats ou sortie ---")
    etape3.etape3_main(result)
    
    print("\n=== Fin du programme ===")

if __name__ == "__main__":
    main()

import rasterio
from rasterio.plot import show
import numpy as np
import pandas as pd
import math as m
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "lat": [48.8566, 48.857, 48.855],
    "lon": [2.3522, 2.353, 2.351],
    "dE": [0.02, -0.01, 0.03],  
    "dN": [0.01, 0.02, -0.02]
})
raster_path = "C:/Users/pcometducass/Downloads/USGS_DS-424_2.tif"

with rasterio.open(raster_path) as src:
    img = src.read(1)
    transform = src.transform
    crs = src.crs
# Fonction pour transformer lon/lat → pixels
def world_to_pixel(x, y, transform):
    col, row = ~transform * (x, y)
    return col, row

# Ajouter colonnes px/py dans le DataFrame
df["px"], df["py"] = zip(*df.apply(lambda r: world_to_pixel(r["lon"], r["lat"], transform), axis=1))
plt.figure(figsize=(10, 10))

# Affichage du raster
plt.imshow(img, cmap="gray", origin="upper")

# Affichage vecteurs vitesse
plt.quiver(
    df["px"], df["py"],          # positions pixel
    df["dE"], -df["dN"],         # vecteurs (y inversé car image)
    angles='xy', scale_units='xy', scale=1, color="red"
)

plt.title("Carte raster + vecteurs vitesses")
plt.xlabel("px")
plt.ylabel("py")
plt.show()

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
