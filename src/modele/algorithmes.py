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

def dfs_pas_a_pas(graphe: Graphe):
    depart = graphe.depart
    pile = [depart]
    visites = set()
    parents = {depart: None}

    while pile:
        courant = pile.pop()

        if courant in visites:
            continue

        visites.add(courant)

        yield {
            "courant": courant,
            "ouverts": set(pile),
            "fermes": visites.copy(),
            "parents": parents.copy()
        }

        for v in reversed(graphe.obtenir_voisins(courant)):
            if graphe.obtenir_sommet(v).bloque or v in visites:
                continue
            parents[v] = courant
            pile.append(v)

def dijkstra_pas_a_pas(graphe: Graphe):
    depart = graphe.depart
    distances = {id: math.inf for id in graphe.sommets}
    parents = {depart: None}
    distances[depart] = 0

    ouverts = [(0, depart)]
    fermes = set()

    while ouverts:
        dist, u = heapq.heappop(ouverts)
        if u in fermes:
            continue

        fermes.add(u)

        yield {
            "courant": u,
            "ouverts": {x[1] for x in ouverts},
            "fermes": fermes.copy(),
            "distances": distances.copy(),
            "parents": parents.copy()
        }

        for v in graphe.obtenir_voisins(u):
            if graphe.obtenir_sommet(v).bloque:
                continue

            nouveau = distances[u] + graphe.obtenir_cout(v)
            if nouveau < distances[v]:
                distances[v] = nouveau
                parents[v] = u
                heapq.heappush(ouverts, (nouveau, v))