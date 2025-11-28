import numpy as np
import matplotlib.pyplot as plt
import trimesh
from geometry import *

# TD2 : Calcul et affichage de l'éclairement des triangles
# =========================================================

# PARTIE 1 : Éclairement sans ombres
# -----------------------------------

# 1. Coder une fonction calcul_eclairement_triangle qui prend en paramètre
#    les 3 sommets d'un triangle et une source lumineuse (vecteur [1x3])
#    et qui renvoie l'éclairement normalisé du triangle (entre 0 et 1).
#
#    L'éclairement dépend de l'angle entre :
#    - la normale au triangle
#    - le vecteur allant du centre du triangle vers la source
#
#    Formule : E = max(0, cos(θ)) où θ est l'angle entre la normale et
#              le vecteur vers la source

# 2. Coder une fonction calcul_eclairement_objet_simple qui calcule
#    l'éclairement d'un objet entier (SANS tenir compte des ombres portées).
#    Elle doit retourner un vecteur contenant l'éclairement de chaque triangle.

# 3. Coder une fonction affichage_objet_eclaire qui prend en paramètre les
#    matrices sommets et triangles d'un objet, la source et les valeurs
#    d'éclairement, et qui affiche l'objet coloré selon son éclairement.
#    Utiliser Poly3DCollection avec 'facecolors' pour les couleurs.

# 4. TEST sur la pyramide
#    - Créer une pyramide avec creer_pyramide
#    - Définir une position de source lumineuse
#    - Calculer le vecteur E d'éclairement avec calcul_eclairement_objet_simple
#    - Créer une figure avec figure()
#    - Afficher le résultat avec affichage_objet_eclaire

# ECRIRE LE TEST ICI
base = 6
height = 8
s, t = creer_pyramide(base, height)
source = np.array([-10, 6, 10])
E = calcul_eclairement_objet_simple(s, t, source)
fig, ax = figure()
affichage_objet_eclaire(s, t, E, source, ax)
plt.show()


# PARTIE 2 : Test sur un objet STL
# ---------------------------------

# 1. Utiliser numpy-stl pour charger le fichier 'building.stl'
#    Le résultat contient :
#    - stl_mesh.vectors : les triangles avec leurs coordonnées de sommets
#
#    Note : Il faut extraire et dédupliquer les sommets pour obtenir
#           la structure sommets/triangles

# 2. Positionner une source lumineuse en fonction de la taille du bâtiment
#    Astuce : utiliser np.max(sommets, axis=0) pour connaître les dimensions et
#             placer la source à une distance proportionnelle

# 3. Calculer l'éclairement avec calcul_eclairement_objet_simple

# 4. Afficher le bâtiment éclairé avec affichage_objet_eclaire

# ECRIRE LE TEST ICI
stl_mesh = trimesh.load('building.stl')

pmax = np.max(stl_mesh.vertices, axis=0)
source = pmax * 3
source[1] = -source[1]
E = calcul_eclairement_objet_simple(stl_mesh.vertices, stl_mesh.faces, source)
fig, ax = figure()
affichage_objet_eclaire(stl_mesh.vertices, stl_mesh.faces, E, source, ax)
plt.show()


# PARTIE 3 : Bonus
# -----------------

# Optionnel : afficher également le bâtiment avec affichage_objet pour
# visualiser toutes les normales des triangles.
#
# Note : Il faudra que affichage_triangle adapte la longueur des normales
#        affichées en fonction de la taille du triangle pour qu'elles restent
#        visibles quelle que soit la taille de l'objet.

fig, ax = figure()
affichage_objet(stl_mesh.vertices, stl_mesh.faces, ax)
plt.show()
