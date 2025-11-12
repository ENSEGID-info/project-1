import pandas as pd # pour les tableaux
import matplotlib.pyplot as plt # graphiques
import tkinter # pour les interfaces graphiques utilisateurs



url_request="sideshow.jpl.nasa.gov/pub/JPL_GPS_Timeseries/repro2018a/post/point/7ODM.series"

def graph_Lat(X,Y_lat):
    plt.plot(X,Y)
    plt.xlabel("Temps")
    plt.ylabel("Latitude")
    plt.title("Latitude en fonction du temps")
    plt.show()

def graph_Long(X,Y_long):
    plt.plot(X,Y_long)
    plt.xlabel("Temps")
    plt.ylabel("Longitude")
    plt.title("Longitude en fonction du temps")
    plt.show()

def graph_Alt(X,Y_alt):
    plt.plot(X,Y_alt)
    plt.xlabel("Temps")
    plt.ylabel("Atitude")
    plt.title("Altitude en fonction du temps")
    plt.show()

































































def etape3_main(result):
    print("Exécution de l'étape 3...")
    # Exemple : display of the result
    print("Maximum is " + str(result) + ".")

