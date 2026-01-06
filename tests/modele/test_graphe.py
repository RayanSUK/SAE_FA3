import pytest
from src.modele.graphe import Graphe, Sommet, Couleur

@pytest.fixture
def graphe_simple():
    # Initialisation avec des objets Sommet
    sommets = {
        1: Sommet(1),
        2: Sommet(2),
        3: Sommet(3)
    }
    voisins = {1: [2, 3], 2: [1], 3: [1]}
    g = Graphe(sommets, voisins, depart=1, arrivee=3)
    return g


def test_ajouter_sommet(graphe_simple):
    # Test de l'ajout d'un nouveau sommet
    graphe_simple.ajouter_sommet(4, voisins=[1])
    assert 4 in graphe_simple.sommets
    assert isinstance(graphe_simple.sommets[4], Sommet)
    assert graphe_simple.voisins[4] == [1]


def test_ajouter_sommet_existant(graphe_simple):
    # Vérifie que l'ajout d'un doublon lève une ValueError
    with pytest.raises(ValueError):
        graphe_simple.ajouter_sommet(1, voisins=[])


def test_voisins(graphe_simple):
    voisins_1 = graphe_simple.obtenir_voisins(1)
    assert voisins_1 == [2, 3]


def test_voisins_sommet_inexistant(graphe_simple):
    # La nouvelle méthode lève une KeyError si le sommet n'existe pas
    with pytest.raises(KeyError):
        graphe_simple.obtenir_voisins(99)


def test_bloquer_debloquer_sommet(graphe_simple):
    graphe_simple.bloquer_sommet(1)
    assert graphe_simple.sommets[1].bloque is True

    graphe_simple.debloquer_sommet(1)
    assert graphe_simple.sommets[1].bloque is False


def test_definir_depart_arrivee(graphe_simple):
    graphe_simple.definir_depart(2)
    graphe_simple.definir_arrivee(1)

    assert graphe_simple.depart == 2
    assert graphe_simple.arrivee == 1


def test_definir_cout(graphe_simple):
    graphe_simple.definir_cout(2, Couleur.BLEU)
    assert graphe_simple.sommets[2].cout == Couleur.BLEU
    # Test de la méthode obtenir_cout qui retourne la valeur numérique
    assert graphe_simple.obtenir_cout(2) == 5


def test_obtenir_sommet_existant(graphe_simple):
    sommet = graphe_simple.obtenir_sommet(1)
    assert sommet.id == 1


def test_obtenir_sommet_inexistant(graphe_simple):
    # La nouvelle méthode lève une KeyError
    with pytest.raises(KeyError):
        graphe_simple.obtenir_sommet(99)


def test_ajouter_sommet_bloque_et_cout():
    # Test de l'initialisation complète via ajouter_sommet
    g = Graphe(sommets={}, voisins={})
    g.ajouter_sommet(10, voisins=[], bloque=True, cout=Couleur.JAUNE)

    sommet = g.obtenir_sommet(10)
    assert sommet.bloque is True
    assert sommet.cout == Couleur.JAUNE
    assert g.obtenir_cout(10) == 3