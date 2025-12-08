# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 16:42:10 2025

@author: lbenaissa
"""

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

fenetre = Tk()
fenetre.title("Analyse GPS")
fenetre.geometry("1600x900")

# Couleur globale
BG = "#f5f5f5"          # fond doux
CARD = "white"          # blocs
ACCENT = "#2f6fed"       # bleu scientifique propre
TEXT = "#1a1a1a"

fenetre.configure(bg=BG)

# ---------------------------------------------------------
# STRUCTURE GLOBALE
# ---------------------------------------------------------

main_frame = Frame(fenetre, bg=BG)
main_frame.pack(fill="both", expand=True)

main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=35)
main_frame.grid_rowconfigure(2, weight=65)

main_frame.grid_columnconfigure(0, weight=1)

# ---------------------------------------------------------
# BARRE DE RECHERCHE
# ---------------------------------------------------------

search_frame = Frame(main_frame, bg=BG)
search_frame.grid(row=0, column=0, sticky="nsew", pady=10)

Label(search_frame,
      text="Recherche de point GPS",
      bg=BG,
      fg=TEXT,
      font=("Segoe UI", 14, "bold")
).pack(pady=2)

value = StringVar()

# Style entrée + bouton
entry = Entry(search_frame, textvariable=value, width=35, font=("Segoe UI", 12))
entry.pack(pady=5, ipady=4)

# Bouton stylé
search_btn = Button(
    search_frame,
    text="Tracer",
    command=lambda: afficher_graphs(value.get()),  #print("graph", value.get()) a remplacé par les fonctions du groupe B et C
    bg=ACCENT,
    fg="white",
    activebackground="#2558c7",
    activeforeground="white",
    bd=0,
    padx=10,
    pady=5,
    font=("Segoe UI", 11, "bold")
)
search_btn.pack(pady=5)

# ---------------------------------------------------------
# FONCTION POUR CARDS
# ---------------------------------------------------------

def make_card(parent, title):
    # Frame principale de la carte avec bordure propre
    card = Frame(parent, bg=CARD, highlightbackground=ACCENT, highlightthickness=2)
    card.pack_propagate(False)

    # Label titre en haut
    title_label = Label(card, text=title, bg=CARD, fg=TEXT,
                        font=("Segoe UI", 12, "bold"))
    title_label.pack(side="top", fill="x", pady=(5,10))

    # Frame interne pour contenu
    inner = Frame(card, bg=CARD)
    inner.pack(fill="both", expand=True, padx=10, pady=10)

    return card, inner


# ---------------------------------------------------------
# GRAPHS (HAUT)
# ---------------------------------------------------------

top_frame = Frame(main_frame, bg=BG)
top_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

for i in range(3):
    top_frame.grid_columnconfigure(i, weight=1)
top_frame.grid_rowconfigure(0, weight=1)

graph_x, gx_inner = make_card(top_frame, "Déplacement X")
graph_y, gy_inner = make_card(top_frame, "Déplacement Y")
graph_z, gz_inner = make_card(top_frame, "Déplacement Z")

graph_x.grid(row=0, column=0, sticky="nsew", padx=8)
graph_y.grid(row=0, column=1, sticky="nsew", padx=8)
graph_z.grid(row=0, column=2, sticky="nsew", padx=8)

Label(gx_inner, text="(graph X)", bg=CARD, fg=TEXT).pack()
Label(gy_inner, text="(graph Y)", bg=CARD, fg=TEXT).pack()
Label(gz_inner, text="(graph Z)", bg=CARD, fg=TEXT).pack()

# ---------------------------------------------------------
# CARTES (BAS)
# ---------------------------------------------------------

bottom_frame = Frame(main_frame, bg=BG)
bottom_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

bottom_frame.grid_columnconfigure(0, weight=1)
bottom_frame.grid_columnconfigure(1, weight=1)
bottom_frame.grid_rowconfigure(0, weight=1)

carte2D, c2_inner = make_card(bottom_frame, "Carte 2D")
carte3D, c3_inner = make_card(bottom_frame, "Carte 3D")

carte2D.grid(row=0, column=0, sticky="nsew", padx=8)
carte3D.grid(row=0, column=1, sticky="nsew", padx=8)

Label(c2_inner, text="(affichage futur 2D)", bg=CARD, fg=TEXT).pack()
Label(c3_inner, text="(affichage futur 3D)", bg=CARD, fg=TEXT).pack()

# ---------------------------------------------------------

def afficher_graphs(valeur):
    # Exemple de données pour démonstration
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.tan(x) / 10

    # ---- Sous-fonction pour dessiner un graphique dans une frame ----
    def draw_plot(frame, x, y, title):
        # Effacer ancien contenu
        for widget in frame.winfo_children():
            widget.destroy()

        fig = plt.Figure(figsize=(3.5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x, y)
        ax.set_title(title)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ----- Plots dans les frames du haut -----
    draw_plot(gx_inner, x, y1, "Déplacement X")
    draw_plot(gy_inner, x, y2, "Déplacement Y")
    draw_plot(gz_inner, x, y3, "Déplacement Z")

    # ----- Carte 2D -----
    fig2 = plt.Figure(figsize=(3.5, 3), dpi=100)
    ax2 = fig2.add_subplot(111)
    ax2.scatter(np.sin(x), np.cos(x), c=x, cmap="viridis")
    ax2.set_title("Carte 2D")

    for widget in c2_inner.winfo_children():
        widget.destroy()
    canvas2 = FigureCanvasTkAgg(fig2, master=c2_inner)
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill="both", expand=True)

    # ----- Carte 3D -----
    fig3 = plt.Figure(figsize=(4, 3), dpi=100)
    ax3 = fig3.add_subplot(111, projection='3d')
    ax3.scatter(np.sin(x), np.cos(x), x, c=x, cmap="plasma")
    ax3.set_title("Carte 3D")

    for widget in c3_inner.winfo_children():
        widget.destroy()
    canvas3 = FigureCanvasTkAgg(fig3, master=c3_inner)
    canvas3.draw()
    canvas3.get_tk_widget().pack(fill="both", expand=True)


fenetre.mainloop()