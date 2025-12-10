

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
    def trace_sliding(x, y, xlabel, ylabel, window=100):
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

# ajouter des titres
# expliquer concept de la sliding window + image/dessin


## Régression locale loess  ###########################################################################################################


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess


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
    # Fonction utilitaire : graphique + régression locale LOESS
    # ---------------------------------------------------------
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
                "Année", "Déplacement Nord (cm)", frac=0.03)

    trace_loess(df["Decimal_YR"], df["East(m)"]*100,
                "Année", "Déplacement Est (cm)", frac=0.03)

    trace_loess(df["Decimal_YR"], df["Vert(m)"]*100,
                "Année", "Déplacement Vertical (cm)", frac=0.03)


# Appel
fonction(r"H:\projet programmation\Stations\7ODM.series")


## régression loess + détéction sauts + ligne vertes ####################################################################################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess


# ------------------------------------------------------------
# Détection automatique des sauts (offsets)
# ------------------------------------------------------------
def detect_offsets(x, y, frac=0.03, k=2):
    """
    x : axe du temps (Decimal Years)
    y : données (cm)
    frac : fraction LOESS (0.02 – 0.05 recommandé)
    k : seuil de détection (sigma multiples)
    """

    # Tendance LOESS
    trend = lowess(y, x, frac=frac, return_sorted=False)

    # Résidus
    res = y - trend

    # Bruit (sigma)
    sigma = np.std(res)

    # Fenêtre adaptative (1.5% de la série)
    window = max(10, int(len(x) * 0.015))

    rough_jumps = []

    # Comparaison avant/après dans une fenêtre glissante
    for i in range(window, len(res)-window):
        mean_before = np.mean(res[i-window:i])
        mean_after = np.mean(res[i:i+window])

        if abs(mean_after - mean_before) > k * sigma:
            rough_jumps.append(x[i])

    # Nettoyage : regrouper détections proches
    final_jumps = []
    for j in rough_jumps:
        if not final_jumps or abs(j - final_jumps[-1]) > 0.05:
            final_jumps.append(j)

    return final_jumps


# ------------------------------------------------------------
# Tracé LOESS + sauts détectés
# ------------------------------------------------------------
def trace_loess_with_offsets(x, y, xlabel, ylabel, frac=0.03):
    plt.figure(figsize=(10, 5))

    # Points bruts
    plt.plot(x, y, '+', alpha=0.4, label="Données")

    # LOESS
    loess_curve = lowess(y, x, frac=frac, return_sorted=False)
    plt.plot(x, loess_curve, 'r-', linewidth=2, label=f"LOESS (frac={frac})")

    # Sauts
    offsets = detect_offsets(x, y, frac=frac)

    for idx, year in enumerate(offsets):
        plt.axvline(year, color="limegreen", linewidth=1.5,
                    label="Saut détecté" if idx == 0 else "")

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.show()


# ------------------------------------------------------------
# Script principal
# ------------------------------------------------------------
def analyser_station(fichier):
    # Lecture du fichier
    df = pd.read_csv(
        fichier,
        sep=r"\s+",
        comment="#",
        header=None,
        engine="python"
    )

    # Entêtes adaptées à TON fichier
    df.columns = [
        "Decimal_YR","East(m)","North(m)","Vert(m)",
        "col5","col6","col7","col8","col9","col10",
        "Time_J2000(s)","Annee","Mois","Jour","Heure","Minute","Seconde"
    ]

    # Extraction + conversion en cm
    x = df["Decimal_YR"]
    north = df["North(m)"] * 100
    east  = df["East(m)"]  * 100
    vert  = df["Vert(m)"]  * 100

    # ---- Graphiques ----
    trace_loess_with_offsets(x, north, "Année", "Déplacement Nord (cm)")
    trace_loess_with_offsets(x, east,  "Année", "Déplacement Est (cm)")
    trace_loess_with_offsets(x, vert,  "Année", "Déplacement Vertical (cm)")


# ------------------------------------------------------------
# Appel
# ------------------------------------------------------------
if __name__ == "__main__":
    analyser_station(r"H:\projet programmation\Stations\7ODM.series")


## graphe avec loess + détection saut et gap de donnée ##############################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess


