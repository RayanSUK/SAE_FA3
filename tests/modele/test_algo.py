import sys
import os
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from collections import deque
from src.modele.graphe import Graphe, Sommet, Couleur
from src.modele.algorithmes import bfs_pas_a_pas, dfs_pas_a_pas


def test_bfs_pas_a_pas():
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

    etapes = list(bfs_pas_a_pas(graphe))
    print(*etapes, sep="\n")

    assert len(etapes) > 0

    assert etapes[0]["courant"] == 1
    assert etapes[0]["distances"][1] == 0

    distances_finales = etapes[-1]["distances"]
    assert distances_finales[2] == 1
    assert distances_finales[3] == 1
    assert distances_finales[4] == 2

    parents_finaux = etapes[-1]["parents"]
    assert parents_finaux[4] == 2
    assert parents_finaux[2] == 1

def test_dfs_pas_a_pas():
    """
    Graphe de test :
        1 -- 2 -- 4 -- 5
         \
          3
    """
    sommets = {i: Sommet(i) for i in range(1, 6)}

    for s in sommets.values():
        s.bloque = False

    voisins = {
        1: [2, 3],
        2: [1, 4],
        3: [1],
        4: [2, 5],
        5: [4]
    }

    graphe = Graphe(
        sommets=sommets,
        voisins=voisins,
        depart=1,
        arrivee=5
    )

    etapes = list(dfs_pas_a_pas(graphe))
    print(*etapes, sep="\n")

    assert len(etapes) == 5

    # Le DFS explore la branche 1-2-4-5 avant de revenir à 3
    ordre_visite = [e["courant"] for e in etapes]
    assert ordre_visite == [1, 2, 4, 5, 3]

    derniere_etape = etapes[-1]

    assert derniere_etape["parents"][2] == 1
    assert derniere_etape["parents"][4] == 2
    assert derniere_etape["parents"][5] == 4
    assert derniere_etape["parents"][3] == 1

    assert derniere_etape["fermes"] == {1, 2, 3, 4, 5}
    assert len(derniere_etape["ouverts"]) == 0
