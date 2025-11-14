import numpy as np
import matplotlib.pyplot as plt
import trimesh
from geometry import *

# TD3 : Calcul des ombres par intersection rayon-triangle
# ========================================================

# PARTIE 1 : Intersection segment-triangle (Bonus)
# ------------------------------------------------

# Optionnel pour les étudiants en avance : utiliser la description de l'algorithme
# dans Calcul_Intersection_Triangle_Segment.pdf pour coder une fonction qui teste
# si un segment intersecte un triangle.
#
# La fonction doit retourner :
#   - test : booléen indiquant si une intersection existe
#   - I : point d'intersection (si il existe)


# PARTIE 2 : Tests d'intersection segment/triangle
# ------------------------------------------------

# Écrire un script qui permet de tester le fonctionnement de la fonction
# calcul_intersection_triangle_segment. Ne pas oublier de tester les cas
# particuliers :
#   - Segments qui intersectent le triangle
#   - Segments qui passent à côté
#   - Segments qui passent par les sommets ou les arêtes
#   - Segments parallèles au plan du triangle

# ECRIRE LE TEST ICI
A = np.array([0, 0, 0])
B = np.array([2, 0, 0])
C = np.array([1, 1, 3])
fig, ax = figure()
affichage_triangle(A, B, C, ax)
source = np.array([1, -6, 1])
points = []
y = 2
for x in np.arange(-1, 4, 1.8):
    for z in np.arange(-1, 4, 1.8):
        points.append([x, y, z])

points.extend([
    (A + B) / 2,
    (B + C) / 2,
    (A + C) / 2,
    A,
    B,
    C
])

points = np.array(points)

for i in range(len(points)):
    test, I = calcul_intersection_triangle_segment(A, B, C, source, points[i])
    if test:
        ax.plot([source[0], I[0]], [source[1], I[1]], [source[2], I[2]],
                'green', linewidth=2)
        ax.scatter(I[0], I[1], I[2], color='green', s=50)
    else:
        ax.plot([source[0], points[i, 0]], [source[1], points[i, 1]],
                [source[2], points[i, 2]], 'red', linewidth=1, alpha=0.5)

plt.show()


# PARTIE 3 : Calcul des éclairements avec ombres
# -----------------------------------------------

# 1. Coder une fonction calcul_eclairement_objet qui prend en paramètre
#    les matrices sommets et triangles d'un objet et une source lumineuse,
#    et qui renvoie l'éclairement de chaque triangle EN TENANT COMPTE des
#    ombres portées.
#
#    Algorithme :
#    - Pour chaque triangle, calculer son éclairement direct
#    - Si le triangle est éclairé (éclairement > 0) :
#        * Tracer un rayon entre le centre du triangle et la source
#        * Tester si ce rayon intersecte un autre triangle
#        * Si oui, le triangle est à l'ombre : éclairement = 0
#
#    UTILISER la fonction calcul_intersection_triangle_segment pour
#    détecter les intersections

# 2. TEST
#    Tester ce nouveau calcul d'éclairement sur building.stl
#    - Charger le fichier avec numpy-stl
#    - Définir une position de source
#    - Calculer l'éclairement avec calcul_eclairement_objet (avec ombres)
#    - Afficher le résultat

# ECRIRE LE TEST ICI
stl_mesh = trimesh.load('building.stl')

pmax = np.max(stl_mesh.vertices, axis=0)
source = pmax * 3
source[1] = -source[1]
E = calcul_eclairement_objet(stl_mesh.vertices, stl_mesh.faces, source)
fig, ax = figure()
affichage_objet_eclaire(stl_mesh.vertices, stl_mesh.faces, E, source, ax)
plt.show()
