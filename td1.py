import numpy as np
import matplotlib.pyplot as plt
from geometry import *

# TD1 : Manipulation de triangles et objets 3D
# =============================================

# PARTIE 1 : Triangle simple
# --------------------------

# Un triangle est défini par 3 sommets (x,y,z) stockés dans 3 vecteurs [1x3]

# 1. Coder une fonction calcul_centre_de_gravite qui retourne le centre de
#    gravité d'un triangle

# 2. Coder une fonction calcul_normale_triangle qui retourne la normale
#    (de norme 1) d'un triangle

# 3. Coder une fonction affichage_triangle qui affiche dans la figure
#    courante un triangle et sa normale (partant de son centre de gravité).
#    Utiliser plot3 pour le triangle et quiver3 pour la normale

# 4. TEST
#    - Définir 3 points
#    - Créer une figure avec figure()
#    - Appeler affichage_triangle

# ECRIRE LE TEST ICI
p1 = np.array([0, 0, 0])
p2 = np.array([2, 0, 0])
p3 = np.array([1, 1, 3])
fig, ax = figure()
affichage_triangle(p1, p2, p3, ax)
set_axes_equal(ax)
plt.show()


# PARTIE 2 : Pyramide à base carrée
# ----------------------------------

# Se référer à l'énoncé du TD pour comprendre comment un objet
# polyhédrique est défini par une matrice 'sommets' et une matrice
# 'triangles'.
#
# Un objet 3D est représenté par :
#   - sommets : matrice (N x 3) où chaque ligne contient les coordonnées
#               (x, y, z) d'un sommet
#   - triangles : matrice (M x 3) où chaque ligne contient les indices
#                 de 3 sommets formant un triangle

# 1. Coder une fonction creer_pyramide qui prend 2 paramètres (taille de la
#    base et hauteur) et qui retourne les matrices sommets et triangles d'une
#    pyramide à base carrée

# 2. Coder une fonction affichage_objet qui prend en paramètre les matrices
#    sommets et triangles d'un objet et qui se sert de affichage_triangle pour
#    afficher l'objet et les normales de tous les triangles

# 3. Coder une fonction recupere_sommets qui extrait les coordonnées des 3
#    sommets d'un triangle à partir de son indice

# 4. TEST
#    - Créer une pyramide avec creer_pyramide
#    - Créer une figure avec figure()
#    - Afficher la pyramide avec affichage_objet

# ECRIRE LE TEST ICI
base = 6
height = 8
s, t = creer_pyramide(base, height)
fig, ax = figure()
affichage_objet(s, t, ax)
plt.show()
