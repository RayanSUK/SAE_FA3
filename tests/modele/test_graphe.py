import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
from src.modele.graphe import Graphe, Sommet, Couleur


@pytest.fixture
def graphe_simple():
    sommets = {}
    voisins = {1: [2, 3], 2: [1], 3: [1]}
    g = Graphe(sommets, voisins, depart=1, arrivee=3)
    return g


def test_ajouter_sommet(graphe_simple):
    assert 1 in graphe_simple.sommets
    assert isinstance(graphe_simple.sommets[1], Sommet)


def test_voisins(graphe_simple):
    voisins_1 = graphe_simple.obtenir_voisins(1)
    assert voisins_1 == [2, 3]


def test_bloquer_debloquer_sommet(graphe_simple):
    graphe_simple.bloquer_sommet(1)
    assert graphe_simple.sommets[1].bloque is True

    graphe_simple.debloquer_sommet(1)
    assert graphe_simple.sommets[1].bloque is False


def test_definir_depart_arrivee(graphe_simple):
    graphe_simple.definir_depart(1)
    graphe_simple.definir_arrivee(3)

    assert graphe_simple.depart == 1
    assert graphe_simple.arrivee == 3


def test_definir_cout(graphe_simple):
    graphe_simple.definir_cout(2, Couleur.BLEU)
    assert graphe_simple.sommets[2].cout == Couleur.BLEU


def test_obtenir_sommet_existant(graphe_simple):
    sommet = graphe_simple.obtenir_sommet(1)
    assert sommet is not None
    assert sommet.id == 1


def test_obtenir_sommet_inexistant(graphe_simple):
    sommet = graphe_simple.obtenir_sommet(99)
    assert sommet is None


def test_ajouter_sommet_bloque_et_cout():
    sommets = {}
    voisins = {10: []}
    g = Graphe(sommets, voisins, depart=1, arrivee=3)   
    g.ajouter_sommet(10, voisins=[], bloque=True, cout=Couleur.JAUNE)

    sommet = g.obtenir_sommet(10)
    if sommet is None:
        assert False, "Le sommet n'a pas été trouvé"
    assert sommet.bloque is True
    assert sommet.cout == Couleur.JAUNE


def test_voisins_sommet_inexistant(graphe_simple):
    voisins = graphe_simple.obtenir_voisins(99)
    assert voisins == []
