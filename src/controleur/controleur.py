from modele.graphe import Couleur
from vue.vue_principale import VueApplication
from modele.algorithmes import bfs_pas_a_pas, dfs_pas_a_pas, dijkstra_pas_a_pas, bellman_ford_pas_a_pas, \
    chemin_depuis_parents

class ControleurApplication:
    '''
    Contrôleur principal de l'application
    Gère les interactions entre la vue et le modèle (graphe + algorithmes)
    '''
    def __init__(self, vue, graphe):
        self.vue = vue
        self.graphe = graphe
        self.couleur_active = Couleur.BLANC

        self.mode_selection = "normal"  # "normal" | "depart" | "arrivee"

        print("<<< CONTROLEUR INITIALISE SANS PROBLEME >>>")
        self.vue.bouton_lancer_algo.config(command=self.lancer_algorithme)

        self.lier_evenements()
        self.initialiser_depart_arrivee_par_defaut()

        self.iterateur_algo = None
        self.after_id = None

        self.en_pause = True
        self.delai_base_ms = 100  # vitesse de base = ×1 (en ms)
        self.delai_ms = self.delai_base_ms

        # --- Historique des étapes pour reculer/avancer ---
        self.historique_etapes: list[dict] = []
        self.index_etape: int = -1  # -1 => aucune étape affichée encore

        self._maj_progression_interne = False

        self.algo_courant = None

        self._drag_actif = False
        self._drag_last_case = None  # (lig, col)
        self._drag_noir_valeur = None

    # ---------------- Utilitaires ----------------
    def sommet_id(self, lig, col):
        return lig * self.vue.nb_colonnes + col + 1
   
    def initialiser_depart_arrivee_par_defaut(self):     
        '''
        Initialisation du départ et de l'arrivée par défaut
        Départ en haut à gauche (0,0)
        Arrivée en bas à droite (nb_lignes-1, nb_colonnes-1
        '''
        depart = self.sommet_id(0, 0)
        arrivee = self.sommet_id(self.vue.nb_lignes - 1, self.vue.nb_colonnes - 1)

        self.graphe.definir_depart(depart)
        self.graphe.definir_arrivee(arrivee)

        # Affichage dans la vue
        self.vue.afficher_depart_arrivee(self.graphe.depart, self.graphe.arrivee)

    def activer_mode_depart(self):
        self.mode_selection = "depart"

    def activer_mode_arrivee(self):
        self.mode_selection = "arrivee"

    def remettre_points_par_defaut(self):
        self.mode_selection = "normal"
        self.initialiser_depart_arrivee_par_defaut()

    # ---------------- Liaisons événements ----------------
    def lier_evenements(self):
        '''
        Liaisons des événements de la vue aux méthodes du contrôleur
        1. Clic sur les tuiles de couleur pour changer la couleur active
        2. Clic sur la grille pour modifier les sommets (via clic_grille)
        3. Boutons de contrôle (reculer, lancer/pause, avancer)
        4. Boutons de placement départ/arrivée
        5. Boutons d'effacement (résultat / tout)
        6. Boutons de vitesse (×1, ×4, ×8)
        7. Curseur de progression
        8. etc...
        '''
        v = self.vue

        v.tuile_noir.bind("<Button-1>", lambda e: self.set_couleur(None))  # bloque
        v.tuile_blanc.bind("<Button-1>", lambda e: self.set_couleur(Couleur.BLANC))
        v.tuile_bleu.bind("<Button-1>", lambda e: self.set_couleur(Couleur.BLEU))
        v.tuile_vert.bind("<Button-1>", lambda e: self.set_couleur(Couleur.VERT))
        v.tuile_jaune.bind("<Button-1>", lambda e: self.set_couleur(Couleur.JAUNE))

        v.canvas_graphe.bind("<Button-1>", self._mouse_down)
        v.canvas_graphe.bind("<B1-Motion>", self._mouse_drag)
        v.canvas_graphe.bind("<ButtonRelease-1>", self._mouse_up)

        # --- Lecture / Animation (placeholders) ---
        v.bouton_reculer_etape.configure(command=self.reculer_etape)
        v.bouton_lancer_pause.configure(command=self.lancer_ou_pause)
        v.bouton_avancer_etape.configure(command=self.avancer_etape)

        v.bouton_placer_depart.configure(command=self.activer_mode_depart)
        v.bouton_placer_arrivee.configure(command=self.activer_mode_arrivee)
        v.bouton_points_par_defaut.configure(command=self.remettre_points_par_defaut)

        v.bouton_effacer_resultat.configure(command=self.effacer_resultat)
        v.bouton_effacer_tout.configure(command=self.effacer_tout)

        v.bouton_vitesse_05.configure(text="×1", command=lambda: self.set_vitesse(1))
        v.bouton_vitesse_1.configure(text="×4", command=lambda: self.set_vitesse(4))
        v.bouton_vitesse_2.configure(text="×8", command=lambda: self.set_vitesse(8))

        v.curseur_progression.configure(command=self._progression_changee)

    # Actions de lecture
    def reculer_etape(self):
        '''
        Gestion du bouton reculer d'une étape
        On ne recule que si on est en pause (comportement simple)
        1. On enlève le chemin final si jamais il avait été tracé
        2. On décrémente l'index d'étape
        3. On affiche l'étape correspondante via _afficher_etape
        '''
        # On ne recule que si on est en pause (comportement simple)
        if not self.en_pause:
            return

        if not self.historique_etapes:
            return

        if self.index_etape <= 0:
            return

        # On enlève le chemin final si jamais il avait été tracé
        if self.vue.ligne_chemin is not None:
            try:
                self.vue.canvas_graphe.delete(self.vue.ligne_chemin)
            except Exception:
                pass
            self.vue.ligne_chemin = None

        self.index_etape -= 1
        etape = self.historique_etapes[self.index_etape]
        self._afficher_etape(etape)


    def lancer_ou_pause(self):
        '''
        Gestion du bouton lancer/pause
        Si en pause => on lance l'animation automatique
        Si en cours d'animation => on met en pause
        '''
        # Toggle pause/play
        self.en_pause = not self.en_pause
        if not self.en_pause:
            self._tick()
        else:
            if self.after_id is not None:
                try:
                    self.vue.after_cancel(self.after_id)
                except Exception:
                    pass
                self.after_id = None

    
    def avancer_etape(self):
        '''
        Gestion de l'avancement d'une étape en mode pause
        On avance d'une étape dans l'itérateur, ou on rejoue une étape déjà existante
        1. Si on est en pause et qu'on a déjà des étapes "en avance" (après un retour arrière), on les rejoue
        2. Sinon on lit une nouvelle étape depuis l'itérateur  
        '''
        # Un seul pas si on est en pause
        if not self.en_pause:
            return

        if not self.historique_etapes:
            return

        # 1) Si on a des étapes en avance dans l'historique, on peut avancer même si iterateur_algo est None
        if self.index_etape < len(self.historique_etapes) - 1:
            self.index_etape += 1
            etape = self.historique_etapes[self.index_etape]
            self._afficher_etape(etape)
            return

        # 2) Sinon, on ne peut avancer que si l'algorithme n'est pas terminé
        if self.iterateur_algo is None:
            return

        # 3) Lire une nouvelle étape depuis l'itérateur
        try:
            etape = next(self.iterateur_algo)
        except StopIteration:
            self.iterateur_algo = None
            return

        self.historique_etapes.append(etape)
        self.index_etape = len(self.historique_etapes) - 1
        self._afficher_etape(etape)

    def set_couleur(self, couleur):
        self.couleur_active = couleur
        self.mode_selection = "normal"

    
    def clic_grille(self, event):
        '''
        Gestion du clic sur la grille
    
        On détermine la case cliquée, grâce à une conversion des coordinées x,y du clic en ligne/colonne
        Puis on agit en fonction du mode de sélection (normal / départ / arrivée)
    
        1. Mode départ : on définit le sommet cliqué comme le nouveau départ (si pas bloqué et pas arrivée)
        2. Mode arrivée : on définit le sommet cliqué comme la nouvelle arrivée (si pas bloqué et pas départ)
        3. Mode normal : on modifie le sommet cliqué
            - Si couleur_active est None => on inverse bloqué / débloqué
            - Sinon on définit le coût du sommet à la couleur active (et on débloque le sommet) 
        On met ensuite à jour la vue via la méthode maj_case de la vue
        '''

        print("En train de cliquer avec le controleur!")

        col = event.x // self.vue.taille_case
        lig = event.y // self.vue.taille_case

        if not (0 <= lig < self.vue.nb_lignes and 0 <= col < self.vue.nb_colonnes):
            return

        id_sommet = self.sommet_id(lig, col)

        if self.mode_selection == "depart":
            sommet = self.graphe.obtenir_sommet(id_sommet)
            if sommet.bloque:
                return

            # Empêche départ = arrivée
            if id_sommet == self.graphe.arrivee:
                return

            self.graphe.definir_depart(id_sommet)
            self.vue.afficher_depart_arrivee(self.graphe.depart, self.graphe.arrivee)
            return

        if self.mode_selection == "arrivee":
            sommet = self.graphe.obtenir_sommet(id_sommet)
            if sommet.bloque:
                return

            # Empêche arrivée = départ
            if id_sommet == self.graphe.depart:
                return

            self.graphe.definir_arrivee(id_sommet)
            self.vue.afficher_depart_arrivee(self.graphe.depart, self.graphe.arrivee)
            return

        # MODE NORMAL : une seule ligne
        self._appliquer_case(lig, col)

    def lancer_algorithme(self):
        '''
        Gestion du bouton lancer l'algorithme
        1. Récupère l'algorithme sélectionné dans la vue
        2. Stoppe toute animation précédente + reset affichage
        3. Reset historique
        4. Initialise l'itérateur de l'algorithme choisi
        5. Démarre l'animation automatique via _tick
        '''
        algo = self.vue.liste_algo.get()
        self.algo_courant = algo
        print(f"[CONTROLEUR] Lancement de l'algorithme : {algo}")

        # stop animation précédente + reset affichage
        self.effacer_resultat()

        # Logs
        self.vue.logs_clear()
        self.vue.logs_append(f"Algo: {algo}")
        self.vue.logs_append(f"Départ: {self.graphe.depart}  Arrivée: {self.graphe.arrivee}")


        # reset historique
        self.historique_etapes = []
        self.index_etape = -1

        if algo == "DFS":
            self.iterateur_algo = dfs_pas_a_pas(self.graphe)
        elif algo == "BFS":
            self.iterateur_algo = bfs_pas_a_pas(self.graphe)
        elif algo == "Dijkstra":
            self.iterateur_algo = dijkstra_pas_a_pas(self.graphe)
        elif algo == "Bellman-Ford":
            self.iterateur_algo = bellman_ford_pas_a_pas(self.graphe)
        else:
            self.iterateur_algo = None
            return

        # on démarre en lecture auto
        self.en_pause = False
        self._tick()

    def effacer_resultat(self):
        '''
        Docstring for effacer_resultat
        
        :param self: Description
        :return: Description
        1. On stoppe l'animation en cours (after_cancel)
        2. On réinitialise l'itérateur + met en pause
        3. On efface le résultat dans la vue (effacer_resultat)
        4. On réinitialise l'historique des étapes + index
        5. On remet la progression à 0
        '''
        if self.after_id is not None:
            try:
                self.vue.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None

        self.iterateur_algo = None
        self.en_pause = True
        self.vue.effacer_resultat()

        self.historique_etapes = []
        self.index_etape = -1

        self.vue.curseur_progression.set(0)

    def effacer_tout(self):
        '''
        Gestion du bouton effacer tout
        1. On stoppe l'animation en cours (effacer_resultat)
        2. On réinitialise le modèle (débloquer tous les sommets + coûts BLANC)
        3. On réinitialise la vue (remettre toutes les cases en blanc + contour normal)
        4. On remet le départ/arrivée par défaut
        5. On remet la progression à 0
        '''
        # Stop animation
        self.effacer_resultat()

        # Reset modèle : débloquer + remettre coûts BLANC
        for sommet in self.graphe.sommets.values():
            sommet.bloque = False
            sommet.cout = Couleur.BLANC

        # Reset vue : remettre toutes les cases en blanc + contour normal
        for lig in range(self.vue.nb_lignes):
            for col in range(self.vue.nb_colonnes):
                rect = self.vue.rectangles_cases[lig][col]
                self.vue.canvas_graphe.itemconfig(rect, fill="#ffffff", outline="#d0d0d0", width=1)

        # Remettre départ/arrivée par défaut
        self.remettre_points_par_defaut()
        self.vue.curseur_progression.set(0)

    def _tick(self):
        '''
        Gestion de l'animation automatique
        1. Si en pause ou itérateur None, alors on ne fait rien
        2. Si on a reculé puis relancé play, on rejoue d'abord l'historique
        3. Sinon, on consomme une nouvelle étape depuis l'itérateur (-1)
        4. On affiche l'étape via _afficher_etape
        5. Si on atteint l'arrivée, on trace le chemin final et on stoppe l'animation
        6. Sinon, on reprogramme un tick après delai_ms.
        '''
        if self.en_pause or self.iterateur_algo is None:
            return

        # Si on a reculé puis relancé play, on rejoue d'abord l'historique
        if self.index_etape < len(self.historique_etapes) - 1:
            self.index_etape += 1
            etape = self.historique_etapes[self.index_etape]
        else:
            # Sinon, on consomme une nouvelle étape
            try:
                etape = next(self.iterateur_algo)
            except StopIteration:
                self._log_fin_execution(None)
                self.iterateur_algo = None
                self.after_id = None
                self.en_pause = True
                return

            self.historique_etapes.append(etape)
            self.index_etape = len(self.historique_etapes) - 1

        self._afficher_etape(etape)

        # Stop sur goal seulement pour certains algos
        stop_on_goal = self.algo_courant in {"DFS", "BFS", "Dijkstra"}

        # Pour Bellman-Ford, on a parfois "destination" et on l'affiche comme courant
        courant_visuel = etape.get("destination", etape.get("courant"))

        if stop_on_goal and courant_visuel == self.graphe.arrivee:
            parents = etape.get("parents")
            if isinstance(parents, dict):
                chemin = chemin_depuis_parents(parents, self.graphe.arrivee)
                if chemin and chemin[0] == self.graphe.depart:
                    self.vue.afficher_chemin(chemin)

            self._log_fin_execution(chemin)

            self.iterateur_algo = None
            self.after_id = None
            self.en_pause = True
            return

        self.after_id = self.vue.after(self.delai_ms, self._tick)

    def _afficher_etape(self, etape: dict):
        '''
        Affiche une étape dans la vue. 
        Utilisé par l'animation automatique et les boutons de contrôle manuel.
        Met aussi à jour la progression.
        Paramètre : etape (dict) avec clés "ouverts", "fermes", "courant, "distances", etc.
        1. Récupère les données de l'étape
        2. Appelle la méthode afficher_etape de la vue
        3. Met à jour la progression via _mettre_a_jour_progression
        '''
        ouverts = etape.get("ouverts", set())
        fermes = etape.get("fermes", set())
        courant = etape.get("courant", None)
        distances = etape.get("distances", None)

        # Bellman-Ford : on peut afficher la destination comme "courant" visuel
        if "destination" in etape:
            courant = etape.get("destination", courant)

        # sécu types
        try:
            ouverts = set(ouverts)
        except Exception:
            ouverts = set()

        try:
            fermes = set(fermes)
        except Exception:
            fermes = set()

        self.vue.afficher_etape(ouverts, fermes, courant, distances)
        self._mettre_a_jour_progression()

    def set_vitesse(self, multiplicateur: int):
        '''
        Gestion du changement de vitesse
        Change la vitesse de l'animation.
        Plus le multiplicateur est grand, plus c'est rapide
        1. On calcule le nouveau delai_ms en fonction du multiplicateur
        2. Si l'animation est en cours, on annule le tick en cours et on relance un tick immédiatement
        3. Le prochain tick sera programmé avec le nouveau delai_ms
        '''
        if multiplicateur <= 0:
            return

        self.delai_ms = max(1, int(self.delai_base_ms / multiplicateur))
        print(f"[CONTROLEUR] Vitesse: x{multiplicateur} (delai={self.delai_ms}ms)")

        # si l'animation est en cours, on applique la nouvelle vitesse tout de suite
        if not self.en_pause and self.iterateur_algo is not None:
            if self.after_id is not None:
                try:
                    self.vue.after_cancel(self.after_id)
                except Exception:
                    pass
                self.after_id = None

            # Relance un tick immédiatement (il va reprogrammer le prochain avec le nouveau delai_ms)
            self._tick()

    def _mettre_a_jour_progression(self):
        '''
        Met à jour la barre de progression en fonction de l'index d'étape actuel
        1. Calcule le total d'étapes dans l'historique
        2. Configure la barre de progression pour aller de 0 à total-1
        3. Met la barre à l'index d'étape actuel
        '''
        total = len(self.historique_etapes)
        if total <= 0:
            self._maj_progression_interne = True
            self.vue.curseur_progression.configure(from_=0, to=0)
            self.vue.curseur_progression.set(0)
            self._maj_progression_interne = False
            return

        self._maj_progression_interne = True
        self.vue.curseur_progression.configure(from_=0, to=total - 1)
        self.vue.curseur_progression.set(self.index_etape)
        self._maj_progression_interne = False

    def _progression_changee(self, valeur):
        '''
        Gestion du changement de la barre de progression par l'utilisateur
        L'utilisateur a bougé la barre => on saute à l'étape correspondante.
        Simple : seulement en pause.
        1. Si la mise à jour est interne (via _mettre_a_jour_progression), on ignore
        2. Si on n'est pas en pause, on ignore (évite de casser l'animation)
        3. Si on n'a pas d'itérateur et pas d'historique, on ignore
        4. On convertit la valeur en entier (index cible)
        5. Si la cible est dans l'historique, on affiche directement l'étape correspondante
        6. Sinon, on calcule des étapes jusqu'à atteindre la cible (sans animation)
        7. On affiche l'étape la plus proche atteinte
        '''

        if self._maj_progression_interne:
            return

        if not self.en_pause:
            return  # on évite de casser l'animation

        if self.iterateur_algo is None and not self.historique_etapes:
            return

        try:
            cible = int(float(valeur))
        except Exception:
            return

        # Clamp (sécurité)
        if cible < 0:
            cible = 0

        # Si la cible est déjà dans l'historique => affichage direct
        if cible <= len(self.historique_etapes) - 1:
            self.index_etape = cible
            etape = self.historique_etapes[self.index_etape]

            # Si un chemin final était tracé, on l'enlève (sinon incohérent)
            if self.vue.ligne_chemin is not None:
                try:
                    self.vue.canvas_graphe.delete(self.vue.ligne_chemin)
                except Exception:
                    pass
                self.vue.ligne_chemin = None

            self._afficher_etape(etape)
            return

        # Sinon, on doit calculer des étapes jusqu'à atteindre la cible
        # (sans animation, juste en consommant l'itérateur)
        while len(self.historique_etapes) - 1 < cible:
            if self.iterateur_algo is None:
                break
            try:
                etape = next(self.iterateur_algo)
            except StopIteration:
                self.iterateur_algo = None
                break

            self.historique_etapes.append(etape)
            self.index_etape = len(self.historique_etapes) - 1

            stop_on_goal = self.algo_courant in {"DFS", "BFS", "Dijkstra"}
            courant_visuel = etape.get("destination", etape.get("courant"))

            # Stop goal seulement si l'algo le permet
            if stop_on_goal and courant_visuel == self.graphe.arrivee:
                parents = etape.get("parents")
                if isinstance(parents, dict):
                    chemin = chemin_depuis_parents(parents, self.graphe.arrivee)
                    if chemin and chemin[0] == self.graphe.depart:
                        self.vue.afficher_chemin(chemin)
                self.iterateur_algo = None
                break

        # Afficher l'étape la plus proche atteinte
        if self.historique_etapes:
            self.index_etape = min(cible, len(self.historique_etapes) - 1)
            self._afficher_etape(self.historique_etapes[self.index_etape])

    def _cout_case(self, sommet) -> int:
        # noir = bloqué
        if sommet.bloque:
            return 10**9

        if sommet.cout == Couleur.BLANC:
            return 1
        if sommet.cout == Couleur.BLEU:
            return 5
        if sommet.cout == Couleur.VERT:
            return 2
        if sommet.cout == Couleur.JAUNE:
            return 3
        return 1

    def _nom_couleur(self, sommet) -> str:
        if sommet.bloque:
            return "Noir"
        if sommet.cout == Couleur.BLANC:
            return "Blanc"
        if sommet.cout == Couleur.BLEU:
            return "Bleu"
        if sommet.cout == Couleur.VERT:
            return "Vert"
        if sommet.cout == Couleur.JAUNE:
            return "Jaune"
        return "Blanc"

    def _log_fin_execution(self, chemin: list[int] | None):
        nb_etapes_algo = len(self.historique_etapes)

        d = self.graphe.depart
        a = self.graphe.arrivee
        d_lig, d_col = self.vue.id_vers_lig_col(d)
        a_lig, a_col = self.vue.id_vers_lig_col(a)

        self.vue.logs_append(f"Arrivée: (lig={a_lig + 1}, col={a_col + 1})")
        self.vue.logs_append(f"Nombre d'étapes (algo): {nb_etapes_algo}")

        if not chemin:
            self.vue.logs_append("Chemin: aucun (pas trouvé / pas disponible)")
            return

        # chemin en nombre de pas
        nb_pas = max(0, len(chemin) - 1)

        stats = {"Blanc": 0, "Bleu": 0, "Vert": 0, "Jaune": 0, "Noir": 0}
        cout_total = 0

        # on ignore le départ pour “cases traversées” + coût
        for node_id in chemin[1:]:
            sommet = self.graphe.obtenir_sommet(node_id)
            nom = self._nom_couleur(sommet)
            stats[nom] = stats.get(nom, 0) + 1
            cout_total += self._cout_case(sommet)

        self.vue.logs_append(f"Chemin: {len(chemin)} cases ({nb_pas} sauts)")
        self.vue.logs_append(
            "Couleurs (hors départ): " + ", ".join([f"{k}={v}" for k, v in stats.items() if v > 0])
        )
        self.vue.logs_append(f"Coût total (hors départ): {cout_total}")

    def _mouse_down(self, event):
        self._drag_actif = True
        self._drag_last_case = None
        self._drag_noir_valeur = None

        col = event.x // self.vue.taille_case
        lig = event.y // self.vue.taille_case
        if not (0 <= lig < self.vue.nb_lignes and 0 <= col < self.vue.nb_colonnes):
            return

        # Si on place depart/arrivee => on garde ton clic_grille normal (1 seul placement)
        if self.mode_selection in ("depart", "arrivee"):
            self.clic_grille(event)
            self._drag_actif = False
            return

        # Normal => on prépare l'action stable du noir AVANT d'appliquer
        id_sommet = self.sommet_id(lig, col)
        if self.couleur_active is None:
            sommet = self.graphe.obtenir_sommet(id_sommet)
            self._drag_noir_valeur = (not sommet.bloque)  # True => bloquer, False => débloquer

        # On applique la 1ère case (clic simple) avec la même logique que le drag
        self._appliquer_case(lig, col)

    def _mouse_drag(self, event):
        if not self._drag_actif:
            return

        # pas de drag si on place depart/arrivee
        if self.mode_selection in ("depart", "arrivee"):
            return

        col = event.x // self.vue.taille_case
        lig = event.y // self.vue.taille_case
        if not (0 <= lig < self.vue.nb_lignes and 0 <= col < self.vue.nb_colonnes):
            return

        if self._drag_last_case == (lig, col):
            return

        self._appliquer_case(lig, col)

    def _mouse_up(self, event):
        self._drag_actif = False
        self._drag_last_case = None
        self._drag_noir_valeur = None

    def _appliquer_case(self, lig: int, col: int):
        self._drag_last_case = (lig, col)

        id_sommet = self.sommet_id(lig, col)

        # ne pas modifier depart/arrivee
        if id_sommet == self.graphe.depart or id_sommet == self.graphe.arrivee:
            return

        sommet = self.graphe.obtenir_sommet(id_sommet)

        # Noir
        if self.couleur_active is None:
            if self._drag_noir_valeur is None:
                sommet.bloque = not sommet.bloque
            else:
                sommet.bloque = self._drag_noir_valeur
        else:
            sommet.bloque = False
            self.graphe.definir_cout(id_sommet, self.couleur_active)

        self.vue.maj_case(lig, col, sommet)
        self.vue.afficher_depart_arrivee(self.graphe.depart, self.graphe.arrivee)

















