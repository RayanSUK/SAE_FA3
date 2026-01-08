import heapq
import math
from .graphe import Graphe, Sommet
from collections import deque

def bfs_pas_a_pas(graphe: Graphe):
    depart = graphe.depart
    file = deque([depart])
    distances = {depart: 0}
    parents = {depart: None}
    visites = set()
    iteration = 0

    while file:
        courant = file.popleft()
        if courant is None :
            continue
        visites.add(courant)

        yield {
            "iteration": iteration,
            "courant": courant,
            "ouverts": set(file),
            "fermes": visites.copy(),
            "distances": distances.copy(),
            "parents": parents.copy()
        }

        if courant == graphe.arrivee:
            return
        
        for v in graphe.obtenir_voisins(courant):
            if graphe.obtenir_sommet(v).bloque or v in visites:
                continue
            distances[v] = distances[courant] + graphe.obtenir_cout(v)
            parents[v] = courant
            file.append(v)

def dfs_pas_a_pas(graphe: Graphe):
    depart = graphe.depart
    pile = [depart]
    visites = set()
    parents = {depart: None}
    distances = {depart: 0}
    iteration = 0

    while pile:
        courant = pile.pop()

        if courant in visites:
            continue

        visites.add(courant)
        iteration += 1

        yield {
            "iteration": iteration,
            "courant": courant,
            "ouverts": set(pile),
            "fermes": visites.copy(),
            "distances": distances.copy(),
            "parents": parents.copy()
        }

        if courant == graphe.arrivee:
            return
        
        for v in reversed(graphe.obtenir_voisins(courant)):
            if graphe.obtenir_sommet(v).bloque or v in visites:
                continue
            distances[v] = distances[courant] + graphe.obtenir_cout(v)
            parents[v] = courant
            pile.append(v)

def dijkstra_pas_a_pas(graphe: Graphe):
    depart = graphe.depart
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
            if nouveau < distances[v]:
                distances[v] = nouveau
                parents[v] = u
                heapq.heappush(ouverts, (nouveau, v))

def bellman_ford_pas_a_pas(graphe: Graphe):
    depart = graphe.depart
    distances = {id: math.inf for id in graphe.sommets}
    parents = {id: None for id in graphe.sommets}
    distances[depart] = 0

    nb_sommets = len(graphe.sommets)
    tous_les_sommets = list(graphe.sommets.keys())
    iteration = 0

    for phase in range(1, nb_sommets):
        changement_dans_phase = False

        for u in tous_les_sommets:
            if graphe.obtenir_sommet(u).bloque or distances[u] == math.inf:
                continue

            for v in graphe.obtenir_voisins(u):
                if graphe.obtenir_sommet(v).bloque: continue

                nouveau_score = distances[u] + graphe.obtenir_cout(v)

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
                        "cycle_negatif": False
                    }

        if not changement_dans_phase:
            break

    for u in tous_les_sommets:
        if distances[u] == math.inf: continue
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

def chemin_depuis_parents(parents: dict[int, int | None], arrivee: int) -> list[int]:
    """
    Reconstruit le chemin depuis la table des parents.
    """
    if parents[arrivee] is None:
        return [arrivee]
    return chemin_depuis_parents(parents, parents[arrivee]) + [arrivee]
