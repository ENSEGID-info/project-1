import pandas as pd # pour les tableaux
import matplotlib.pyplot as plt # graphiques
import tkinter # pour les interfaces graphiques utilisateurs
import requests
import io


##
def fonction(fichier):
    df = pd.read_csv(fichier, 
                     sep=r"\s+",
                     comment="#",     # ignore les lignes commençant par #
                     header=None,     # pas d'en-têtes dans le fichier
                     engine="python") # indispensable pour espaces irréguliers
    # transforme le fichier texte en dataframe
    
    df.columns = ["Decimal_YR","East(m)","North(m)","Vert(m)","col5","col6","col7","col8","col9","col10","Time past J2000(s)","Annee","Mois","Jour","Heure","Minute","Seconde"]
    print(df)
    # renomme les colonnes utiles 
    north = df["North(m)"]
    print(north)
    
    # graphique déplacement Nord
    plt.plot(df["Decimal_YR"], df["North(m)"]*100, '+')
    plt.xlabel("Année")
    plt.ylabel("Déplacement Nord (cm)")
    plt.show()
    
    # graphique déplacement Est
    plt.plot(df["Decimal_YR"], df["East(m)"]*100, '+')
    plt.xlabel("Année")
    plt.ylabel("Déplacement Est (cm)")
    plt.show()
    
    # Graphique déplacement Hauteur
    plt.plot(df["Decimal_YR"], df["Vert(m)"]*100, '+')
    plt.xlabel("Année")
    plt.ylabel("Déplacement Vertical (cm)")
    plt.show()


fonction(r"H:\projet programmation\Stations\7ODM.series")


##

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def fonction(fichier):
    df = pd.read_csv(fichier, 
                     sep=r"\s+",
                     comment="#",
                     header=None,
                     engine="python")

    df.columns = ["Decimal_YR","East(m)","North(m)","Vert(m)","col5","col6",
                  "col7","col8","col9","col10","Time past J2000(s)",
                  "Annee","Mois","Jour","Heure","Minute","Seconde"]

    # ---------------------------------------------------------
    # Fonction utilitaire : graphique + sliding window moyenne
    # ---------------------------------------------------------
    def trace_sliding(x, y, xlabel, ylabel, window=200):
        plt.figure()

        # Données brutes
        plt.plot(x, y, '+', alpha=0.4, label="Données")

        # --- Sliding window (moyenne mobile) ---
        y_smooth = np.convolve(y, np.ones(window)/window, mode='same')

        plt.plot(x, y_smooth, 'r-', linewidth=2, 
                 label=f"Moyenne mobile ({window} points)")

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(True)
        plt.show()

    # -------- Graphiques --------
    trace_sliding(df["Decimal_YR"], df["North(m)"]*100,
                  "Année", "Déplacement Nord (cm)")

    trace_sliding(df["Decimal_YR"], df["East(m)"]*100,
                  "Année", "Déplacement Est (cm)")

    trace_sliding(df["Decimal_YR"], df["Vert(m)"]*100,
                  "Année", "Déplacement Vertical (cm)")

# Appel
fonction(r"H:\projet programmation\Stations\7ODM.series")















def etape3_main(result):
    print("Exécution de l'étape 3...")
    # Exemple : display of the result
    print("Maximum is " + str(result) + ".")

