import tkinter as tk

from vue.vue_principale import VueApplication
from modele.graphe import Graphe, Sommet, construire_graphe_grille
from controleur.controleur import ControleurApplication


def main():
    root = tk.Tk()
    root.title("Visualisation de plus court chemin")
    root.geometry("1400x900")

    # View
    vue = VueApplication(root)

    # Model
    graphe = construire_graphe_grille(
        vue.nb_lignes,
        vue.nb_colonnes
    )

    # Controller (glue)
    controleur = ControleurApplication(vue, graphe)

    root.mainloop()


if __name__ == "__main__":
    main()
