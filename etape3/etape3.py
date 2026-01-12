## téléchargement des fichiers 

import os
import requests


def telechargement():
    BASE_URL = "https://sideshow.jpl.nasa.gov/pub/JPL_GPS_Timeseries/repro2018a/post/point/" # URL de l'emplacement des fichiers en ligne
    OUT_DIR = "stations"  # dossier où télécharger les fichiers
    os.makedirs(OUT_DIR, exist_ok=True)  # crée le dossier stations s’il n’existe pas
    
    print("Téléchargement de la liste des stations...")  # affiche un message pour dire que le téléchargement est en cours
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
    }   # Spyder se fait passer pour un utilisateur Mozilla pour contourner certains problèmes d'accès
    
    # Ignore warnings SSL
    requests.packages.urllib3.disable_warnings()  # télécharge la page web
    page = requests.get(BASE_URL, headers=headers, verify=False)  # ignore les problèmes de certificat
    text = page.text  # met le contenu HTML de la page sous forme de texte
    
    # Extraction des noms des fichiers de la forme XXXX.series dans une liste
    links = []
    for line in text.splitlines():  # On lit la page ligne par ligne
        line = line.strip()
        if ".series" in line and "href" in line:  # On garde seulement les lignes qui contiennent : ".series" et "href" (=lien HTML)
            start = line.find('href="') + 6  # définit le début du nom de fichier
            end = line.find('"', start)      # définit la fin du nom de fichier
            filename = line[start:end]       # donne le nom des futurs fichiers 
            if filename.endswith(".series"): # ajoute le nom du fichier à la liste links
                links.append(filename)

    print(f"{len(links)} fichiers trouvés.")  # affiche le nombre de fichiers trouvés
    
    # télécharge les fichiers de la liste précédemment extraite
    for filename in links:
        print("Téléchargement :", filename)
        url = BASE_URL + filename              # construit l'url complète
        r = requests.get(url, headers=headers, verify=False) 
        with open(os.path.join(OUT_DIR, filename), "wb") as f:  # écriture du fichier sur le disque de l'ordinateur
            f.write(r.content)
    
    print("\nTerminé !")
    
# option pour exécuter ou non la fonction précédente
telechar = False
if telechar == True :
    telechargement()
    

## graphiques avec sliding window ########################################################################################

# import des bibliothèques
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def fonction(fichier):
    df = pd.read_csv(fichier,   
                     sep=r"\s+",
                     comment="#",
                     header=None,
                     engine="python")  # lit le fichier texte et le convertit en dataframe

    df.columns = ["Decimal_YR","East(m)","North(m)","Vert(m)","col5","col6",
                  "col7","col8","col9","col10","Time past J2000(s)",
                  "Annee","Mois","Jour","Heure","Minute","Seconde"]  # on renomme le nom des colonnes utiles


    # Fonction utilitaire : graphique + sliding window moyenne
    def trace_sliding(x, y, xlabel, ylabel, window=150):
        plt.figure()
        # Données brutes et paramètres de courbe
        plt.plot(x, y, '+', alpha=0.4, label="Données") 
        
        # Sliding window (moyenne mobile) 
        y_smooth = np.convolve(y, np.ones(window)/window, mode='same')
        
        plt.plot(x, y_smooth, 'r-', linewidth=2, 
                 label=f"Moyenne mobile ({window} points)")  # ajoute la sliding window au graphique
        # affichage des titres des axes, de la légende, de la grille et affichage du graphique
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(True)
        plt.show()

    # Traçage des graphiques avec la fonction précédente
    trace_sliding(df["Decimal_YR"], df["North(m)"]*100,
                  "Année", "Déplacement Nord (cm)")

    trace_sliding(df["Decimal_YR"], df["East(m)"]*100,
                  "Année", "Déplacement Est (cm)")

    trace_sliding(df["Decimal_YR"], df["Vert(m)"]*100,
                  "Année", "Déplacement Vertical (cm)")

# Appel avec option (ici non appelé car choix d'utiliser la régression LOESS ci-dessous)
option = True
if option == True :
    fonction(r"H:\projet programmation\Stations\7ODM.series")


## Régression locale LOESS  ########################################################################################################

# import des bibliothèques
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess  
    # Importe la fonction LOWESS / LOESS utile aux série temporelles GNSS

def graphes(station):
    fichier=f"H:\projet programmation\Stations\{station}.series"  # emplacement du fichier de la station demandée
    df = pd.read_csv(fichier, 
                     sep=r"\s+",
                     comment="#",
                     header=None,
                     engine="python")  # lecture du fichier texte et conversion en dataframe

    df.columns = ["Decimal_YR","East(m)","North(m)","Vert(m)","col5","col6",
                  "col7","col8","col9","col10","Time past J2000(s)",
                  "Annee","Mois","Jour","Heure","Minute","Seconde"]  # on renomme le nom des colonnes utiles

# Fonction utilitaire : graphique + régression locale LOESS
    def trace_loess(x, y, xlabel, ylabel, frac=0.05):
        """
        frac = pourcentage de données utilisées dans chaque fenêtre locale
              0.01 → très peu lissé
              0.05 → lissage moyen
              0.10 → lissage fort
        """
        plt.figure(figsize=(10,5))  # taille de la figure
        plt.plot(x, y, '+', alpha=0.4, label="Données")  # Données brutes et paramètres de courbe

        loess_result = lowess(y, x, frac=frac, return_sorted=False)  # calul de la régression locale LOESS / LOWESS

        plt.plot(x, loess_result, 'r-', linewidth=2, 
                 label=f"LOESS (frac={frac})")        # tracé de la courbe LOESS
        # Habillage du graphique
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(True)
        plt.show()

    # Traçage des graphiques
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

