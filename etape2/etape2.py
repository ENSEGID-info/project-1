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

