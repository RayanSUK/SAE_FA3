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
        self.nb_lignes = 60
        self.nb_colonnes = 80
        self.taille_case = 23  # px (change si tu veux plus grand/petit)

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
        ajouter_ligne_cout(3, "Vert",  "3")
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
            values=["DFS", "Bellman-Ford", "A*"],
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

        self.bouton_vitesse_05 = ttk.Button(conteneur_vitesse, text="×0,5")
        self.bouton_vitesse_1 = ttk.Button(conteneur_vitesse, text="×1")
        self.bouton_vitesse_2 = ttk.Button(conteneur_vitesse, text="×2")

        self.bouton_vitesse_05.grid(row=0, column=0, sticky="ew", padx=2)
        self.bouton_vitesse_1.grid(row=0, column=1, sticky="ew", padx=2)
        self.bouton_vitesse_2.grid(row=0, column=2, sticky="ew", padx=2)

        # Barre de progression (avancement de l'algorithme)
        ttk.Label(parent, text="Progression").grid(row=21, column=0, sticky="w", pady=(10, 2))
        self.curseur_progression = ttk.Scale(parent, from_=0, to=100, orient="horizontal")
        self.curseur_progression.grid(row=22, column=0, sticky="ew")

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

        self.canvas_graphe.tag_raise(self.marqueur_depart)
        self.canvas_graphe.tag_raise(self.marqueur_arrivee)






