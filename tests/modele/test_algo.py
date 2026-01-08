from modulefinder import test
import sys
import os
import pytest
import heapq
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from collections import deque
from src.modele.graphe import Graphe, Sommet, Couleur
from src.modele.algorithmes import bfs_pas_a_pas, dfs_pas_a_pas, dijkstra_pas_a_pas, bellman_ford_pas_a_pas, composantes_connexes_pas_a_pas, minimum_dominating_set_pas_a_pas


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

    assert len(etapes) == 4

    # Le DFS explore la branche 1-2-4-5 avant de revenir à 3
    ordre_visite = [e["courant"] for e in etapes]
    assert ordre_visite == [1, 2, 4, 5]

    derniere_etape = etapes[-1]

    assert derniere_etape["parents"][2] == 1
    assert derniere_etape["parents"][4] == 2
    assert derniere_etape["parents"][5] == 4
    assert derniere_etape["parents"][3] == 1

    assert derniere_etape["fermes"] == {1, 2, 4, 5}
    assert len(derniere_etape["ouverts"]) == 1

def test_dijkstra_pas_a_pas():
    """
    Graphe de test avec poids (basés sur Couleur)

    """

    sommets = {
        1: Sommet(1),
        2: Sommet(2),
        3: Sommet(3),
        4: Sommet(4),
        5: Sommet(5)
    }

    sommets[1].cout = Couleur.BLANC # 1
    sommets[2].cout = Couleur.JAUNE # 3
    sommets[3].cout = Couleur.BLEU # 5
    sommets[4].cout = Couleur.BLANC # 1
    sommets[5].cout = Couleur.BLANC # 1


    voisins = {
        1: [2, 3],
        2: [1, 4],
        3: [1, 5],
        4: [2, 5],
        5: [3,4]
    }

    graphe = Graphe(
        sommets=sommets,
        voisins=voisins,
        depart=1,
        arrivee=5
    )

    etapes = list(dijkstra_pas_a_pas(graphe))
    print(*etapes, sep="\n")

    assert len(etapes) > 0

    derniere_etape = etapes[-1]
    distances_finales = derniere_etape["distances"]
    parents_finaux = derniere_etape["parents"]

    assert distances_finales[1] == 0
    assert distances_finales[2] == 3
    assert distances_finales[3] == 5
    assert distances_finales[4] == 4
    assert distances_finales[5] == 5
    assert parents_finaux[5] == 4

    ordre_traitement = [e["courant"] for e in etapes]
    assert ordre_traitement[0] == 1
    assert ordre_traitement[1] == 2

def test_bellman_ford_pas_a_pas():
    """
    Graphe de test avec poids (basés sur Couleur)
    """

    # 1. Initialisation des sommets
    sommets = {
        1: Sommet(1),
        2: Sommet(2),
        3: Sommet(3),
        4: Sommet(4),
        5: Sommet(5)
    }

    sommets[1].cout = Couleur.BLANC
    sommets[5].cout = Couleur.BLEU
    sommets[4].cout = Couleur.BLANC
    sommets[3].cout = Couleur.BLANC
    sommets[2].cout = Couleur.BLANC

    voisins = {
        1: [5, 4],
        5: [1, 2],
        4: [1, 3],
        3: [4, 2],
        2: [3, 5]
    }

    graphe = Graphe(
        sommets=sommets,
        voisins=voisins,
        depart=1,
        arrivee=5
    )

    etapes = list(bellman_ford_pas_a_pas(graphe))
    print(*etapes, sep="\n")

    assert len(etapes) > 0, "L'algorithme devrait produire au moins une étape"

    derniere_etape = etapes[-1]
    distances_finales = derniere_etape["distances"]
    parents_finaux = derniere_etape["parents"]

    assert distances_finales[1] == 0
    assert distances_finales[5] == 5
    assert distances_finales[2] == 3
    assert distances_finales[3] == 2
    assert distances_finales[4] == 1

    assert parents_finaux[2] == 3
    assert parents_finaux[3] == 4
    assert parents_finaux[4] == 1
    assert parents_finaux[5] == 1

def test_composantes_connexes():
    """
    Graphe de test :
        1 -- 2     4
              \
               3
    """
    sommets = {i: Sommet(i) for i in range(1, 5)}

    voisins = {
        1: [2],
        2: [1, 3],
        3: [2],
        4: []
    }

    graphe = Graphe(sommets=sommets, voisins=voisins)

    etapes = list(composantes_connexes_pas_a_pas(graphe))
    print(*etapes, sep="\n")
    assert len(etapes) > 0

    derniere = etapes[-1]
    composantes = derniere["composantes"]

    assert len(composantes) == 2
    assert {1, 2, 3} in composantes.values()
    assert {4} in composantes.values()

def test_minimum_dominating_set_pas_a_pas():
    """
    Graphe de test :
        1 -- 2 -- 3
        |         |
        4---------5
    Sommets 3 bloqué
    """

    sommets = {i: Sommet(i) for i in range(1, 6)}
    sommets[3].bloque = True

    voisins = {
        1: [2,4],
        2: [1,3],
        3: [2,5],
        4: [1,5],
        5: [3,4]
    }

    graphe = Graphe(
        sommets=sommets,
        voisins=voisins
    )

    etapes = list(minimum_dominating_set_pas_a_pas(graphe))
    print(*etapes, sep="\n")

    assert len(etapes) > 0

    for etape in etapes:
        assert 3 not in etape["ensemble_dominant"]

    dernier = etapes[-1]
    ensemble_dominant = dernier["ensemble_dominant"]
    sommets_non_domines = dernier["sommets_non_domines"]
    assert len(sommets_non_domines) == 0  # tous dominés

    assert len(ensemble_dominant) > 0

    # 1 domine 1,2,4 → suffisant, approximatif
    assert 1 in ensemble_dominant or 2 in ensemble_dominant or 4 in ensemble_dominant

    for etape in etapes:
        assert etape["sommet_choisi"] in etape["ensemble_dominant"]
