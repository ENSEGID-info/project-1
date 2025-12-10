###Modèle 3D code 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import rasterio
from pyproj import Transformer


def modele3D():
    df = pd.read_csv(
        "M:/projet/programation/7ODM.txt",
        comment='#',
        sep="\s+",
        names=["Decimal_YY","East","North","Vert","col5","col6","col7","col8","col9","Time"]
    ) #Lecture du fichier
    
    x,y,z=df["East"],df["North"],df["Vert"] #récupération des données utiles : longitude, latitude et altitude  

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(x, y, z, label='Courbe') 

    #nomme les axes
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Altitude")
    
    plt.title("Représentation 3D du déplacement d'une station dans le temps")

    plt.tight_layout()
    plt.show() #affiche le graphe 3D 
   
"""
pour faire tourner le graphique dans spyder : Tools -> Preferences -> IPython console -> Graphics -> Backend -> Qt5
"""


###Carte 2D
# ---------------- CONFIG ----------------
raster_path = r"C:/Users/PCOMET~1/AppData/Local/Temp/7zO46F67846/viz.SRTMGL3_color-relief.tif"

# Points en Californie (EPSG:4326)
df_input = pd.DataFrame({
    "lon":[ -122.4194, -118.2437, -121.4944],
    "lat":[37.7749, 34.0522, 38.5816],
    "dE": [50, -100, 80],
    "dN": [30, 60, -40]
})

DE_DN_IN_PIXELS = False
SHOW_REAL_SCALE = False
USER_AMPLIFICATION = 0.1


# ---------------- Helpers ----------------

def reproj_points(lons, lats, dst_crs):
    """ lon/lat -> projection du raster """
    t = Transformer.from_crs("EPSG:4326", dst_crs, always_xy=True)
    xs, ys = t.transform(lons, lats)
    return np.array(xs), np.array(ys)

def xy_to_pixel(inv_affine, xs, ys):
    """ Coordonnées projetées -> indices pixels float """
    cols, rows = [], []
    for x, y in zip(xs, ys):
        col, row = inv_affine * (x, y)
        cols.append(col)
        rows.append(row)
    return np.array(cols), np.array(rows)


def trace(img, amplification, df_plot):
    """Affiche le vecteur résultant."""
    sum_dx = df_plot["dx_px_f"].sum()
    sum_dy = df_plot["dy_px_f"].sum()

    start_col = df_plot["col_f"].mean()
    start_row = df_plot["row_f"].mean()

    plt.figure(figsize=(10, 10))
    plt.imshow(img, cmap="gray", origin="upper")

    plt.quiver(
        [start_col],
        [start_row],
        [sum_dx * amplification],
        [sum_dy * amplification],
        angles='xy',
        scale_units='xy',
        scale=1,
        color='red',
        width=0.01
    )

    plt.scatter([start_col], [start_row], s=60, color='cyan', marker='x')
    plt.gca().invert_yaxis()
    plt.title(f"Vecteur résultant amplifié x{amplification:.2f}")
    plt.show()


# ---------------- Main ----------------

df = df_input.copy()

with rasterio.open(raster_path) as src:
    img = src.read(1)
    raster_crs = src.crs
    aff = src.transform
    inv_aff = ~aff
    bounds = src.bounds

# Reprojection vers le CRS du raster
xs, ys = reproj_points(df["lon"].values, df["lat"].values, raster_crs)
df["x_proj"], df["y_proj"] = xs, ys

# Conversion en pixels
df["col_f"], df["row_f"] = xy_to_pixel(inv_aff, xs, ys)

# Vérification emprise
in_bounds = (
    (df["x_proj"] >= bounds.left) &
    (df["x_proj"] <= bounds.right) &
    (df["y_proj"] >= bounds.bottom) &
    (df["y_proj"] <= bounds.top)
)

print(f"Points dans l'emprise : {in_bounds.sum()} / {len(df)}")
if in_bounds.sum() == 0:
    raise RuntimeError("Les points ne sont pas dans l'emprise du raster !")


# ---------- Calcul des extrémités ----------
if DE_DN_IN_PIXELS:
    df["col_end_f"] = df["col_f"] + df["dE"]
    df["row_end_f"] = df["row_f"] - df["dN"]
else:
    df["x_end"] = df["x_proj"] + df["dE"]
    df["y_end"] = df["y_proj"] + df["dN"]
    df["col_end_f"], df["row_end_f"] = xy_to_pixel(inv_aff, df["x_end"], df["y_end"])

# Deltas pixels
df["dx_px_f"] = df["col_end_f"] - df["col_f"]
df["dy_px_f"] = df["row_end_f"] - df["row_f"]

# -------------- scaling --------------
lengths = np.hypot(df["dx_px_f"], df["dy_px_f"])
median_len = np.median(lengths)

if SHOW_REAL_SCALE or median_len <= 0:
    display_scale = 1.0
else:
    display_scale = max(1.0, 20.0 / median_len)

amplification = display_scale * USER_AMPLIFICATION
print("Amplification totale = ", amplification)

# ---- Plot final ----
trace(img, amplification, df)

print("\nScript nettoyé terminé.")