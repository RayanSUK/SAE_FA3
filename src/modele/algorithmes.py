import heapq
import math
from .graphe import Graphe, Sommet
from collections import deque

def bfs_pas_a_pas(graphe: Graphe):
    """
    Algorithme de recherche de "parcours en largeur" (*Breadth-First Search*).

    Il cherche parmi les voisins directs du sommet courant,
    puis parmi les sous-voisins des voisins et ainsi de suite.

    Cet algorithme ne prend pas en compte le coût et ne renvoie pas forcément
    le chemin le plus court.
    """
    depart = graphe.depart
    file = deque([depart])
    distances = {depart: 0}
    parents = {depart: None}
    visites = set()
    iteration = 0

    # L'ordre de l'algorithme est basé sur une file,
    # car on visite les voisins directs en premier (principe FIFO),
    # puis les sous-voisins et ainsi de suite.
    while file:
        courant = file.popleft()
        if courant is None :
            continue
        visites.add(courant)

        yield {
            "iteration": iteration, # Étape actuelle de l'algorithme
            "courant": courant, # Sommet courant de l'itération
            "ouverts": set(file), # Sommets non-visités
            "fermes": visites.copy(), # Sommets déjà visités
            "distances": distances.copy(), # Distances à partir du départ
            "parents": parents.copy() # Sommet précédent sur le chemin
        }

        # Quand l'arrivée est atteinte, on interrompt l'algorithme
        # car il s'agit d'un algorithme de recherche
        # et que l'on veut seulement trouver *un* chemin lors de l'affichage.
        if courant == graphe.arrivee:
            return

        for v in graphe.obtenir_voisins(courant):
            # On ne récupère pas les sommets déjà visités
            # ou bloqués (non-visitables).
            if graphe.obtenir_sommet(v).bloque or v in visites:
                continue
            distances[v] = distances[courant] + graphe.obtenir_cout(v)
            parents[v] = courant
            file.append(v)

def dfs_pas_a_pas(graphe: Graphe):
    """
    Algorithme de recherche de "parcours en profondeur" (*Depth-First Search*).

    Il recherche parmi les sous-voisins récursifs avant de passer
    aux voisins directs du sommet courant, et ainsi de suite.

    Cet algorithme ne prend pas en compte le coût et ne renvoie pas forcément
    le chemin le plus court.
    """
    depart = graphe.depart
    pile = [depart]
    visites = set()
    parents = {depart: None}
    distances = {depart: 0}
    iteration = 0

    # L'ordre de l'algorithme est basé sur une pile,
    # car on visite les sous-voisins qui ont été trouvés
    # le plus récemment d'abord (principe LIFO),
    # puis les voisins directs et leurs sous-voisins, et ainsi de suite.
    while pile:
        courant = pile.pop()

        if courant in visites:
            continue

        visites.add(courant)
        iteration += 1

        yield {
            "iteration": iteration, # Étape actuelle de l'algorithme
            "courant": courant, # Sommet courant de l'itération
            "ouverts": set(pile), # Sommets non-visités
            "fermes": visites.copy(), # Sommets déjà visités
            "distances": distances.copy(), # Distances à partir du départ
            "parents": parents.copy() # Sommet précédent sur le chemin
        }

        # Quand l'arrivée est atteinte, on interrompt l'algorithme
        # car il s'agit d'un algorithme de recherche
        # et que l'on veut seulement trouver *un* chemin lors de l'affichage.
        if courant == graphe.arrivee:
            return

        for v in reversed(graphe.obtenir_voisins(courant)):
            # On ne récupère pas les sommets déjà visités
            # ou bloqués (non-visitables).
            if graphe.obtenir_sommet(v).bloque or v in visites:
                continue
            distances[v] = distances[courant] + graphe.obtenir_cout(v)
            parents[v] = courant
            pile.append(v)

def dijkstra_pas_a_pas(graphe: Graphe):
    """
    Algorithme de plus court chemin pour des graphes
    dont les arêtes ont un poids positif.

    Il procède de manière itérative en sélectionnant
    à chaque étape le noeud le plus proche non encore traité
    pour mettre à jour la distance minimale vers ses voisins.

    Cet algorithme prend en compte les coûts
    donnés par les couleurs de chaque sommet.

    Explication de Yvan Monka :
    https://www.youtube.com/watch?v=rHylCtXtdNs
    """
    depart = graphe.depart
    # Les distances sont initialisées à l'infini puisque
    # l'on ne les connait pas encore.
    distances = {id: math.inf for id in graphe.sommets}
    parents = {depart: None}
    distances[depart] = 0

    ouverts = [(0, depart)]
    fermes = set()
    iteration = 0

    while ouverts:
        dist, u = heapq.heappop(ouverts)
        if u in fermes:
            continue

        fermes.add(u)
        iteration += 1

        yield {
            "iteration": iteration,
            "courant": u,
            "ouverts": {x[1] for x in ouverts},
            "fermes": fermes.copy(),
            "distances": distances.copy(),
            "parents": parents.copy()
        }

        if u == graphe.arrivee:
            return

        for v in graphe.obtenir_voisins(u):
            if graphe.obtenir_sommet(v).bloque:
                continue

            nouveau = distances[u] + graphe.obtenir_cout(v)

            # Si le nouveau coût calculé (à partir d'un autre sommet/chemin)
            # est plus court que le coût déjà enregistré, on le remplace.
            if nouveau < distances[v]:
                distances[v] = nouveau
                parents[v] = u

                # On ajoute à la liste des sommets non-visités
                # la nouvelle distance enregistrée et le voisin.
                # (tuple: nouveau, v)
                heapq.heappush(ouverts, (nouveau, v))

