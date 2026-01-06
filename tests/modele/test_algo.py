import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


import pytest

from collections import deque

from src.modele.graphe import Graphe, Sommet, Couleur
from src.modele.algorithmes import bfs_pas_a_pas


def test_bfs_pas_a_pas_simple():
    """
    Graphe de test :
        1 -- 2 -- 4
         \
          3
    """

    # Création des sommets
    sommets = {
        1: Sommet(1),
        2: Sommet(2),
        3: Sommet(3),
        4: Sommet(4)
    }

    # Tous les sommets ont un coût par défaut
    for s in sommets.values():
        s.cout = Couleur.BLANC

    # Définition des voisins
    voisins = {
        1: [2, 3],
        2: [1, 4],
        3: [1],
        4: [2]
    }

    # Création du graphe
    graphe = Graphe(
        sommets=sommets,
        voisins=voisins,
        depart=1,
        arrivee=4
    )

    # Exécution du BFS pas à pas
    etapes = list(bfs_pas_a_pas(graphe))
    for i in range(len(etapes)):
        print(f"Étape {i}: {etapes[i]}")

    # ────────────────
    # Vérifications
    # ────────────────

    # Il doit y avoir plusieurs étapes
    assert len(etapes) > 0

    # Première étape : sommet de départ
    assert etapes[0]["courant"] == 1
    assert etapes[0]["distances"][1] == 0

    # Dernière étape : toutes les distances connues
    distances_finales = etapes[-1]["distances"]
    assert distances_finales[2] == 1
    assert distances_finales[3] == 1
    assert distances_finales[4] == 2

    # Vérification des parents (chemin possible vers 4)
    parents_finaux = etapes[-1]["parents"]
    assert parents_finaux[4] == 2
    assert parents_finaux[2] == 1

test_bfs_pas_a_pas_simple()