# Recueil des besoins

## CHAPITRE 1 : Objectif et portée

L’objectif principal de ce projet est de développer un logiciel permettant de visualiser l’exécution d’algorithmes de théorie des graphes.
L’application doit permettre à l’utilisateur de manipuler un graphe, de choisir des points de départ et d’arrivée, et d’observer pas à pas le fonctionnement des algorithmes.

Le logiciel s’inscrit dans le cadre de la SAE FA3 et vise principalement un usage pédagogique, notamment pour faciliter la compréhension des notions de parcours, de distances et de chemins dans un graphe.

Il n'y a qu'un intervenant :
- **Utilisateur** : utilise l’application pour visualiser les algorithmes et interagir avec le graphe

La portée du système définit les fonctionnalités incluses dans le projet ainsi que les limites de celui‑ci.

**Ce qui entre dans la portée** :
- Création et manipulation d’un graphe
- Choix des points de départ et d’arrivée
- Visualisation d’algorithmes de graphes (Dijkstra, Bellman-Ford, etc.)
- Affichage progressif des résultats

**Ce qui est en dehors de la portée** :
- Stockage des graphes ou des résultats

---

## CHAPITRE 2 : Terminologie employée / Glossaire

Ce glossaire regroupe les termes essentiels liés à la théorie des graphes utilisés dans le projet : 

1. **Graphe**
   - Un graphe est une structure composée de sommets reliés par des arêtes

2. **Sommet**
   - Élément de base du graphe, représenté visuellement par une case (ex : hexagone)
   - Peut être normal (point blanc) ou bloqué (point noir)

3. **Arête**
   - Liaison entre deux sommets, avec un coût associé

4. **Poids**
   - Valeur associée à un déplacement entre deux sommets
   - Exemple : coût 1 pour un déplacement normal, coût plus élevé pour certains sommets de couleurs

5. **Algorithme de graphe**
   - Méthode permettant d’explorer ou d’analyser un graphe (Dijkstra, Bellman-Ford, etc.)

6. **Chemin**
   - Suite de sommets reliant un point de départ à un point d’arrivée

---

## CHAPITRE 3 : Les cas d’utilisation

### (a) L'acteur principale et son objectif général : 

1. **Utilisateur**
   - **Objectif général** :
     - Visualiser l’exécution d’algorithmes de graphes
     - Comprendre le fonctionnement des parcours et du calcul de chemin
   - **Actions possibles** :
     - Choisir des points de départ et d’arrivée
     - Lancer un algorithme
     - Observer le résultat

---

### (b) Les cas d’utilisation métier

#### 1. Utiliser l’application
| **Nom** | Utiliser l’application |
|-------|------------------------|
| **Niveau** | Stratégique |
| **Acteur principal** | Utilisateur |
| **Pré-requis** | Aucun |
| **Scénario nominal** | 1. L’utilisateur choisit les points de départ et d’arrivée <br> 2. L’utilisateur modifie les sommets du graphe <br> 3. L’utilisateur lance l’algorithme de son choix <br> 4. Le résultat s’affiche |
| **Scénario alternatif** | |
| **Scénario exceptionnel** | |

#### 2. Modifier les sommets du graphe
| **Nom** | Modifier les sommets du graphe |
|-------|-------------------------------|
| **Niveau** | Utilisateur |
| **Acteur principal** | Utilisateur |
| **Pré-requis** | Aucun |
| **Scénario nominal** | 1. L’utilisateur ajoute des points noirs (sommets non‑traversables) sur la grille <br> 2. L’utilisateur ajoute des points de couleur représentant des distances plus élevées |
| **Scénario alternatif** | |
| **Scénario exceptionnel** | |

#### 3. Choisir les points de départ et d’arrivée
| **Nom** | Choisir les points de départ et d’arrivée |
|-------|------------------------------------------|
| **Niveau** | Utilisateur |
| **Acteur principal** | Utilisateur |
| **Scénario nominal** | 1. L’utilisateur place le point de départ sur la grille <br> 2. L’utilisateur place le point d’arrivée sur la grille |
| **Scénario alternatif** | Les points ne sont pas placés <br> → Le système définit automatiquement un point de départ et d’arrivée |
| **Scénario exceptionnel** | |

#### 4. Lancer un algorithme
| **Nom** | Lancer un algorithme |
|-------|---------------------|
| **Niveau** | Utilisateur |
| **Acteur principal** | Utilisateur |
| **Pré-requis** | Points de départ et d’arrivée définis |
| **Scénario nominal** | 1. L’utilisateur sélectionne un algorithme <br> 2. L’utilisateur exécute l’algorithme |
| **Scénario alternatif** | |
| **Scénario exceptionnel** | |

#### 5. Afficher le résultat
| **Nom** | Afficher le résultat |
|-------|---------------------|
| **Niveau** | Sous-fonction |
| **Acteur principal** | Système |
| **Pré-requis** | Un algorithme a été lancé |
| **Scénario nominal** | 1. Le programme affiche progressivement les sommets explorés <br> 2. Le programme met en évidence le chemin trouvé |
| **Scénario alternatif** | |
| **Scénario exceptionnel** | |

#### 6. Utiliser l’application – Chemin impossible
| **Nom** | Utiliser l’application – Chemin impossible |
|-------|--------------------------------------------|
| **Niveau** | Stratégique |
| **Acteur principal** | Utilisateur |
| **Pré-requis** | Un graphe est affiché <br> Certains sommets sont bloqués |
| **Scénario nominal** | 1. Choisir un point de départ et d’arrivée <br> 2. Placer des sommets bloqués <br> 3. Lancer un algorithme <br> 4. Visualiser que l’arrivée est inatteignable |
| **Scénario alternatif** | |
| **Scénario exceptionnel** | |


---

## CHAPITRE 4 : La technologie employée

- **Langage** : Python  
- **Interface graphique** : Tkinter 
- **Environnement d’exécution** : Ordinateur local (Windows)
- **Versioning** : Git (GitHub)

---

## CHAPITRE 5 : Autres exigences

### (a) Processus de développement

#### i) Participants
Le projet est réalisé par un groupe d’étudiants travaillant en collaboration sur toutes les phases du projet.

#### ii) Valeurs privilégiées
- Clarté du code
- Simplicité d’utilisation
- Aspect pédagogique

#### iii) Visibilité du projet
- Code source disponible sur GitHub
- Documentation du code

#### iv) Achats / concurrence
Aucun.

#### v) Autres exigences
- Projet compréhensible en soutenance

---

Les autres rubriques ainsi que le **Chapitre 6** ne sont pas traités, le projet étant réalisé dans un cadre universitaire.
