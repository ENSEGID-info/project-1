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


##

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------------
#  Lecture du fichier
# ------------------------------------------------------------------
df = pd.read_csv(
    "M:/projet/programation/7ODM.txt",
    comment='#',
    sep="\s+",
    names=["Decimal_YY","East","North","Vert","col5","col6","col7","col8","col9","Time"]
)

# Conversion en années décimales
t = df["Decimal_YY"]

# ------------------------------------------------------------------
#  Fonction pour tracer un graphique individuel
# ------------------------------------------------------------------
def plot_component(ax, t, data, ylabel):
    # nuage de points
    ax.scatter(t, data, s=6, color="steelblue", alpha=0.7)

    # régression linéaire
    p = np.polyfit(t, data, 1)
    trend = np.polyval(p, t)
    ax.plot(t, trend, color="red", linewidth=2, label=f"Tendance : {p[0]*10:.3f} cm/an")

    # style
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.set_ylabel(ylabel)
    ax.legend(loc="upper left", fontsize=9)


# ------------------------------------------------------------------
#  Figure complète
# ------------------------------------------------------------------
fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
fig.suptitle("Séries temporelles – Station 7ODM", fontsize=16, fontweight='bold')

# graphique Nord
plot_component(axes[0], t, df["North"]*100, "Déplacement Nord (cm)")

# graphique Est
plot_component(axes[1], t, df["East"]*100, "Déplacement Est (cm)")

# graphique Vertical
plot_component(axes[2], t, df["Vert"]*100, "Déplacement Vertical (cm)")
axes[2].set_xlabel("Année")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()


































































def etape3_main(result):
    print("Exécution de l'étape 3...")
    # Exemple : display of the result
    print("Maximum is " + str(result) + ".")