# ------------------------------------------------------------
# Détection automatique des sauts
# ------------------------------------------------------------
def detect_offsets(x, y, frac=0.05, k=2):
    trend = lowess(y, x, frac=frac, return_sorted=False)
    res = y - trend
    sigma = np.std(res)

    window = max(10, int(len(x) * 0.015))
    rough_jumps = []

    for i in range(window, len(res)-window):
        mean_before = np.mean(res[i-window:i])
        mean_after = np.mean(res[i:i+window])

        if abs(mean_after - mean_before) > k * sigma:
            rough_jumps.append(x[i])

    final_jumps = []
    for j in rough_jumps:
        # éviter des détections trop proches
        if not final_jumps or abs(j - final_jumps[-1]) > 0.05:
            final_jumps.append(j)

    return final_jumps


# ------------------------------------------------------------
# Détection des gaps (trous dans les données)
# ------------------------------------------------------------
def detect_gaps(x, threshold_days=30):
    """
    x : Decimal year
    threshold_days : seuil pour considérer un trou dans les données
    """
    gaps = []
    for i in range(1, len(x)):
        dt = (x.iloc[i] - x.iloc[i-1]) * 365  # approx en jours
        if dt > threshold_days:
            gaps.append(x.iloc[i])
    return gaps


# ------------------------------------------------------------
# Segmentation selon sauts + gaps
# ------------------------------------------------------------
def segment_series(x, y, jumps, gaps):
    cut_points = sorted(jumps + gaps)
    segments = []

    start_idx = 0
    for cp in cut_points:
        idx = np.searchsorted(x, cp)
        if idx > start_idx:
            segments.append((x.iloc[start_idx:idx], y.iloc[start_idx:idx]))
        start_idx = idx

    # dernier segment
    if start_idx < len(x):
        segments.append((x.iloc[start_idx:], y.iloc[start_idx:]))

    return segments


# ------------------------------------------------------------
# Tracé LOESS segmenté + points + sauts + gaps
# ------------------------------------------------------------
def trace_loess_segmented(x, y, xlabel, ylabel, frac=0.03):
    plt.figure(figsize=(10, 5))

    # scatter brut
    plt.plot(x, y, '+', alpha=0.4, label="Données")

    # détecter sauts
    jumps = detect_offsets(x, y, frac=frac)
    for idx, j in enumerate(jumps):
        plt.axvline(j, color="limegreen", linewidth=1.5,
                    label="Saut détecté" if idx == 0 else "")

    # détecter les gaps
    gaps = detect_gaps(x)
    for idx, g in enumerate(gaps):
        plt.axvline(g, color="orange", linewidth=1.5, linestyle="--",
                    label="Gap de données" if idx == 0 else "")

    # segmentation
    segments = segment_series(x, y, jumps, gaps)

    # LOESS par segment
    for xs, ys in segments:
        if len(xs) < 10:  # trop petit pour LOESS
            continue
        lo = lowess(ys, xs, frac=frac, return_sorted=False)
        plt.plot(xs, lo, 'r-', linewidth=2)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.show()


# ------------------------------------------------------------
# PROGRAMME PRINCIPAL
# ------------------------------------------------------------
def analyser_station(fichier):
    # Lecture du fichier
    df = pd.read_csv(
        fichier,
        sep=r"\s+",
        comment="#",
        header=None,
        engine="python"
    )

    # Entêtes adaptées à TON fichier
    df.columns = [
        "Decimal_YR","East(m)","North(m)","Vert(m)",
        "col5","col6","col7","col8","col9","col10",
        "Time_J2000(s)","Annee","Mois","Jour","Heure","Minute","Seconde"
    ]

    # Extraction + conversion en cm
    x = df["Decimal_YR"]
    north = df["North(m)"] * 100
    east  = df["East(m)"]  * 100
    vert  = df["Vert(m)"]  * 100

    # Graphiques
    trace_loess_segmented(x, north, "Année", "Déplacement Nord (cm)")
    trace_loess_segmented(x, east,  "Année", "Déplacement Est (cm)")
    trace_loess_segmented(x, vert,  "Année", "Déplacement Vertical (cm)")


# ------------------------------------------------------------
# Exécuter
# ------------------------------------------------------------
if __name__ == "__main__":
    analyser_station(r"H:\projet programmation\Stations\7ODM.series")





def etape3_main(result):
    print("Exécution de l'étape 3...")
    # Exemple : display of the result
    print("Maximum is " + str(result) + ".")

