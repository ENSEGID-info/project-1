# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 16:06:36 2025

@author: pcometducass
"""

import rasterio
from rasterio.transform import Affine
from rasterio.warp import transform as rio_transform
from pyproj import Transformer, CRS, Geod
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math as m
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# ---------------- CONFIG ----------------
raster_path = r"C:/Users/pcometducass/Downloads/CA_Adelaida_287792_1948_24000_geo.tif"

# DataFrame d'exemple : remplace par tes vraies coordonnées
# IMPORTANT: lon,lat en DEGRES (EPSG:4326). dE,dN ici supposés en METRES.
df_input = pd.DataFrame({
    "lon": [2.3522, 2.3530, 2.3510],   # remplacer par des lon californiens si disponibles
    "lat": [48.8566, 48.8570, 48.8550],
    "dE": [0.02, -0.01, 0.03],         # en mètres (exemple / remplacer)
    "dN": [0.01, 0.02, -0.02]
})

# Si tes dE/dN sont déjà en PIXELS, mets ceci sur True et le script sautera la conversion mètres->pixels
DE_DN_IN_PIXELS = False

# Forcer affichage en vraies unités ? False = on amplifie pour visibilité si vecteurs très petits
SHOW_REAL_SCALE = False

# ---------------- Helpers ----------------
def try_make_transformer(src_crs, dst_crs):
    """Try to create a pyproj Transformer; fallback to rasterio.warp.transform if PROJ broken."""
    try:
        return Transformer.from_crs(src_crs, dst_crs, always_xy=True)
    except Exception as e:
        print("Warning: pyproj.Transformer failed:", e)
        print(" -> Le script va utiliser rasterio.warp.transform pour reprojeter point par point (moins rapide).")
        return None

def reproj_points_with_fallback(lons, lats, dst_crs):
    """Return xs, ys in dst_crs from lon,lat. Uses Transformer if available, else rasterio.warp.transform."""
    t = try_make_transformer("EPSG:4326", dst_crs)
    if t is not None:
        xs, ys = t.transform(lons, lats)
        return np.array(xs), np.array(ys)
    else:
        # fallback: rasterio.warp.transform expects sequences and crs objects/strings
        try:
            xs, ys = rio_transform("EPSG:4326", dst_crs, lons, lats)
            return np.array(xs), np.array(ys)
        except Exception as e:
            raise RuntimeError("Impossible de reprojeter les points avec aucune méthode disponible: " + str(e))

def xy_to_float_pixel_coords(inv_affine, xs, ys):
    """Donne col_f, row_f floats à partir de coords projetées x,y et inverse affine."""
    cols = []
    rows = []
    for x, y in zip(xs, ys):
        col, row = inv_affine * (x, y)   # floats
        cols.append(col)
        rows.append(row)
    return np.array(cols, dtype=float), np.array(rows, dtype=float)

# ---------------- Main ----------------
df = df_input.copy()

with rasterio.open(raster_path) as src:
    img = src.read(1)
    raster_crs = src.crs
    aff = src.transform
    inv_aff = ~aff
    height, width = img.shape
    bounds = src.bounds
    px_w = aff.a
    px_h = abs(aff.e)

print("Raster CRS:", raster_crs)
print("Taille (cols x rows):", width, "x", height)
print("Pixel size (m):", px_w, px_h)
print("Bounds (proj coords):", bounds)
print("")

# Reproj des origines lon/lat -> x_proj,y_proj (CRS raster)
lons = df["lon"].values.tolist()
lats = df["lat"].values.tolist()
try:
    xs_proj, ys_proj = reproj_points_with_fallback(lons, lats, raster_crs)
except Exception as e:
    raise RuntimeError("Échec de reprojection initiale : " + str(e))

df["x_proj"] = xs_proj
df["y_proj"] = ys_proj

# Positions pixel float (origines)
df["col_f"], df["row_f"] = xy_to_float_pixel_coords(inv_aff, df["x_proj"].values, df["y_proj"].values)

# Diagnostic: points dans l'emprise reproductible en coords projetées ?
in_x = (df["x_proj"] >= bounds.left) & (df["x_proj"] <= bounds.right)
in_y = (df["y_proj"] >= bounds.bottom) & (df["y_proj"] <= bounds.top)
in_bounds_proj = in_x & in_y
print("Points dans l'emprise projetée (via coords projetées):", in_bounds_proj.sum(), "/", len(df))
print(df[["lon","lat","x_proj","y_proj","col_f","row_f"]])
print("")

# Si aucun point dans emprise -> créer points démo au centre pour vérifier affichage
if in_bounds_proj.sum() == 0:
    print("Aucun point d'entrée dans l'emprise du raster. Probable: tes lon/lat ne sont pas en Californie.")
    cx = (bounds.left + bounds.right) / 2.0
    cy = (bounds.bottom + bounds.top) / 2.0
    # convert center to lon/lat pour info
    try:
        t_back = try_make_transformer(raster_crs, "EPSG:4326")
        if t_back is not None:
            center_lon, center_lat = t_back.transform(cx, cy)
        else:
            center_lon, center_lat = rio_transform(raster_crs, "EPSG:4326", [cx],[cy])
            center_lon = center_lon[0]; center_lat = center_lat[0]
    except Exception:
        center_lon, center_lat = (np.nan, np.nan)
    print("Centre raster (proj):", (cx, cy))
    print("Centre raster (lon,lat):", (center_lon, center_lat))
    # demo points: 3 points around center in projected coords; dE/dN example in meters
    demo = pd.DataFrame({
        "x_proj": [cx, cx + 50.0, cx - 80.0],   # metres offset
        "y_proj": [cy, cy + 30.0, cy - 60.0],
        "dE": [20.0, -40.0, 80.0],             # metres
        "dN": [10.0, 25.0, -30.0]
    })
    demo["col_f"], demo["row_f"] = xy_to_float_pixel_coords(inv_aff, demo["x_proj"].values, demo["y_proj"].values)
    # pour cohérence, on rajoute lon/lat back-transform
    try:
        t_back2 = try_make_transformer(raster_crs, "EPSG:4326")
        if t_back2 is not None:
            lons_demo, lats_demo = t_back2.transform(demo["x_proj"].values, demo["y_proj"].values)
        else:
            lons_demo, lats_demo = rio_transform(raster_crs, "EPSG:4326", demo["x_proj"].values.tolist(), demo["y_proj"].values.tolist())
    except Exception:
        lons_demo = [np.nan]*len(demo); lats_demo = [np.nan]*len(demo)
    demo["lon"] = lons_demo; demo["lat"] = lats_demo
    print("\nJe crée un jeu de démonstration centré sur la raster (3 points) pour vérifier le rendu.")
    print(demo[["lon","lat","col_f","row_f","dE","dN"]])
    # remplacer df_plot par demo
    df_plot = demo.copy()
    # déja en x_proj / y_proj définis
else:
    df_plot = df.copy()

# ---------- Calcul des extrémités ----------
# Si dE/dN en pixels (flag) -> utiliser directement; sinon on convertit METRES -> pixels via px_w/px_h.
if DE_DN_IN_PIXELS:
    df_plot["col_end_f"] = df_plot["col_f"] + df_plot["dE"].values
    df_plot["row_end_f"] = df_plot["row_f"] + df_plot["dN"].values
else:
    # On suppose dE/dN EN METRES : conv en pixels = metres / pixel_size_m
    # ATTENTION: ici on suppose orientation standard: +E -> +x -> col increases ; +N -> +y -> row decreases in image coordinates
    # Nous calculons en coordonnées projetées puis convertissons en pixels float pour précision.
    # Si df_plot contient x_proj,y_proj use them; sinon compute from col_f,row_f
    if "x_proj" not in df_plot.columns:
        # calculer x_proj,y_proj à partir des pixels floats
        df_plot["x_proj"] = [aff * (c, r)[0] for c, r in zip(df_plot["col_f"], df_plot["row_f"])]
        # Above line is placeholder; safer to compute properly:
        # But since we had x_proj for original df, in demo it is already present.
    # compute endpoints in projected meters
    df_plot["x_end"] = df_plot["x_proj"].values + df_plot["dE"].values
    df_plot["y_end"] = df_plot["y_proj"].values + df_plot["dN"].values
    # convert to pixel floats
    df_plot["col_end_f"], df_plot["row_end_f"] = xy_to_float_pixel_coords(inv_aff, df_plot["x_end"].values, df_plot["y_end"].values)

# deltas pixels floats
df_plot["dx_px_f"] = df_plot["col_end_f"].values - df_plot["col_f"].values
df_plot["dy_px_f"] = df_plot["row_end_f"].values - df_plot["row_f"].values

print("\nRésumé final pour tracé (cols/rows floats & deltas pixels):")
print(df_plot[["lon","lat","col_f","row_f","col_end_f","row_end_f","dx_px_f","dy_px_f"]])

# ---------------- Scaling for visibility ----------------
median_len = np.median(np.hypot(df_plot["dx_px_f"].values, df_plot["dy_px_f"].values))
if SHOW_REAL_SCALE:
    display_scale = 1.0
else:
    if median_len <= 0:
        display_scale = 1.0
    else:
        display_scale = max(1.0, 20.0 / median_len)  # make median ~ 20 pixels for visibility

print("\nMedian vector length (px):", median_len)
print("Display scale used to amplify arrows:", display_scale)
print("Note: si tu veux voir la vraie longueur, définis SHOW_REAL_SCALE=True")

# ---------------- Plot ----------------
plt.figure(figsize=(10,10))
plt.imshow(img, cmap="gray", origin="upper")

valid = np.isfinite(df_plot["col_f"].values)

cols_plot = df_plot["col_f"].values[valid]
rows_plot = df_plot["row_f"].values[valid]

# --- AMPLIFICATION FORCÉE ICI ---
AMPLIFICATION_FORCEE = 100   # ajuste ici !
dx_plot = df_plot["dx_px_f"].values[valid] * AMPLIFICATION_FORCEE
dy_plot = df_plot["dy_px_f"].values[valid] * AMPLIFICATION_FORCEE
# --------------------------------

plt.quiver(cols_plot, rows_plot, dx_plot, dy_plot,
           angles='xy', scale_units='xy', scale=1, color='red', width=0.005)

plt.scatter(cols_plot, rows_plot, s=20, color='yellow')
plt.gca().invert_yaxis()
plt.title(f"Vecteurs amplifiés x{AMPLIFICATION_FORCEE}")
plt.show()

print("\nScript terminé.")