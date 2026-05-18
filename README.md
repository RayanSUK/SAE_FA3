# SAE FA3 — Logiciel de visualisation d'algorithmes sur un graphe

Projet réalisé dans le cadre de la SAE FA3 (Situation d'Apprentissage et d'Évaluation).  
L'objectif est de concevoir un **logiciel pédagogique interactif** permettant de visualiser l'exécution d'algorithmes de théorie des graphes, pas à pas et en temps réel.

---

## Fonctionnalités

- **Grille interactive** (30 × 44 cases) représentant un graphe non orienté
- **Placement libre** du point de départ (violet) et d'arrivée (rouge)
- **Cases colorées** pour modifier le coût de traversée d'un sommet :
  - Noir : sommet bloqué (mur)
  - Blanc : coût 1
  - Vert : coût 2
  - Jaune : coût 3
  - Bleu : coût 5
- **6 algorithmes disponibles** :
  - BFS (parcours en largeur)
  - DFS (parcours en profondeur)
  - Dijkstra
  - Bellman-Ford
  - Composantes connexes
  - Ensemble dominant minimum (approche gloutonne)
- **Lecture pas à pas** : avancer, reculer, lancer/pause
- **Contrôle de vitesse** : ×1, ×4, ×8
- **Barre de progression** pour sauter à n'importe quelle étape
- **Affichage des distances** calculées sur chaque case
- **Tracé du chemin final** (ligne rouge) à la fin de l'algorithme
- **Logs** avec résumé : nombre d'étapes, coût total, composition du chemin

---

## Technologies utilisées

| Technologie | Rôle |
|---|---|
| Python 3.11+ | Langage principal |
| Tkinter / ttk | Interface graphique (GUI) |
| `collections.deque` | File FIFO pour BFS et composantes connexes |
| `heapq` | File de priorité pour Dijkstra |
| `enum.Enum` | Typage des couleurs/coûts |
| `pytest` | Tests unitaires |

Aucune dépendance externe — uniquement la bibliothèque standard Python.

---

## Lancer le projet

### Prérequis

- Python 3.11 ou supérieur
- Tkinter installé (inclus par défaut avec Python sur Windows et macOS)

Sur Linux (si nécessaire) :
```bash
sudo apt install python3-tk
```

### Lancement

Depuis la racine du projet :

```bash
cd src
python main.py
```

### Lancer les tests

Depuis la racine du projet :

```bash
pytest tests/
```

---

## Structure des dossiers

```
SAE_FA3/
├── src/
│   ├── main.py                     # Point d'entrée de l'application
│   ├── modele/
│   │   ├── graphe.py               # Classes Sommet, Graphe, enum Couleur
│   │   └── algorithmes.py          # BFS, DFS, Dijkstra, Bellman-Ford, etc.
│   ├── vue/
│   │   └── vue_principale.py       # Interface graphique (Tkinter/ttk)
│   ├── controleur/
│   │   └── controleur.py           # Contrôleur MVC (logique + événements)
│   └── docs/
│       ├── analyse_des_besoins/
│       │   ├── cahier_des_charges.md
│       │   └── recueil_des_besoins.md
│       └── conception/
│           └── Diagramme_classes.drawio.png
└── tests/
    └── modele/
        ├── test_graphe.py          # Tests unitaires du modèle graphe
        └── test_algo.py            # Tests unitaires des algorithmes
```

---

## Architecture — Pattern MVC

Le projet suit le patron de conception **MVC (Modèle-Vue-Contrôleur)** :

```
main.py
  ├── Modèle  →  Graphe + Sommet + Couleur  (graphe.py)
  │              Algorithmes générateurs     (algorithmes.py)
  ├── Vue     →  VueApplication (Tkinter)   (vue_principale.py)
  └── Contrôleur → ControleurApplication   (controleur.py)
```

**Modèle** : contient toutes les données (graphe, sommets, coûts) et les algorithmes. Il ne connaît pas la vue.

**Vue** : affiche la grille, les boutons, les logs. Elle ne contient aucune logique métier.

**Contrôleur** : fait le lien entre les deux. Il écoute les événements de la vue (clics, boutons), appelle les algorithmes du modèle, et met à jour la vue en conséquence.

---

## Fonctionnement des algorithmes — Générateurs Python

Tous les algorithmes sont implémentés comme des **générateurs Python** (mot-clé `yield`).  
À chaque étape, l'algorithme produit un dictionnaire contenant l'état courant :

```python
yield {
    "iteration": ...,
    "courant": ...,    # sommet en cours de traitement
    "ouverts": ...,    # sommets découverts mais non traités
    "fermes": ...,     # sommets déjà traités
    "distances": ...,  # distances calculées depuis le départ
    "parents": ...     # dictionnaire pour reconstruire le chemin
}
```

Le contrôleur consomme ces étapes une par une via `next()`, et les stocke dans un **historique**. Cela permet :
- L'animation automatique (boucle `after()` de Tkinter)
- Le retour arrière (relecture de l'historique)
- La barre de progression (saut direct à une étape)

---

## Représentation du graphe

Le graphe est une **grille 2D** (30 lignes × 44 colonnes = 1 320 sommets).  
Chaque sommet a un identifiant unique calculé ainsi :

```
id = ligne * nb_colonnes + colonne + 1
```

Les voisins sont stockés dans une **liste d'adjacence** (`dict[int, list[int]]`).  
Chaque sommet a au maximum 4 voisins (haut, bas, gauche, droite).
