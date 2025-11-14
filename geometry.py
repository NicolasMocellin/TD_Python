"""
Geometry and rendering functions for 3D triangle mesh processing.

This module provides all the core functionality for:
- Triangle geometry computations (centroid, normal, area)
- Object creation (pyramid, ground plane, mesh concatenation)
- Rendering and display (triangles, meshes, lighting)
- Lighting simulation (with and without shadows)
- Ray tracing (ray-triangle intersection)
- Mesh refinement (adaptive tessellation)
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from tqdm import tqdm

# ============================================================================
# GEOMETRY PRIMITIVES (Triangle operations)
# ============================================================================

def calcul_centre_de_gravite(A, B, C):
    """
    Calculate the centroid (center of gravity) of a triangle.

    Parameters:
    -----------
    A, B, C : array-like, shape (3,)
        Coordinates of the three vertices (x, y, z)

    Returns:
    --------
    G : ndarray, shape (3,)
        Centroid coordinates
    """
    return (A + B + C) / 3


def calcul_normale_triangle(A, B, C):
    """
    Calculate the unit normal vector of a triangle.

    Parameters:
    -----------
    A, B, C : array-like, shape (3,)
        Coordinates of the three vertices (x, y, z)

    Returns:
    --------
    normale : ndarray, shape (3,)
        Unit normal vector
    """
    AB = B - A
    AC = C - A
    normale = np.cross(AB, AC)
    return normale / np.linalg.norm(normale)


def calcul_surface_triangle(A, B, C):
    """
    Calculate the area of a triangle.

    Parameters:
    -----------
    A, B, C : array-like, shape (3,)
        Coordinates of the three vertices (x, y, z)

    Returns:
    --------
    surface : float
        Area of the triangle
    """
    AB = B - A
    AC = C - A
    return np.linalg.norm(np.cross(AB, AC)) * 0.5


def recupere_sommets(ind, sommets, triangles):
    """
    Extract the coordinates of the three vertices of a triangle.

    Parameters:
    -----------
    ind : int
        Index of the triangle in the triangles matrix
    sommets : ndarray, shape (N, 3)
        Vertex coordinates matrix
    triangles : ndarray, shape (M, 3)
        Triangle indices matrix

    Returns:
    --------
    A, B, C : ndarray, shape (3,)
        Coordinates of the three vertices
    """
    i_A, i_B, i_C = triangles[ind]
    A = sommets[i_A]
    B = sommets[i_B]
    C = sommets[i_C]
    return A, B, C


# ============================================================================
# OBJECT CREATION
# ============================================================================

def creer_pyramide(base, hauteur):
    """
    Create a square-based pyramid centered at the origin.

    Parameters:
    -----------
    base : float
        Side length of the square base
    hauteur : float
        Height of the pyramid (along z-axis)

    Returns:
    --------
    sommets : ndarray, shape (5, 3)
        Coordinates of the 5 vertices
    triangles : ndarray, shape (6, 3)
        Triangle indices (2 for base, 4 for sides)
    """
    b = base
    h = hauteur

    sommets = np.array([
        [0, 0, 0],
        [b, 0, 0],
        [b, b, 0],
        [0, b, 0],
        [b/2, b/2, h]
    ])

    triangles = np.array([
        [0, 2, 1],
        [0, 3, 2],
        [4, 0, 1],
        [4, 1, 2],
        [4, 2, 3],
        [4, 3, 0]
    ], dtype=int)

    return sommets, triangles


def creer_sol(p1, p2):
    """
    Create a rectangular ground plane defined by two opposite corners.

    Parameters:
    -----------
    p1, p2 : array-like, shape (3,)
        Two opposite corners of the rectangle.
        The z-coordinate defines the altitude of the ground.

    Returns:
    --------
    sommets : ndarray, shape (4, 3)
        Coordinates of the 4 corners
    triangles : ndarray, shape (2, 3)
        Triangle indices forming the ground
    """
    p1, p2 = np.array(p1), np.array(p2)

    sommets = np.array([
        p1,
        [p2[0], p1[1], p1[2]],
        p2,
        [p1[0], p2[1], p1[2]]
    ])

    triangles = np.array([
        [0, 1, 2],
        [0, 2, 3]
    ], dtype=int)

    return sommets, triangles


def creer_concatenation(s1, t1, s2, t2):
    """
    Merge two meshes into a single mesh.

    Parameters:
    -----------
    s1, t1 : ndarray
        Vertices and triangles of the first mesh
    s2, t2 : ndarray
        Vertices and triangles of the second mesh

    Returns:
    --------
    sommets : ndarray
        Combined vertices
    triangles : ndarray
        Combined triangles with adjusted indices for second mesh
    """
    sommets = np.vstack([s1, s2])
    n = len(s1)
    triangles = np.vstack([t1, t2 + n])
    return sommets, triangles


# ============================================================================
# RENDERING AND DISPLAY
# ============================================================================

def set_axes_equal(ax):
    """
    Set equal aspect ratio for 3D axes by computing equal limits.

    Uses the current axis limits (based on plotted data) and adjusts them
    to have equal scales in all three dimensions.

    Parameters:
    -----------
    ax : matplotlib 3D Axes
        The axes to configure
    """
    # Get current data limits
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    z_min, z_max = ax.get_zlim()

    # Calculate the range for each axis
    x_range = x_max - x_min
    y_range = y_max - y_min
    z_range = z_max - z_min

    # Find the maximum range
    max_range = max(x_range, y_range, z_range)

    # Calculate centers
    x_center = (x_max + x_min) / 2
    y_center = (y_max + y_min) / 2
    z_center = (z_max + z_min) / 2

    # Set limits with equal range around center
    ax.set_xlim(x_center - max_range/2, x_center + max_range/2)
    ax.set_ylim(y_center - max_range/2, y_center + max_range/2)
    ax.set_zlim(z_center - max_range/2, z_center + max_range/2)

    ax.set_box_aspect([1, 1, 1])


def figure():
    """
    Create and configure a new 3D figure with standard settings.

    Returns:
    --------
    fig : matplotlib Figure
        The created figure
    ax : matplotlib 3D Axes
        The 3D axes
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    #ax.set_box_aspect([1, 1, 1])
    ax.grid(True)
    return fig, ax


