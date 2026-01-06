from src.modele.graphe import ModeleGraphe
from src.vue.vue_principale import VueApplication


class ControleurApplication:
    def __init__(self, root):
        self.modele = ModeleGraphe()
        self.vue = VueApplication(root)
        self.lier_evenements()

    def lier_evenements(self):
        v = self.vue

        # Clics sur les cases couleurs
        v.tuile_noir.bind("<Button-1>", self.clic_case_noire)
        v.tuile_blanc.bind("<Button-1>", self.clic_case_blanche)
        v.tuile_bleu.bind("<Button-1>", self.clic_case_bleue)
        v.tuile_vert.bind("<Button-1>", self.clic_case_verte)
        v.tuile_jaune.bind("<Button-1>", self.clic_case_jaune)

        # Sélection d'algorithme
        v.liste_algo.bind("<<ComboboxSelected>>", self.quand_algo_change)

        # Boutons
        v.bouton_lancer_algo.config(command=self.lancer_algo)
        v.bouton_effacer_resultat.config(command=self.effacer_resultat)
        v.bouton_effacer_tout.config(command=self.effacer_tout)

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

    def quand_algo_change(self, event):
        pass

    def lancer_algo(self):
        pass

    def effacer_resultat(self):
        pass

    def effacer_tout(self):
        pass

