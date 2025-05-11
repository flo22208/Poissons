import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import numpy as np

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


fig, ax = plt.subplots()
sc = ax.scatter([], [], s=50)

def update(frame):
    global positions, velocities

    # Déplacement + rebonds
    for i in range(Nb_POISSON): 
        if frame % changement_direction[i] == 0:
            velocities[i] = np.array([random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0)])
            changement_direction[i] = random.randint(5, 20)

        new_pos = positions[i] + velocities[i]
        if new_pos[0] <= 5 or new_pos[0] >= GRID_WIDTH - 5:
            velocities[i][0] *= -1
        if new_pos[1] <= 5 or new_pos[1] >= GRID_HEIGHT - 5:
            velocities[i][1] *= -1

        positions[i] += velocities[i]

    # Couleurs d'affichage
    colors = ["yellow"] * Nb_POISSON

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
