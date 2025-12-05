# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 16:06:36 2025

@author: pcometducass
"""

import rasterio
from rasterio.transform import Affine
from rasterio.warp import transform as rio_transform
from pyproj import Transformer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# ---------------- CONFIG ----------------
raster_path = r"C:/Users/pcometducass/Downloads/CA_Adelaida_287792_1948_24000_geo.tif"

# DataFrame d'exemple : remplace par tes vraies coordonnées (lon,lat en degrés EPSG:4326)
df_input = pd.DataFrame({
    "lon": [2.3522, 2.3530, 2.3510],
    "lat": [48.8566, 48.8570, 48.8550],
    # dE,dN en METRES par défaut; si tu as des pixels, active DE_DN_IN_PIXELS
    "dE": [0.02, -0.01, 0.03],
    "dN": [0.01, 0.02, -0.02]
})

# Si tes dE/dN sont déjà en PIXELS, mets ceci sur True
DE_DN_IN_PIXELS = False

# Forcer affichage en vraies unités ? False = on amplifie pour visibilité si vecteurs très petits
SHOW_REAL_SCALE = False

# Facteur optionnel supplémentaire d'amplification pour rendre le vecteur résultant bien visible
USER_AMPLIFICATION = 75  # met >1 pour agrandir encore

# ---------------- Helpers ----------------
def try_make_transformer(src_crs, dst_crs):
    try:
        return Transformer.from_crs(src_crs, dst_crs, always_xy=True)
    except Exception as e:
        print("Warning: pyproj.Transformer failed:", e)
        return None

def reproj_points_with_fallback(lons, lats, dst_crs):
    t = try_make_transformer("EPSG:4326", dst_crs)
    if t is not None:
        xs, ys = t.transform(lons, lats)
        return np.array(xs), np.array(ys)
    else:
        xs, ys = rio_transform("EPSG:4326", dst_crs, lons, lats)
        return np.array(xs), np.array(ys)

def xy_to_float_pixel_coords(inv_affine, xs, ys):
    """Returns (cols_f, rows_f) floats from projected x,y using inverse affine."""
    cols = []
    rows = []
    for x, y in zip(xs, ys):
        col, row = inv_affine * (x, y)
        cols.append(col)
        rows.append(row)
    return np.array(cols, dtype=float), np.array(rows, dtype=float)

def colsrows_to_xy(affine, cols, rows):
    """From pixel col,row floats -> projected x,y (using forward affine)"""
    xs = []
    ys = []
    for c, r in zip(cols, rows):
        x, y = affine * (c, r)
        xs.append(x)
        ys.append(y)
    return np.array(xs, dtype=float), np.array(ys, dtype=float)

# ---------------- Main ----------------
df = df_input.copy()

with rasterio.open(raster_path) as src:
    img = src.read(1)
    raster_crs = src.crs
    aff = src.transform
    inv_aff = ~aff
    height, width = img.shape
    bounds = src.bounds
    # pixel size approx (aff.a is x scale, aff.e is y scale usually negative for north-up)
    px_w = aff.a
    px_h = abs(aff.e)

print("Raster CRS:", raster_crs)
print("Taille (cols x rows):", width, "x", height)
print("Pixel size (m) approx:", px_w, px_h)
print("Bounds (proj coords):", bounds)
print("")

# Reprojection lon/lat -> coords projetées du raster
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

# Diagnostic points in bounds (projected coords)
in_x = (df["x_proj"] >= bounds.left) & (df["x_proj"] <= bounds.right)
in_y = (df["y_proj"] >= bounds.bottom) & (df["y_proj"] <= bounds.top)
in_bounds_proj = in_x & in_y
print("Points dans l'emprise projetée (via coords projetées):", in_bounds_proj.sum(), "/", len(df))
print(df[["lon","lat","x_proj","y_proj","col_f","row_f"]])
print("")

# Si aucun point dans emprise -> créer jeu demo centré sur raster (comme dans ton script original)
if in_bounds_proj.sum() == 0:
    print("Aucun point d'entrée dans l'emprise du raster. Création d'un jeu de démonstration centré sur la raster.")
    cx = (bounds.left + bounds.right) / 2.0
    cy = (bounds.bottom + bounds.top) / 2.0
    demo = pd.DataFrame({
        "x_proj": [cx, cx + 50.0, cx - 80.0],
        "y_proj": [cy, cy + 30.0, cy - 60.0],
        "dE": [20.0, -40.0, 80.0],
        "dN": [10.0, 25.0, -30.0]
    })
    demo["col_f"], demo["row_f"] = xy_to_float_pixel_coords(inv_aff, demo["x_proj"].values, demo["y_proj"].values)
    # back-transform for lon/lat (optionnel)
    t_back = try_make_transformer(raster_crs, "EPSG:4326")
    if t_back is not None:
        demo_lon, demo_lat = t_back.transform(demo["x_proj"].values, demo["y_proj"].values)
    else:
        demo_lon, demo_lat = rio_transform(raster_crs, "EPSG:4326", demo["x_proj"].values.tolist(), demo["y_proj"].values.tolist())
    demo["lon"] = demo_lon
    demo["lat"] = demo_lat
    print(demo[["lon","lat","col_f","row_f","dE","dN"]])
    df_plot = demo.copy()
else:
    df_plot = df.copy()

# ---------- Calcul des extrémités ----------
if DE_DN_IN_PIXELS:
    # dE/dN déjà en pixels image coordinates:
    # Convention: +dE -> +col ; +dN -> -row (si dN is "north" positive)
    # Ici on assume que dE is pixels in col direction and dN is pixels in row direction (image), user must ensure convention
    df_plot["col_end_f"] = df_plot["col_f"].values + df_plot["dE"].values
    df_plot["row_end_f"] = df_plot["row_f"].values - df_plot["dN"].values  # minus if dN positive -> move up in image
else:
    # dE/dN en METRES : safer to compute extrémités en coords projetées puis convertir en pixels
    # s'assurer qu'on a x_proj,y_proj
    if "x_proj" not in df_plot.columns or "y_proj" not in df_plot.columns:
        xs, ys = colsrows_to_xy(aff, df_plot["col_f"].values, df_plot["row_f"].values)
        df_plot["x_proj"] = xs
        df_plot["y_proj"] = ys

    # extrémités en coordonnées projetées
    df_plot["x_end"] = df_plot["x_proj"].values + df_plot["dE"].values
    df_plot["y_end"] = df_plot["y_proj"].values + df_plot["dN"].values

    # convertir extrémités projetées -> pixels floats
    df_plot["col_end_f"], df_plot["row_end_f"] = xy_to_float_pixel_coords(inv_aff, df_plot["x_end"].values, df_plot["y_end"].values)

# deltas pixels floats (direction vecteurs en pixels image)
df_plot["dx_px_f"] = df_plot["col_end_f"].values - df_plot["col_f"].values
df_plot["dy_px_f"] = df_plot["row_end_f"].values - df_plot["row_f"].values

print("\nRésumé final pour tracé (cols/rows floats & deltas pixels):")
print(df_plot[["lon","lat","col_f","row_f","col_end_f","row_end_f","dx_px_f","dy_px_f"]])

# ---------------- Scaling for visibility ----------------
lengths_px = np.hypot(df_plot["dx_px_f"].values, df_plot["dy_px_f"].values)
median_len = np.median(lengths_px) if len(lengths_px) > 0 else 0.0

if SHOW_REAL_SCALE:
    display_scale = 1.0
else:
    if median_len <= 0:
        display_scale = 1.0
    else:
        display_scale = max(1.0, 20.0 / median_len)  # make median ~ 20 px for visibility

# combine with user amplification
amplification = display_scale * float(USER_AMPLIFICATION)

print("\nMedian vector length (px):", median_len)
print("Display scale used to amplify arrows:", display_scale)
print("User amplification factor:", USER_AMPLIFICATION)
print("Final amplification applied:", amplification)

# ---------------- Calcul vecteur résultant (somme) ----------------
sum_dx_px = df_plot["dx_px_f"].sum()
sum_dy_px = df_plot["dy_px_f"].sum()

# point de départ: centroïde des points (moyenne des col_f,row_f)
start_col = df_plot["col_f"].mean()
start_row = df_plot["row_f"].mean()

print("\nVecteur résultant en pixels (non amplifié): dx =", sum_dx_px, " dy =", sum_dy_px)
print("Start (col,row):", start_col, start_row)

# ---------------- Plot ----------------
plt.figure(figsize=(10,10))
plt.imshow(img, cmap="gray", origin="upper")

# tracer vecteur résultant (unique)
dx_plot = sum_dx_px * amplification
dy_plot = sum_dy_px * amplification

plt.quiver([start_col], [start_row], [dx_plot], [dy_plot],
           angles='xy', scale_units='xy', scale=1, color='red', width=0.01)

plt.scatter(df_plot["col_f"].values, df_plot["row_f"].values, s=20, color='yellow', label='origines')
# marquer point de départ choisi
plt.scatter([start_col], [start_row], s=60, color='cyan', marker='x', label='start (centroïde)')

plt.gca().invert_yaxis()
plt.legend()
plt.title(f"Vecteur résultant (somme) amplifié x{amplification:.2f}")
plt.show()

print("\nScript terminé.")