def affichage_triangle(A, B, C, ax=None):
    """
    Display a triangle in 3D with its normal vector.

    Parameters:
    -----------
    A, B, C : array-like, shape (3,)
        Coordinates of the three vertices
    ax : matplotlib 3D Axes, optional
        The axes to draw on. If None, uses current axes.
    """
    if ax is None:
        ax = plt.gca()

    # Draw triangle edges
    triangle = np.array([A, B, C, A])
    ax.plot(triangle[:, 0], triangle[:, 1], triangle[:, 2], 'blue')

    # Calculate and draw normal
    G = calcul_centre_de_gravite(A, B, C)
    H = calcul_normale_triangle(A, B, C)

    # Scale normal to 30% of edge length for visibility
    H = H * np.linalg.norm(A - B) * 0.3

    ax.quiver(G[0], G[1], G[2], H[0], H[1], H[2], color='red', arrow_length_ratio=0.1)


def affichage_objet(sommets, triangles, ax=None):
    """
    Display a polyhedral object with normals for all triangles.

    Parameters:
    -----------
    sommets : ndarray, shape (N, 3)
        Vertex coordinates
    triangles : ndarray, shape (M, 3)
        Triangle indices
    ax : matplotlib 3D Axes, optional
        The axes to draw on. If None, uses current axes.
    """
    if ax is None:
        ax = plt.gca()

    nb_tri = len(triangles)
    for i in range(nb_tri):
        A, B, C = recupere_sommets(i, sommets, triangles)
        affichage_triangle(A, B, C, ax)
    set_axes_equal(ax)


