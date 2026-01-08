import tkinter as tk
from tkinter import ttk
from modele.graphe import Couleur



class VueApplication(ttk.Frame):
    """
    interface graphique.
    Zone graphe + panneau propriétés.
    """
    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.construire_style()
        self.construire_layout()

        # --- Mémoire d'affichage (résultat algo) ---
        self._ouverts_prev = set()
        self._fermes_prev = set()
        self._courant_prev = None

        self._textes_distances = {}   # id_sommet -> id_canvas_text
        self.ligne_chemin = None


    # ---------------- Style ----------------
    def construire_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Card.TFrame", padding=12)
        style.configure("Title.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("Section.TLabel", font=("Segoe UI", 11, "bold"))
        style.configure("Legend.TLabel", font=("Segoe UI", 10, "bold"))

    # ---------------- Layout principal ----------------
    def construire_layout(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)   # graphe
        self.columnconfigure(1, weight=0)   # propriétés

        self.construire_zone_graphe()
        self.construire_zone_proprietes()

    # ---------------- Zone Graphe ----------------
    def construire_zone_graphe(self):
        self.zone_gauche = ttk.Frame(self)
        self.zone_gauche.grid(row=0, column=0, sticky="nsew", padx=(10, 8), pady=10)
        self.zone_gauche.rowconfigure(0, weight=1)
        self.zone_gauche.columnconfigure(0, weight=1)

        self.canvas_graphe = tk.Canvas(
            self.zone_gauche,
            bg="#f7f7f7",
            highlightthickness=1,
            highlightbackground="#d0d0d0"
        )
        self.canvas_graphe.grid(row=0, column=0, sticky="nsew")

        # --- Grille ---
        self.nb_lignes = 30
        self.nb_colonnes = 44
        self.taille_case = 45  # px (change si tu veux plus grand/petit)

        self.rectangles_cases = [[None for _ in range(self.nb_colonnes)] for _ in range(self.nb_lignes)]

        for lig in range(self.nb_lignes):
            for col in range(self.nb_colonnes):
                x1 = col * self.taille_case
                y1 = lig * self.taille_case
                x2 = x1 + self.taille_case
                y2 = y1 + self.taille_case

                rect_id = self.canvas_graphe.create_rectangle(
                    x1, y1, x2, y2,
                    fill="#ffffff",
                    outline="#d0d0d0"
                )
                self.rectangles_cases[lig][col] = rect_id

        #  Marqueurs Départ / Arrivée
        self.marqueur_depart = self.canvas_graphe.create_oval(0, 0, 0, 0, outline="purple", width=3)
        self.marqueur_arrivee = self.canvas_graphe.create_oval(0, 0, 0, 0, outline="red", width=3)

    # ---------------- Zone Propriétés ----------------
    def construire_zone_proprietes(self):
        self.zone_droite = ttk.Frame(self, style="Card.TFrame", width=340)
        self.zone_droite.grid(row=0, column=1, sticky="ns", padx=(8, 10), pady=10)
        self.zone_droite.grid_propagate(False)

        self.construire_proprietes(self.zone_droite)

    # ---------------- Tuile couleur ----------------
    def creer_tuile_couleur(self, parent, nom: str, couleur: str):
        conteneur = ttk.Frame(parent)

        tuile = tk.Canvas(
            conteneur,
            width=46,
            height=46,
            highlightthickness=1,
            highlightbackground="#cfcfcf"
        )
        tuile.create_rectangle(0, 0, 46, 46, fill=couleur, outline=couleur)
        tuile.grid(row=0, column=0, pady=(0, 4))

        ttk.Label(conteneur, text=nom).grid(row=1, column=0)

        try:
            tuile.configure(cursor="hand2")
        except tk.TclError:
            pass

        return conteneur, tuile

    def maj_case(self, lig, col, sommet):
        rect = self.rectangles_cases[lig][col]

        couleurs = {
            Couleur.BLANC: "#ffffff",
            Couleur.BLEU: "#2f6fed",
            Couleur.VERT: "#2fa84f",
            Couleur.JAUNE: "#f2d23a",
        }

        couleur = "#000000" if sommet.bloque else couleurs[sommet.cout]

        self.canvas_graphe.itemconfig(rect, fill=couleur)

    def id_vers_lig_col(self, id_sommet: int) -> tuple[int, int]:
        idx = id_sommet - 1
        lig = idx // self.nb_colonnes
        col = idx % self.nb_colonnes
        return lig, col

    def afficher_depart_arrivee(self, id_depart: int | None, id_arrivee: int | None):
        """
        Affiche visuellement le départ (violet) et l'arrivée (rouge) sur la grille.
        On dessine juste un ovale
        """
        if id_depart is not None:
            lig, col = self.id_vers_lig_col(id_depart)
            self._placer_marqueur(self.marqueur_depart, lig, col)

        if id_arrivee is not None:
            lig, col = self.id_vers_lig_col(id_arrivee)
            self._placer_marqueur(self.marqueur_arrivee, lig, col)

        # Met les marqueurs au premier plan
        self.canvas_graphe.tag_raise(self.marqueur_depart)
        self.canvas_graphe.tag_raise(self.marqueur_arrivee)

    def _placer_marqueur(self, marqueur_id: int, lig: int, col: int):
        marge = 5
        x1 = col * self.taille_case + marge
        y1 = lig * self.taille_case + marge
        x2 = (col + 1) * self.taille_case - marge
        y2 = (lig + 1) * self.taille_case - marge
        self.canvas_graphe.coords(marqueur_id, x1, y1, x2, y2)



    # ---------------- Propriétés ----------------
    def construire_proprietes(self, parent: ttk.Frame):
        parent.columnconfigure(0, weight=1)

        # Titre
        ttk.Label(parent, text="Propriétés", style="Title.TLabel") \
            .grid(row=0, column=0, sticky="w", pady=(0, 10))

        # ---- Couleurs ----
        ttk.Label(parent, text="Couleurs", style="Section.TLabel") \
            .grid(row=1, column=0, sticky="w", pady=(0, 8))

        modes = ttk.Frame(parent)
        modes.grid(row=2, column=0, sticky="ew")
        for i in range(3):
            modes.columnconfigure(i, weight=1)

        wrap_noir,   self.tuile_noir   = self.creer_tuile_couleur(modes, "Noir",  "#000000")
        wrap_blanc,  self.tuile_blanc  = self.creer_tuile_couleur(modes, "Blanc", "#ffffff")
        wrap_bleu,   self.tuile_bleu   = self.creer_tuile_couleur(modes, "Bleu",  "#2f6fed")
        wrap_vert,   self.tuile_vert   = self.creer_tuile_couleur(modes, "Vert",  "#2fa84f")
        wrap_jaune,  self.tuile_jaune  = self.creer_tuile_couleur(modes, "Jaune", "#f2d23a")

        wrap_noir.grid(row=0, column=0, padx=6, pady=4)
        wrap_blanc.grid(row=0, column=1, padx=6, pady=4)
        wrap_bleu.grid(row=0, column=2, padx=6, pady=4)
        wrap_vert.grid(row=1, column=0, padx=6, pady=4)
        wrap_jaune.grid(row=1, column=1, padx=6, pady=4)

        # ---- Coûts ----
        ttk.Label(parent, text="Coûts", style="Section.TLabel") \
            .grid(row=3, column=0, sticky="w", pady=(10, 6))

        couts = ttk.Frame(parent)
        couts.grid(row=4, column=0, sticky="ew")
        couts.columnconfigure(0, weight=1)
        couts.columnconfigure(1, weight=0)

        def ajouter_ligne_cout(ligne, libelle, valeur):
            ttk.Label(couts, text=libelle).grid(row=ligne, column=0, sticky="w", pady=2)
            ttk.Label(couts, text=valeur).grid(row=ligne, column=1, sticky="e", pady=2)

        ajouter_ligne_cout(0, "Noir",  "Bloqué")
        ajouter_ligne_cout(1, "Blanc", "1")
        ajouter_ligne_cout(2, "Bleu",  "5")
        ajouter_ligne_cout(3, "Vert",  "2")
        ajouter_ligne_cout(4, "Jaune", "3")

        # ---- Légende ----
        legende = ttk.Frame(parent)
        legende.grid(row=5, column=0, sticky="ew", pady=(12, 10))

        ttk.Label(legende, text="● Départ", style="Legend.TLabel", foreground="purple") \
            .grid(row=0, column=0, sticky="w")
        ttk.Label(legende, text="● Arrivee", style="Legend.TLabel", foreground="red") \
            .grid(row=1, column=0, sticky="w")

        # ---- Points (départ / arrivée) ----
        ttk.Separator(parent).grid(row=6, column=0, sticky="ew", pady=(8, 8))

        ttk.Label(parent, text="Points", style="Section.TLabel") \
            .grid(row=7, column=0, sticky="w", pady=(0, 6))

        points = ttk.Frame(parent)
        points.grid(row=8, column=0, sticky="ew")
        points.columnconfigure(0, weight=1)
        points.columnconfigure(1, weight=1)

        self.bouton_placer_depart = ttk.Button(points, text="Placer départ")
        self.bouton_placer_arrivee = ttk.Button(points, text="Placer arrivée")

        self.bouton_placer_depart.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.bouton_placer_arrivee.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        self.bouton_points_par_defaut = ttk.Button(parent, text="Points par défaut")
        self.bouton_points_par_defaut.grid(row=9, column=0, sticky="ew", pady=(6, 0))


        # ---- Option distances ----
        self.var_afficher_distances = tk.BooleanVar(value=True)
        self.case_distances = ttk.Checkbutton(
            parent,
            text="Afficher distances",
            variable=self.var_afficher_distances
        )
        self.case_distances.grid(row=10, column=0, sticky="w", pady=8)

        # ---- Algorithme ----
        ttk.Separator(parent).grid(row=11, column=0, sticky="ew", pady=8)

        ttk.Label(parent, text="Algorithme", style="Section.TLabel") \
            .grid(row=12, column=0, sticky="w", pady=(0, 6))

        self.liste_algo = ttk.Combobox(
            parent,
            values=["DFS", "Bellman-Ford", "BFS", "Dijkstra"],
            state="readonly"
        )

        self.liste_algo.set("DFS")
        self.liste_algo.grid(row=13, column=0, sticky="ew")

        # ---- Bouton lancer ----
        self.bouton_lancer_algo = ttk.Button(parent, text="Lancer")
        self.bouton_lancer_algo.grid(row=14, column=0, sticky="ew", pady=(8, 0))

        # ---- Boutons bas ----
        bas = ttk.Frame(parent)
        bas.grid(row=15, column=0, sticky="ew", pady=(10, 0))
        bas.columnconfigure(0, weight=1)
        bas.columnconfigure(1, weight=1)

        self.bouton_effacer_resultat = ttk.Button(bas, text="Effacer résultat")
        self.bouton_effacer_tout = ttk.Button(bas, text="Effacer tout")

        self.bouton_effacer_resultat.grid(row=0, column=0, padx=(0, 6), sticky="ew")
        self.bouton_effacer_tout.grid(row=0, column=1, padx=(6, 0), sticky="ew")

        # ---- Lecture de l'algorithme ----
        ttk.Separator(parent).grid(row=16, column=0, sticky="ew", pady=(12, 10))

        ttk.Label(parent, text="Lecture", style="Section.TLabel") \
            .grid(row=17, column=0, sticky="w", pady=(0, 6))

        # Conteneur des boutons de contrôle (reculer / pause / avancer)
        conteneur_controles = ttk.Frame(parent)
        conteneur_controles.grid(row=18, column=0, sticky="ew")

        # Les boutons occupent toute la largeur disponible
        for i in range(3):
            conteneur_controles.columnconfigure(i, weight=1)

        self.bouton_reculer_etape = ttk.Button(conteneur_controles, text="⏮")
        self.bouton_lancer_pause = ttk.Button(conteneur_controles, text="⏯")
        self.bouton_avancer_etape = ttk.Button(conteneur_controles, text="⏭")

        self.bouton_reculer_etape.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.bouton_lancer_pause.grid(row=0, column=1, sticky="ew", padx=6)
        self.bouton_avancer_etape.grid(row=0, column=2, sticky="ew", padx=(6, 0))

        # Réglage de la vitesse d'exécution
        ttk.Label(parent, text="Vitesse").grid(row=19, column=0, sticky="w", pady=(10, 4))

        conteneur_vitesse = ttk.Frame(parent)
        conteneur_vitesse.grid(row=20, column=0, sticky="ew")

        for i in range(3):
            conteneur_vitesse.columnconfigure(i, weight=1)

        self.bouton_vitesse_05 = ttk.Button(conteneur_vitesse, text="×1")
        self.bouton_vitesse_1 = ttk.Button(conteneur_vitesse, text="×4")
        self.bouton_vitesse_2 = ttk.Button(conteneur_vitesse, text="×8")

        self.bouton_vitesse_05.grid(row=0, column=0, sticky="ew", padx=2)
        self.bouton_vitesse_1.grid(row=0, column=1, sticky="ew", padx=2)
        self.bouton_vitesse_2.grid(row=0, column=2, sticky="ew", padx=2)

        # Barre de progression (avancement de l'algorithme)
        ttk.Label(parent, text="Progression").grid(row=21, column=0, sticky="w", pady=(10, 2))
        self.curseur_progression = ttk.Scale(parent, from_=0, to=100, orient="horizontal")
        self.curseur_progression.grid(row=22, column=0, sticky="ew")

        # ---- Logs ----
        ttk.Separator(parent).grid(row=23, column=0, sticky="ew", pady=(12, 8))

        ttk.Label(parent, text="Logs", style="Section.TLabel") \
            .grid(row=24, column=0, sticky="w", pady=(0, 6))

        logs_frame = ttk.Frame(parent)
        logs_frame.grid(row=25, column=0, sticky="nsew")
        parent.rowconfigure(25, weight=1)  # pour que ça prenne l'espace restant si possible

        self.logs_text = tk.Text(
            logs_frame,
            height=8,
            wrap="word",
            state="disabled",
            font=("Consolas", 12)
        )
        # Tag pour le gras (avant les :)
        self.logs_text.tag_configure("log_bold", font=("Consolas", 12, "bold"))

        self.logs_text.grid(row=0, column=0, sticky="nsew")

        logs_scroll = ttk.Scrollbar(logs_frame, orient="vertical", command=self.logs_text.yview)
        logs_scroll.grid(row=0, column=1, sticky="ns")

        self.logs_text.configure(yscrollcommand=logs_scroll.set)

        logs_frame.rowconfigure(0, weight=1)
        logs_frame.columnconfigure(0, weight=1)



    def _centre_case(self, lig: int, col: int) -> tuple[int, int]:
        x = col * self.taille_case + self.taille_case // 2
        y = lig * self.taille_case + self.taille_case // 2
        return x, y

    def effacer_resultat(self):
        """Efface uniquement le résultat/affichage de l'algorithme"""
        if hasattr(self, "_ouverts_prev"):
            for id_sommet in self._ouverts_prev:
                lig, col = self.id_vers_lig_col(id_sommet)
                rect = self.rectangles_cases[lig][col]
                self.canvas_graphe.itemconfig(rect, outline="#d0d0d0", width=1)

        if hasattr(self, "_fermes_prev"):
            for id_sommet in self._fermes_prev:
                lig, col = self.id_vers_lig_col(id_sommet)
                rect = self.rectangles_cases[lig][col]
                self.canvas_graphe.itemconfig(rect, outline="#d0d0d0", width=1)

        self._ouverts_prev = set()
        self._fermes_prev = set()

        if hasattr(self, "ligne_chemin") and self.ligne_chemin is not None:
            self.canvas_graphe.delete(self.ligne_chemin)
            self.ligne_chemin = None

        if hasattr(self, "logs_text"):
            self.logs_clear()


        self.canvas_graphe.tag_raise(self.marqueur_depart)
        self.canvas_graphe.tag_raise(self.marqueur_arrivee)
        self.effacer_distances()
        self._courant_prev = None

    def _set_outline_case(self, id_sommet: int, couleur: str, width: int = 2):
        lig, col = self.id_vers_lig_col(id_sommet)
        rect = self.rectangles_cases[lig][col]
        self.canvas_graphe.itemconfig(rect, outline=couleur, width=width)

    def _maj_texte_distance(self, id_sommet: int, valeur: int | float):
        """Affiche (ou met à jour) un texte de distance au centre de la case."""
        lig, col = self.id_vers_lig_col(id_sommet)
        x, y = self._centre_case(lig, col)

        # On n'affiche pas les distances infinies (sinon ça pollue l'écran)
        if valeur == float("inf"):
            return

        txt = str(int(valeur)) if isinstance(valeur, (int, float)) else str(valeur)

        if id_sommet in self._textes_distances:
            self.canvas_graphe.itemconfig(self._textes_distances[id_sommet], text=txt)
            self.canvas_graphe.coords(self._textes_distances[id_sommet], x, y)
        else:
            text_id = self.canvas_graphe.create_text(x, y, text=txt, font=("Segoe UI", 9, "bold"))
            self._textes_distances[id_sommet] = text_id

    def effacer_distances(self):
        """Supprime tous les textes de distances."""
        for _, text_id in self._textes_distances.items():
            try:
                self.canvas_graphe.delete(text_id)
            except Exception:
                pass
        self._textes_distances = {}

    def afficher_etape(
        self,
        ouverts: set[int],
        fermes: set[int],
        courant: int | None,
        distances: dict[int, int | float] | None = None
    ):
        """
        Affichage simple type 'hexa':
        - OUVERTS : contour bleu
        - FERMES : contour gris
        - COURANT : contour violet plus épais
        - Distances : texte si option cochée
        """

        # 1) Remettre à normal les cases qui sortent de "ouverts"
        for id_sommet in (self._ouverts_prev - ouverts):
            self._set_outline_case(id_sommet, "#d0d0d0", 1)

        # 2) Remettre à normal les cases qui sortent de "fermes"
        for id_sommet in (self._fermes_prev - fermes):
            self._set_outline_case(id_sommet, "#d0d0d0", 1)

        # 3) Appliquer style sur nouveaux ouverts / fermes
        for id_sommet in (ouverts - self._ouverts_prev):
            self._set_outline_case(id_sommet, "#1e90ff", 2)  # bleu

        for id_sommet in (fermes - self._fermes_prev):
            self._set_outline_case(id_sommet, "#808080", 2)  # gris

        # 4) Ancien courant -> le remettre cohérent (ouvert/fermé/normal)
        if self._courant_prev is not None:
            prev = self._courant_prev
            if prev in fermes:
                self._set_outline_case(prev, "#808080", 2)
            elif prev in ouverts:
                self._set_outline_case(prev, "#1e90ff", 2)
            else:
                self._set_outline_case(prev, "#d0d0d0", 1)

        # 5) Nouveau courant
        if courant is not None:
            self._set_outline_case(courant, "purple", 3)

        # 6) Distances (option)
        if self.var_afficher_distances.get() and distances is not None:
            # On affiche uniquement celles qu'on connaît (distances dict)
            for id_sommet, d in distances.items():
                self._maj_texte_distance(id_sommet, d)
        else:
            self.effacer_distances()

        # 7) Mémoriser pour le prochain tick
        self._ouverts_prev = set(ouverts)
        self._fermes_prev = set(fermes)
        self._courant_prev = courant

        # marqueurs au-dessus
        self.canvas_graphe.tag_raise(self.marqueur_depart)
        self.canvas_graphe.tag_raise(self.marqueur_arrivee)

    def afficher_chemin(self, chemin: list[int]):
        """Trace un polyline rouge pour le chemin final."""
        if not chemin or len(chemin) < 2:
            return

        # Supprime ancien chemin
        if self.ligne_chemin is not None:
            try:
                self.canvas_graphe.delete(self.ligne_chemin)
            except Exception:
                pass
            self.ligne_chemin = None

        points = []
        for id_sommet in chemin:
            lig, col = self.id_vers_lig_col(id_sommet)
            x, y = self._centre_case(lig, col)
            points.extend([x, y])

        self.ligne_chemin = self.canvas_graphe.create_line(*points, fill="red", width=3)

        self.canvas_graphe.tag_raise(self.marqueur_depart)
        self.canvas_graphe.tag_raise(self.marqueur_arrivee)

    def logs_clear(self):
        self.logs_text.configure(state="normal")
        self.logs_text.delete("1.0", "end")
        self.logs_text.configure(state="disabled")

    def logs_append(self, message: str):
        self.logs_text.configure(state="normal")

        # position de début de la ligne
        start_index = self.logs_text.index("end-1c")

        # insère le message + retour ligne
        self.logs_text.insert("end", message + "\n")

        # Met en gras tout ce qui est avant le premier ":" (si présent)
        colon_pos = message.find(":")
        if colon_pos != -1:
            # de start_index à start_index + colon_pos caractères
            bold_start = start_index
            bold_end = f"{start_index}+{colon_pos}c"
            self.logs_text.tag_add("log_bold", bold_start, bold_end)

        self.logs_text.see("end")
        self.logs_text.configure(state="disabled")











