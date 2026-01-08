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

    @classmethod
    def creer_graphe_parties(cls, largeur, hauteur):
        sommets = {}
        voisins = {}

        for y in range(hauteur):
            for x in range(largeur):
                id = y * largeur + x + 1

                sommets[id] = Sommet(id)
                liste_voisins = []

                # Voisin de droite (x + 1)
                if x < largeur - 1:
                    liste_voisins.append(id + 1)

                # Voisin de gauche (x - 1)
                if x > 0:
                    liste_voisins.append(id - 1)

                # Voisin du bas (y + 1)
                if y < hauteur - 1:
                    liste_voisins.append(id + largeur)

                # Voisin du haut (y - 1)
                if y > 0:
                    liste_voisins.append(id - largeur)

                voisins[id] = liste_voisins

        return cls(sommets, voisins)
