from modele.graphe import Couleur


class ControleurApplication:
    def __init__(self, vue, graphe):
        self.vue = vue
        self.graphe = graphe
        self.couleur_active = Couleur.BLANC
        print("<<< CONTROLEUR INITIALISE SANS PROBLEME >>>")

        self.lier_evenements()

    # ---------------- Utilitaires ----------------
    def sommet_id(self, lig, col):
        return lig * self.vue.nb_colonnes + col

    # ---------------- Liaisons événements ----------------
    def lier_evenements(self):
        v = self.vue

        v.tuile_noir.bind("<Button-1>", lambda e: self.set_couleur(None))  # bloque
        v.tuile_blanc.bind("<Button-1>", lambda e: self.set_couleur(Couleur.BLANC))
        v.tuile_bleu.bind("<Button-1>", lambda e: self.set_couleur(Couleur.BLEU))
        v.tuile_vert.bind("<Button-1>", lambda e: self.set_couleur(Couleur.VERT))
        v.tuile_jaune.bind("<Button-1>", lambda e: self.set_couleur(Couleur.JAUNE))

        v.canvas_graphe.bind("<Button-1>", self.clic_grille)

        # --- Lecture / Animation (placeholders) ---
        v.bouton_reculer_etape.configure(command=self.reculer_etape)
        v.bouton_lancer_pause.configure(command=self.lancer_ou_pause)
        v.bouton_avancer_etape.configure(command=self.avancer_etape)


    # Actions de lecture
    def reculer_etape(self):
        pass
    def lancer_ou_pause(self):
        pass
    def avancer_etape(self):
        pass

    def set_couleur(self, couleur):
        self.couleur_active = couleur

    # ---------------- Actions ----------------
    def clic_grille(self, event):
        print("En train de cliquer avec le controleur!")
        col = event.x // self.vue.taille_case
        lig = event.y // self.vue.taille_case

        if not (0 <= lig < self.vue.nb_lignes and 0 <= col < self.vue.nb_colonnes):
            return

        id_sommet = self.sommet_id(lig, col)
        sommet = self.graphe.obtenir_sommet(id_sommet)

        # MAJ MODELE
        if self.couleur_active is None:  # si tu veux un clic "bloqué"
            sommet.bloque = not sommet.bloque
        else:
            sommet.bloque = False
            sommet.cout = self.couleur_active

        # MAJ VUE via la méthode de la vue
        print("Sommet cliqué!", sommet.bloque)
        self.vue.maj_case(lig, col, sommet)





