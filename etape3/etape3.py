## téléchargement des fichiers 

import os
import requests


def telechargement():
    BASE_URL = "https://sideshow.jpl.nasa.gov/pub/JPL_GPS_Timeseries/repro2018a/post/point/"
    OUT_DIR = "stations"
    os.makedirs(OUT_DIR, exist_ok=True)
    
    print("Téléchargement de la liste des stations...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
    }
    
    # Ignore warnings SSL
    requests.packages.urllib3.disable_warnings()
    
    page = requests.get(BASE_URL, headers=headers, verify=False)
    text = page.text
    
    print("\n--- APERÇU DE LA PAGE REÇUE (normalement on doit voir des <a href=...>) ---")
    print(text[:500])
    print("--------------------------------\n")
    
    # Extraction simple
    links = []
    for line in text.splitlines():
        line = line.strip()
        if ".series" in line and "href" in line:
            start = line.find('href="') + 6
            end = line.find('"', start)
            filename = line[start:end]
            if filename.endswith(".series"):
                links.append(filename)
    
    print(f"{len(links)} fichiers trouvés.")
    
    for filename in links:
        print("Téléchargement :", filename)
        url = BASE_URL + filename
        r = requests.get(url, headers=headers, verify=False)
        with open(os.path.join(OUT_DIR, filename), "wb") as f:
            f.write(r.content)
    
    print("\nTerminé !")
    
telechar = False

if telechar == True :
    telechargement()
    

## graphiques avec sliding window ########################################################################################

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
    def trace_sliding(x, y, xlabel, ylabel, window=150):
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

option = True
if option == True :
    fonction(r"H:\projet programmation\Stations\7ODM.series")


# expliquer concept de la sliding window + image/dessin


## Régression locale loess  ###########################################################################################################


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess


def graphes(station):
    #nom_station = station
    fichier=f"H:\projet programmation\Stations\{station}.series"
    
    df = pd.read_csv(fichier, 
                     sep=r"\s+",
                     comment="#",
                     header=None,
                     engine="python")

    df.columns = ["Decimal_YR","East(m)","North(m)","Vert(m)","col5","col6",
                  "col7","col8","col9","col10","Time past J2000(s)",
                  "Annee","Mois","Jour","Heure","Minute","Seconde"]

    # Fonction utilitaire : graphique + régression locale LOESS

    def trace_loess(x, y, xlabel, ylabel, frac=0.05):
        """
        frac = pourcentage de données utilisées dans chaque fenêtre locale
              0.01 → très peu lissé
              0.05 → lissage moyen
              0.10 → lissage fort
        """

        plt.figure(figsize=(10,5))

        # Données brutes
        plt.plot(x, y, '+', alpha=0.4, label="Données")

        # --- Régression locale LOESS / LOWESS ---
        loess_result = lowess(y, x, frac=frac, return_sorted=False)

        plt.plot(x, loess_result, 'r-', linewidth=2, 
                 label=f"LOESS (frac={frac})")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(True)
        plt.show()

    # -------- Graphiques --------
    trace_loess(df["Decimal_YR"], df["North(m)"]*100,
                "Année", "Déplacement Nord (cm)", frac=0.02)
    trace_loess(df["Decimal_YR"], df["East(m)"]*100,
                "Année", "Déplacement Est (cm)", frac=0.02)
    trace_loess(df["Decimal_YR"], df["Vert(m)"]*100,
                "Année", "Déplacement Vertical (cm)", frac=0.02)

# Appel
graphes("7ODM")




def etape3_main(result):
    print("Exécution de l'étape 3...")
    # Exemple : display of the result
    print("Maximum is " + str(result) + ".")