def affichage_objet_eclaire(sommets, triangles, couleurs, source, ax=None):
    """
    Display a polyhedral object with colored lighting and light source.

    Parameters:
    -----------
    sommets : ndarray, shape (N, 3)
        Vertex coordinates
    triangles : ndarray, shape (M, 3)
        Triangle indices
    couleurs : ndarray, shape (M,)
        Normalized lighting values for each triangle (0 to 1)
    source : array-like, shape (3,)
        Light source coordinates
    ax : matplotlib 3D Axes, optional
        The axes to draw on. If None, uses current axes.
    """
    if ax is None:
        ax = plt.gca()

    # Create triangle collection with colors
    verts = [[sommets[t[0]], sommets[t[1]], sommets[t[2]]] for t in triangles]
    collection = Poly3DCollection(verts, facecolors=plt.cm.hot(couleurs),
                                   edgecolors='k', linewidths=0.1, alpha=0.9)
    ax.add_collection3d(collection)

    # Display light source
    ax.scatter(*source, color='yellow', s=200, marker='*', edgecolors='black', linewidths=2)

    # Set axis limits with equal scales (based on all plotted data)
    set_axes_equal(ax)


# ============================================================================
# LIGHTING SIMULATION
# ============================================================================

def calcul_eclairement_triangle(A, B, C, source):
    """
    Calculate normalized direct lighting for a triangle.

    Parameters:
    -----------
    A, B, C : array-like, shape (3,)
        Coordinates of the three vertices
    source : array-like, shape (3,)
        Light source coordinates

    Returns:
    --------
    E : float
        Normalized lighting value (0 to 1)
        E = max(0, cos(θ)) where θ is the angle between normal and light direction
    """

    # Calculate triangle centroid
    G = calcul_centre_de_gravite(A, B, C)

    # Vector from centroid to source
    vecteur_rayon = source - G
    d = np.linalg.norm(vecteur_rayon)

    # Triangle normal (unit vector)
    normale = calcul_normale_triangle(A, B, C)

    # Cosine of angle between normal and light ray
    costheta = np.dot(vecteur_rayon, normale) / d

    # Normalized lighting (no negative values)
    E = max(0, costheta)

    return E


def calcul_eclairement_objet_simple(sommets, triangles, source):
    """
    Calculate direct lighting for all triangles WITHOUT shadows.

    Parameters:
    -----------
    sommets : ndarray, shape (N, 3)
        Vertex coordinates
    triangles : ndarray, shape (M, 3)
        Triangle indices
    source : array-like, shape (3,)
        Light source coordinates

    Returns:
    --------
    E : ndarray, shape (M,)
        Normalized lighting values for each triangle (0 to 1)
    """
    nb_tri = len(triangles)
    E = np.zeros(nb_tri)

    for i in range(nb_tri):
        A, B, C = recupere_sommets(i, sommets, triangles)
        E[i] = calcul_eclairement_triangle(A, B, C, source)

    return E


def calcul_eclairement_objet(sommets, triangles, source):
    """
    Calculate lighting for all triangles WITH shadow computation.

    For each triangle:
    1. Calculate base lighting based on angle to light source
    2. If facing light, test ray from triangle centroid to source
    3. Check intersection against all other triangles
    4. Set lighting to 0 if any triangle blocks the light

    Parameters:
    -----------
    sommets : ndarray, shape (N, 3)
        Vertex coordinates
    triangles : ndarray, shape (M, 3)
        Triangle indices
    source : array-like, shape (3,)
        Light source coordinates

    Returns:
    --------
    E : ndarray, shape (M,)
        Normalized lighting values for each triangle (0 to 1)
        Triangles in shadow have value 0
    """
    nb_tri = len(triangles)
    E = np.zeros(nb_tri)

    for i in tqdm(range(nb_tri), desc="Calcul de l'éclairement"):
        A, B, C = recupere_sommets(i, sommets, triangles)
        E[i] = calcul_eclairement_triangle(A, B, C, source)

        if E[i] > 0:  # If triangle faces the light
            G = calcul_centre_de_gravite(A, B, C)

            # Test intersection with all other triangles
            for j in range(nb_tri):
                if i != j:  # Don't test triangle with itself
                    a, b, c = recupere_sommets(j, sommets, triangles)
                    test, I = calcul_intersection_triangle_segment(a, b, c, G, source)

                    if test:
                        # Intersection found: triangle is in shadow
                        E[i] = 0
                        break  # No need to test other triangles

    return E


# ============================================================================
# RAY TRACING
# ============================================================================

