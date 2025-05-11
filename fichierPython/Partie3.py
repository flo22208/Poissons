import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import numpy as np
from scipy.spatial import KDTree

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
TILE_SIZE = 10
GRID_WIDTH = SCREEN_WIDTH / TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / TILE_SIZE
Nb_POISSON = 30
FPS = 15


positions = np.array([[random.uniform(5, GRID_WIDTH - 10), random.uniform(5, GRID_HEIGHT - 10)]
                      for _ in range(Nb_POISSON)], dtype=float)


velocities = np.array([[random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0)]
                      for _ in range(Nb_POISSON)], dtype=float)

changement_direction = [random.randint(5, 20) for _ in range(Nb_POISSON)]

# Contamination
leader = random.randint(0, Nb_POISSON - 1)
contaminer = [0 for _ in range(Nb_POISSON)]
contaminer[leader] = 2
limite_leader = 3

# Paramètres de comportement
krepulsion = 2
kattraction = 0.5
Vnormz = 2  
Rrepulsion = 5
Ralignement = 5
Rattraction = 10

fig, ax = plt.subplots()
sc = ax.scatter([], [], s=50)

def update(frame):
    global positions, velocities

    # Propagation de la contamination
    for i in range(Nb_POISSON):
        if i == leader:
            continue
        min_dist = np.min([np.linalg.norm(positions[i] - positions[j])
                           for j in range(Nb_POISSON) if contaminer[j] == 1 or j == leader])
        if min_dist < limite_leader:
            contaminer[i] = 1


    # KDTree pour interactions locales
    tree = KDTree(positions)

    # Déplacement + rebonds
    for i in range(Nb_POISSON):
        if contaminer[i] == 1:
            velocities[i] = velocities[leader] + [random.uniform(-0.5, 0.5),random.uniform(-0.5, 0.5)]
        #else:
        #   if frame % changement_direction[i] == 0:
        #       velocities[i] = np.array([random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0)])
        #       changement_direction[i] = random.randint(5, 20)     
    
        distances, indices = tree.query(positions[i], k=7)
        Frepulsion = np.zeros(2)
        Fattraction = np.zeros(2)
        Falignement = np.zeros(2)
        N=7
        for j in range(1, len(distances)):
            if distances[j] < Rrepulsion:
                Frepulsion -= krepulsion * (positions[indices[j]] - positions[i]) / (distances[j]**2)
            elif distances[j] < Ralignement:
                Falignement += (1/N)*velocities[indices[j]]
            elif distances[j] < Rattraction:
                Fattraction += kattraction * (positions[indices[j]] - positions[i]) / (distances[j]**2) 
        # Mise à jour du vecteur vitesse
        velocities[i] += Frepulsion + Fattraction + Falignement

        # Limiter la norme de la vitesse
        velocities[i] = velocities[i] / np.linalg.norm(velocities[i]) * Vnormz

        new_pos = positions[i] + velocities[i]
        if new_pos[0] <= 5 or new_pos[0] >= GRID_WIDTH - 5:
            velocities[i][0] *= -1
        if new_pos[1] <= 5 or new_pos[1] >= GRID_HEIGHT - 5:
            velocities[i][1] *= -1

        positions[i] += velocities[i]

    # Couleurs d'affichage
    colors = []
    for i in range(Nb_POISSON):
        if contaminer[i] == 2:
            colors.append("black")
        elif contaminer[i] == 1:
            colors.append("red")
        else:
            colors.append("yellow")

    sc.set_offsets(positions * TILE_SIZE)
    sc.set_color(colors)
    return sc,

# Setup graphique
ax.set_xlim(0, SCREEN_WIDTH)
ax.set_ylim(0, SCREEN_HEIGHT)
ax.set_aspect('equal')
ax.set_facecolor("royalblue")
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])

ani = animation.FuncAnimation(fig, update, interval=1000 // FPS, blit=True)
plt.show()
