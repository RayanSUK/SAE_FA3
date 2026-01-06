from src.vue.vue_principale import VueApplication
from src.modele.graphe import Graphe, Couleur


class ControleurApplication:
    def __init__(self, root):
        # Graphe minimal
        self.graphe = Graphe(sommets={}, voisins={})
        self.vue = VueApplication(root)
        self.lier_evenements()

    def lier_evenements(self):
        v = self.vue

        # Sélection du type de sommet
        v.tuile_noir.bind("<Button-1>", self.clic_case_noire)
        v.tuile_blanc.bind("<Button-1>", self.clic_case_blanche)
        v.tuile_bleu.bind("<Button-1>", self.clic_case_bleue)
        v.tuile_vert.bind("<Button-1>", self.clic_case_verte)
        v.tuile_jaune.bind("<Button-1>", self.clic_case_jaune)


    def clic_case_noire(self, event):
        pass

    def clic_case_blanche(self, event):
        pass

    def clic_case_bleue(self, event):
        pass

    def clic_case_verte(self, event):
        pass

    def clic_case_jaune(self, event):
        pass

