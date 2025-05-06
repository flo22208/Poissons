import pygame
import sys
import random

# Initialiser Pygame
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# Définir les dimensions de la fenêtre en plein écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Définir le titre de la fenêtre
pygame.display.set_caption('Poisson @ Cap')

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DOT_COLOR = (255, 255, 255)  # Points blancs

# Constantes
FPS = 3
Nb_POISSON = 30


# Définir les dimensions de la grille
TILE_SIZE = 10
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE



game_map = [
    [0 for x in range(10)]
    for y in range(10)
]



Poissons_Position = [[random.randint(5, GRID_WIDTH - 10), random.randint(5, GRID_HEIGHT - 10)] for _ in range(Nb_POISSON)]
direction = [[random.randint(-1, 1), random.randint(-1, 1)] for _ in range(Nb_POISSON)]
changement_direction = [random.randint(5, 20) for _ in range(Nb_POISSON)]
speed = [random.randint(1, 2) for _ in range(Nb_POISSON)]
changement_speed = [random.randint(1, 10) for _ in range(Nb_POISSON)]

clock = pygame.time.Clock()
time = 0

# trafalgar
# selection d'un leader
leader = random.randint(0, Nb_POISSON-1)
contaminer = [0 for i in range(Nb_POISSON)]
contaminer[leader] = 2
limite_leader = 5


while True:

    # distance leader
    distance = [0 for i in range(Nb_POISSON)]
    distance[leader] = 1000
   

    for i in range(Nb_POISSON):
        if i == leader:
            distance[i] = 1000 
        else:
            distance[i] = min(
                ((Poissons_Position[j][0] - Poissons_Position[i][0])**2 + 
                 (Poissons_Position[j][1] - Poissons_Position[i][1])**2)**0.5
                for j in range(Nb_POISSON) if contaminer[j] == 1 or j == leader
            )
    for i in range(Nb_POISSON):
        if distance[i] < limite_leader:
            contaminer[i] = 1

    new_pos_poisson_x = [Poissons_Position[i][0] for i in range(len(Poissons_Position))]
    new_pos_poisson_y = [Poissons_Position[i][1] for i in range(len(Poissons_Position))]
    for i in range(len(Poissons_Position)):
        if contaminer[i] == 1:
                direction[i][0] = direction[leader][0]
                direction[i][1] = direction[leader][1]
                speed[i] = speed[leader]
        else:
            if time%changement_direction[i] == 0:
                    direction[i][0] = random.randint(-1, 1)
                    direction[i][1] = random.randint(-1, 1)
                    changement_direction[i] = random.randint(5, 20)
            if time%changement_speed[i] == 0:
                    speed[i] = random.randint(1, 2)
                    changement_speed[i] = random.randint(1, 10)

       
        n_pos_x =  speed[i] * direction[i][0] + new_pos_poisson_x[i]
        n_pos_y =  speed[i] * direction[i][1] + new_pos_poisson_y[i]

        if n_pos_x < 5 :
            new_pos_poisson_x[i] = - speed[i] * direction[i][0] + new_pos_poisson_x[i]
            direction[i][0] = - direction[i][0]
        if n_pos_x >= GRID_WIDTH-5:
            new_pos_poisson_x[i] = - speed[i] * direction[i][0] + new_pos_poisson_x[i]
            direction[i][0] = - direction[i][0]
        else :
            new_pos_poisson_x[i] = n_pos_x
        if n_pos_y < 5:
            new_pos_poisson_y[i] = - speed[i] * direction[i][1] + new_pos_poisson_y[i]
            direction[i][1] = - direction[i][1]
        if n_pos_y >= GRID_HEIGHT-5:
            new_pos_poisson_y[i] = - speed[i] * direction[i][1] + new_pos_poisson_y[i]
            direction[i][1] = - direction[i][1]
        else :
            new_pos_poisson_y[i] = n_pos_y

    Poissons_Position = [[int(new_pos_poisson_x[i]), int(new_pos_poisson_y[i])] for i in range(len(Poissons_Position))]


    # Dessiner l'écran
    screen.fill(BLUE)

    # Dessiner la carte
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == 1:
                pygame.draw.rect(screen, WHITE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


    # Dessiner les fantômes
    for poisson in Poissons_Position:
        if contaminer[Poissons_Position.index(poisson)] == 2:
            pygame.draw.circle(screen, BLACK, (int(poisson[0] * TILE_SIZE + TILE_SIZE // 2), int(poisson[1] * TILE_SIZE + TILE_SIZE // 2)), TILE_SIZE // 2)
        elif contaminer[Poissons_Position.index(poisson)] == 1:
            pygame.draw.circle(screen, RED, (int(poisson[0] * TILE_SIZE + TILE_SIZE // 2), int(poisson[1] * TILE_SIZE + TILE_SIZE // 2)), TILE_SIZE // 2)
        else:
            pygame.draw.circle(screen, YELLOW, (int(poisson[0] * TILE_SIZE + TILE_SIZE // 2), int(poisson[1] * TILE_SIZE + TILE_SIZE // 2)), TILE_SIZE // 2)
        
    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter la vitesse de la boucle
    clock.tick(FPS)
    time += 1