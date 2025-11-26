import pandas as pd # pour les tableaux
import matplotlib.pyplot as plt # graphiques
import tkinter # pour les interfaces graphiques utilisateurs
import requests
import io


##

df = pd.read_csv(r"H:\projet programmation\7ODM.txt", 
                 sep=r"\s+",
                 comment="#",     # ignore les lignes commençant par #
                 header=None,     # pas d'en-têtes dans le fichier
                 engine="python") # indispensable pour espaces irréguliers


df.columns = ["Decimal_YR","East(m)","North(m)","Vert(m)","col5","col6","col7","col8","col9","col10","Time past J2000(s)","Annee","Mois","Jour","Heure","Minute","Seconde"]
print(df)
north = df["North(m)"]
print(north)

# graphique déplacement Nord
plt.plot(df["Decimal_YR"], df["North(m)"]*100)
plt.xlabel("Année")
plt.ylabel("Déplacement Nord (cm)")
plt.show()

# graphique déplacement Est
plt.plot(df["Decimal_YR"], df["East(m)"]*100)
plt.xlabel("Année")
plt.ylabel("Déplacement Est (cm)")
plt.show()

# Graphique déplacement Hauteur
plt.plot(df["Decimal_YR"], df["Vert(m)"]*100)
plt.xlabel("Année")
plt.ylabel("Déplacement Vertical (cm)")
plt.show()



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

