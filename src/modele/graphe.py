from enum import Enum

class Couleur(Enum):
    BLANC = 1
    VERT = 2
    JAUNE = 3
    BLEU = 5
    BLOQUE = 100000


class Sommet:
    def __init__(self, id: int):
        self.id: int = id
        self.bloque: bool = False
        self.cout: Couleur = Couleur.BLANC


class Graphe:
    def __init__(
        self,
        sommets: dict[int, Sommet],
        voisins: dict[int, list[int]],
        depart: int | None = None,
        arrivee: int | None = None
    ):
        self.sommets: dict[int, Sommet] = sommets
        self.voisins: dict[int, list[int]] = voisins
        self.depart: int | None = depart
        self.arrivee: int | None = arrivee

    def ajouter_sommet(
        self,
        id: int,
        voisins: list[int],
        bloque: bool = False,
        cout: Couleur = Couleur.BLANC
    ):
        if id in self.sommets:
            raise ValueError(f"Sommet {id} déjà existant")

        self.sommets[id] = Sommet(id)
        self.sommets[id].bloque = bloque
        self.sommets[id].cout = cout
        self.voisins[id] = voisins

    def obtenir_sommet(self, id: int) -> Sommet:
        if id not in self.sommets:
            raise KeyError(f"Sommet {id} inexistant")
        return self.sommets[id]

    def definir_cout(self, id: int, cout: Couleur):
        self.obtenir_sommet(id).cout = cout

    def obtenir_cout(self, id: int) -> int:
        sommet = self.obtenir_sommet(id)
        return sommet.cout.value

    def bloquer_sommet(self, id: int):
        print("En train de débloquer le sommet! (Depuis graphe/model)")
        self.obtenir_sommet(id).bloque = True

    def debloquer_sommet(self, id: int):
        print("En train de débloquer le sommet! (Depuis graphe/model)")
        self.obtenir_sommet(id).bloque = False

    def definir_depart(self, id: int):
        self.depart = self.obtenir_sommet(id).id

    def definir_arrivee(self, id: int):
        self.arrivee = self.obtenir_sommet(id).id

    def obtenir_voisins(self, id: int) -> list[int]:
        if id not in self.voisins:
            raise KeyError(f"Aucune liste de voisins pour le sommet {id}")
        return self.voisins[id]
    
def construire_graphe_grille(nb_lignes: int, nb_colonnes: int) -> Graphe:
    sommets = {}
    voisins = {}

    def sommet_id(lig, col):
        return lig * nb_colonnes + col

    for lig in range(nb_lignes):
        for col in range(nb_colonnes):
            id = sommet_id(lig, col)

            sommets[id] = Sommet(id)
            voisins[id] = []

            for dl, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nl, nc = lig + dl, col + dc
                if 0 <= nl < nb_lignes and 0 <= nc < nb_colonnes:
                    voisins[id].append(sommet_id(nl, nc))

    return Graphe(sommets, voisins)

