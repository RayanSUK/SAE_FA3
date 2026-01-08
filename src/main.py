import tkinter as tk

from vue.vue_principale import VueApplication
from modele.graphe import Graphe, Sommet
from controleur.controleur import ControleurApplication


def main():
    root = tk.Tk()
    root.title("Visualisation de plus court chemin")
    root.geometry("1400x900")

    # View
    vue = VueApplication(root)

    # Model
    graphe = Graphe.creer_graphe_parties(
        vue.nb_colonnes,
        vue.nb_lignes,
    )

    # Controller (glue)
    controleur = ControleurApplication(vue, graphe)

    root.mainloop()


if __name__ == "__main__":
    main()
