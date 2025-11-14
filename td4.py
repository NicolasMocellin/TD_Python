import numpy as np
import matplotlib.pyplot as plt
import trimesh
from geometry import *

# TD4 : Tessellation et raffinement de maillage
# ==============================================

# PARTIE 1 : Tessellation d'un triangle
# --------------------------------------

# 1. Coder une fonction tessellation_triangle qui subdivise un triangle en
#    4 sous-triangles de taille égale.
#
#    Principe : Ajouter 3 nouveaux sommets au milieu de chaque arête, puis
#               créer 4 nouveaux triangles.
#
#    Entrées :
#    - ind : indice du triangle à subdiviser
#    - sommets, triangles : les matrices de l'objet
#
#    Sorties :
#    - nouveaux_sommets : les 3 points au milieu des arêtes
#    - nouveaux_triangles : les 4 triangles qui remplaceront l'ancien
#
# 2. TEST : Tester sur un triangle simple

A = np.array([0, 0, 0])
B = np.array([2, 0, 0])
C = np.array([1, 1, 3])
s1 = np.array([A, B, C])
t1 = np.array([[0, 1, 2]])
s2, t2 = tessellation_triangle(0, s1, t1)
s = np.vstack([s1, s2])
t = t2
fig, ax = figure()
affichage_objet(s, t, ax)
plt.show()


# PARTIE 2 : Tessellation d'un objet complet
# -------------------------------------------

# 1. Coder une fonction tessellation_objet qui raffine un maillage en
#    subdivisant récursivement tous les triangles dont la surface dépasse
#    un seuil donné.
#
#    Entrées :
#    - sommets, triangles : les matrices de l'objet
#    - surf_min : surface minimale en dessous de laquelle on arrête de subdiviser
#
#    Sorties :
#    - sommets_out, triangles_out : le maillage raffiné
#
#    Algorithme :
#    - Parcourir tous les triangles
#    - Si un triangle a une surface > surf_min :
#        * Le subdiviser avec tessellation_triangle
#        * Ajouter les nouveaux sommets et triangles
#        * Supprimer l'ancien triangle
#    - Continuer jusqu'à ce que tous les triangles respectent le critère
#
# 2. Coder une fonction calcul_surface_triangle qui calcule l'aire d'un triangle
#
# 3. TEST : Tester sur un triangle simple avec surf_min = 0.1

s, t = tessellation_objet(s1, t1, 0.1)
fig, ax = figure()
affichage_objet(s, t, ax)
plt.show()


# PARTIE 3 : Ajout d'un sol sous le bâtiment
# -------------------------------------------

# 1. Coder une fonction creer_sol qui crée un plan rectangulaire horizontal
#    défini par deux coins opposés.
#
# 2. Coder une fonction creer_concatenation qui fusionne deux objets maillés
#    en un seul.
#
#    Principe :
#    - Concaténer les matrices de sommets
#    - Concaténer les matrices de triangles en ajustant les indices du
#      second objet pour pointer vers les bons sommets
#
# 3. TEST : Créer un sol sous le bâtiment
#    - Charger building.stl
#    - Calculer les dimensions du bâtiment (pmin, pmax)
#    - Créer un sol légèrement plus grand que le bâtiment
#    - Fusionner le bâtiment et le sol avec creer_concatenation
#    - Calculer l'éclairement avec ombres
#    - Afficher le résultat

stl_mesh = trimesh.load('building.stl')

pmax = np.max(stl_mesh.vertices, axis=0)
source = pmax * 3
source[1] = -source[1]

pmin = np.min(stl_mesh.vertices, axis=0)
h0 = pmin[2]
delta = np.linalg.norm(pmax - pmin)
pmin_sol = pmin - 1 * delta
pmax_sol = pmax + 1 * delta
pmax_sol[2] = h0
pmin_sol[2] = h0

s_sol, t_sol = creer_sol(pmin_sol, pmax_sol)
s, t = creer_concatenation(stl_mesh.vertices, stl_mesh.faces, s_sol, t_sol)
E = calcul_eclairement_objet(s, t, source)

fig, ax = figure()
affichage_objet_eclaire(s, t, E, source, ax)
plt.show()


# PARTIE 4 : Modélisation de l'éclairage du bâtiment avec tessellation
# ---------------------------------------------------------------------

# Objectif : Obtenir un rendu d'éclairage de meilleure qualité en raffinant
#            le maillage du bâtiment.
#
# 1. Calculer une surface minimale appropriée en fonction des dimensions
#    du bâtiment.
#
#    Stratégie suggérée :
#    - Trouver la surface du plus grand triangle du bâtiment (s_max)
#    - Choisir surf_min = s_max / 10 (ou une autre fraction)
#
#    Cela permet d'avoir une tessellation adaptée à la taille de l'objet.
#
# 2. Appliquer la tessellation sur l'ensemble bâtiment + sol
#
# 3. Calculer l'éclairement avec ombres sur le maillage raffiné
#
# 4. Afficher le résultat final
#
# Observer : Le rendu d'éclairage devrait être plus précis grâce au
#            maillage plus fin.

s_max = 0
for i in range(len(stl_mesh.faces)):
    A, B, C = recupere_sommets(i, stl_mesh.vertices, stl_mesh.faces)
    surf = calcul_surface_triangle(A, B, C)
    if surf > s_max:
        s_max = surf

s_min = s_max / 5

s_final, t_final = tessellation_objet(s, t, s_min)
E = calcul_eclairement_objet(s_final, t_final, source)

fig, ax = figure()
affichage_objet_eclaire(s_final, t_final, E, source, ax)
plt.show()
