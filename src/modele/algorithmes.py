from .graphe import Graphe, Sommet
from collections import deque

def bfs_pas_a_pas(graphe: Graphe):
    depart = graphe.depart
    file = deque([depart])
    distances = {depart: 0}
    parents = {depart: None}
    visites = set()

    while file:
        courant = file.popleft()
        if courant is None :
            continue
        visites.add(courant)

        yield {
            "courant": courant,
            "ouverts": set(file),
            "fermes": visites.copy(),
            "distances": distances.copy(),
            "parents": parents.copy()
        }
        for v in graphe.obtenir_voisins(courant):
            if graphe.obtenir_sommet(v).bloque or v in distances:
                continue
            distances[v] = distances[courant] + 1
            parents[v] = courant
            file.append(v)