def bellman_ford_pas_a_pas(graphe: Graphe):
    """
    Algorithme de plus court chemin pour des graphes
    dont les arêtes peuvent avoir un poids négatifs.

    Il fonctionne en "relaxant" en plusieurs phases toutes les arêtes du graphe,
    ce qui lui permet de détecter la présence de cycles de poids négatifs
    (cycles dans lesquels le coût serait infiniment diminué)
    qui rendraient le calcul impossible.

    Cet algorithme prend en compte les coûts
    donnés par les couleurs de chaque sommet (toujours positifs).
    """
    depart = graphe.depart
    distances = {id: math.inf for id in graphe.sommets}
    parents = {id: None for id in graphe.sommets}
    distances[depart] = 0

    nb_sommets = len(graphe.sommets)
    tous_les_sommets = list(graphe.sommets.keys())
    iteration = 0

    for phase in range(1, nb_sommets):
        # Si aucun changement de distances n'a été réalisé lors de la phase,
        # l'algorithme s'arrête puisque cela signifie que les chemins
        # les plus courts ont déjà été trouvés.
        changement_dans_phase = False

        for u in tous_les_sommets:
            # Si le sommet n'est pas atteignable, on ne le vérifie pas.
            # Cela inclut les cas où le sommet est bloqué
            # et les cas où le sommet n'a pas encore de chemin.
            if graphe.obtenir_sommet(u).bloque or distances[u] == math.inf:
                continue

            for v in graphe.obtenir_voisins(u):
                if graphe.obtenir_sommet(v).bloque:
                    continue

                nouveau_score = distances[u] + graphe.obtenir_cout(v)

                # Si le nouveau coût calculé (à partir d'un autre sommet/chemin)
                # est plus court que le coût déjà enregistré, on le remplace.
                if nouveau_score < distances[v]:
                    distances[v] = nouveau_score
                    parents[v] = u
                    changement_dans_phase = True
                    iteration += 1

                    yield {
                        "iteration": iteration,
                        "phase": phase,
                        "courant": u,
                        "destination": v,
                        "distances": distances.copy(),
                        "parents": parents.copy(),
                        # "cycle_negatif" est constamment à False
                        # car les graphes représentés dans cette application
                        # n'ont pas de coûts négatifs.
                        "cycle_negatif": False
                    }

        if not changement_dans_phase:
            break

    for u in tous_les_sommets:
        if distances[u] == math.inf:
            continue

        for v in graphe.obtenir_voisins(u):
            if not graphe.obtenir_sommet(v).bloque:
                if distances[u] + graphe.obtenir_cout(v) < distances[v]:
                    iteration += 1

                    yield {
                        "iteration": iteration,
                        "phase": "Verification",
                        "courant": u,
                        "distances": distances.copy(),
                        "parents": parents.copy(),
                        "cycle_negatif": True
                    }
                    return

def composantes_connexes_pas_a_pas(graphe: Graphe):
    """
    Calcule les composantes connexes du graphe en ignorant les sommets bloqués.
    Génère les états intermédiaires pour visualisation.
    """
    visites = set()
    composantes = {}
    composante_id = 0
    iteration = 0

    for sommet_id in graphe.sommets:
        if sommet_id in visites or graphe.obtenir_sommet(sommet_id).bloque:
            continue

        # Nouvelle composante (regroupement de sommets connectés)
        composante_id += 1
        file = deque([sommet_id])
        composantes[composante_id] = set()

        while file:
            courant = file.popleft()

            if courant in visites:
                continue

            # Marquer le sommet comme visité
            visites.add(courant)
            composantes[composante_id].add(courant)
            iteration += 1

            yield {
                "iteration": iteration,
                "courant": courant,
                "composante_id": composante_id,
                "composantes": {k: v.copy() for k, v in composantes.items()},
                "ouverts": set(file),
                "visites": visites.copy()
            }

            # Exploration des voisins
            for v in graphe.obtenir_voisins(courant):
                # Sommet ajouté s'il n'a pas été visité et n'est pas bloqué
                if v not in visites and not graphe.obtenir_sommet(v).bloque:
                    file.append(v)

def chemin_depuis_parents(
        parents: dict[int, int | None],
        arrivee: int
    ) -> list[int]:
    """
    Fonction reconstruisant le chemin du sommet de départ à celui d'arrivée
    d'un graphe à partir du dictionnaire de parents d'un algorithme.

    :type parents: Dictionnaire issu du résultat d'un algorithme.
    :param parents: Dictionnaire des identifiants des sommets
        et de leurs parents.
    :param arrivee: Identifiant du sommet d'arrivée du graphe.
    """
    # Si le sommet courant (parents[arrivee]) n'a pas de parents,
    # il s'agit du départ.
    if parents[arrivee] is None:
        return [arrivee]

    # Dans le cas général, on ajoute l'identifiant du sommet courant
    # à la liste des précédents (à partir d'un appel récursif).
    return chemin_depuis_parents(parents, parents[arrivee]) + [arrivee]