def calcul_intersection_triangle_segment(A, B, C, P1, P2):
    """
    Calculate intersection between a triangle and a segment in 3D space.

    Algorithm: Ray-plane intersection followed by point-in-triangle test.

    Parameters:
    -----------
    A, B, C : array-like, shape (3,)
        Triangle vertices
    P1, P2 : array-like, shape (3,)
        Segment endpoints

    Returns:
    --------
    test : bool
        True if intersection exists within segment [P1, P2]
    I : ndarray, shape (3,) or None
        Intersection point coordinates (None if no intersection)
    """
    test = False
    I = None

    N = calcul_normale_triangle(A, B, C)
    direction = P2 - P1
    den = np.dot(N, direction)

    if abs(den) > np.finfo(float).eps:  # Segment not parallel to triangle plane
        t = np.dot(N, (A - P1)) / den

        if 0 <= t <= 1:  # Intersection within segment bounds
            I = P1 + t * direction

            # Check if intersection point is inside triangle
            # (point is inside if it's "to the left" of all edges)
            if (np.dot(N, np.cross(B - A, I - A)) >= 0 and
                np.dot(N, np.cross(C - B, I - B)) >= 0 and
                np.dot(N, np.cross(A - C, I - C)) >= 0):
                test = True

    return test, I


# ============================================================================
# MESH REFINEMENT (Tessellation)
# ============================================================================

def tessellation_triangle(ind, sommets, triangles):
    """
    Subdivide a triangle into 4 sub-triangles by adding midpoint vertices.

    Parameters:
    -----------
    ind : int
        Index of triangle to subdivide
    sommets : ndarray, shape (N, 3)
        Vertex coordinates
    triangles : ndarray, shape (M, 3)
        Triangle indices

    Returns:
    --------
    nouveaux_sommets : ndarray, shape (3, 3)
        The 3 new midpoint vertices (will be appended to sommets)
    nouveaux_triangles : ndarray, shape (4, 3)
        The 4 triangles that replace the original
    """
    A, B, C = recupere_sommets(ind, sommets, triangles)

    # Create new vertices at edge midpoints
    m_ab = (A + B) * 0.5
    m_bc = (B + C) * 0.5
    m_ca = (C + A) * 0.5

    nouveaux_sommets = np.array([m_ab, m_bc, m_ca])

    # New vertices will be appended to end of vertex array
    nb = len(sommets)
    i_ab = nb
    i_bc = nb + 1
    i_ca = nb + 2

    # Create 4 new triangles to replace the original
    i_A, i_B, i_C = triangles[ind]

    nouveaux_triangles = np.array([
        [i_A, i_ab, i_ca],
        [i_ab, i_bc, i_ca],
        [i_ab, i_B, i_bc],
        [i_ca, i_bc, i_C]
    ], dtype=int)

    return nouveaux_sommets, nouveaux_triangles


def tessellation_objet(sommets, triangles, surf_min):
    """
    Refine a mesh by recursively subdividing triangles exceeding a surface threshold.

    Iteratively subdivides triangles larger than surf_min:
    1. Loop through all triangles (list grows during iteration)
    2. If triangle surface > surf_min, subdivide into 4 triangles
    3. Remove original triangle, add new vertices and triangles
    4. Only increment index when triangle is NOT subdivided

    Parameters:
    -----------
    sommets : ndarray, shape (N, 3)
        Vertex coordinates
    triangles : ndarray, shape (M, 3)
        Triangle indices
    surf_min : float
        Maximum allowed surface area for a triangle

    Returns:
    --------
    sommets_out : ndarray
        Refined vertex coordinates
    triangles_out : ndarray
        Refined triangle indices
    """
    sommets_out = sommets.copy()
    triangles_out = triangles.copy()

    i = 0
    while i < len(triangles_out):
        A, B, C = recupere_sommets(i, sommets_out, triangles_out)
        s = calcul_surface_triangle(A, B, C)

        if s > surf_min:
            # Subdivide this triangle
            nouveaux_som, nouveaux_tri = tessellation_triangle(i, sommets_out, triangles_out)

            # Add new vertices
            sommets_out = np.vstack([sommets_out, nouveaux_som])

            # Remove old triangle and add new ones
            triangles_out = np.delete(triangles_out, i, axis=0)
            triangles_out = np.vstack([triangles_out, nouveaux_tri])

            # Don't increment i - check this position again with new triangle
        else:
            i += 1

    return sommets_out, triangles_out
