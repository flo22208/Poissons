import pygame
import sys
import random

# Initialiser Pygame
pygame.init()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

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
POISSON_SPEED = 1
Nb_POISSON = 30


# Définir les dimensions de la grille
TILE_SIZE = 15
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE



game_map = [
    [0 for x in range(30)]
    for y in range(30)
]



Poissons_Position = [[random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2)] for _ in range(Nb_POISSON)]
direction = [[random.randint(-1, 1), random.randint(-1, 1)] for _ in range(Nb_POISSON)]
changement_direction = [random.randint(1, 10) for _ in range(Nb_POISSON)]
speed = [random.randint(1, 3) for _ in range(Nb_POISSON)]
changement_speed = [random.randint(1, 10) for _ in range(Nb_POISSON)]

clock = pygame.time.Clock()
time = 0

# trafalgar
# selection d'un leader
leader = random.randint(0, Nb_POISSON-1)
contaminer = [0 for i in range(Nb_POISSON)]
contaminer[leader] = 1
limite_leader = 2


while True:

    # distance leader
    distance = [0 for i in range(Nb_POISSON)]
   

    for i in range(Nb_POISSON):
        distance[i] = ((Poissons_Position[leader][0] - Poissons_Position[i][0])**2 + (Poissons_Position[leader][1] - Poissons_Position[i][1])**2)**0.5
    for i in range(Nb_POISSON):
        if distance[i] < limite_leader:
            contaminer[i] = 1
        else:
            contaminer[i] = 0

    new_pos_poisson_x = [Poissons_Position[i][0] for i in range(len(Poissons_Position))]
    new_pos_poisson_y = [Poissons_Position[i][1] for i in range(len(Poissons_Position))]
    for i in range(len(Poissons_Position)):
        
        #if time%(10) == 0:
        #    direction = [random.randint(-1, 1), random.randint(-1, 1)]
        if time%changement_direction[i] == 0:
            if contaminer[i] == 1:
                direction[i][0] = direction[leader][0]
                direction[i][1] = direction[leader][1]
            else:
                direction[i][0] = random.randint(-1, 1)
                direction[i][1] = random.randint(-1, 1)
                changement_direction[i] = random.randint(1, 10)

        if time%changement_speed[i] == 0:
            if contaminer[i] == 1:
                speed[i] = speed[leader]
            else:
                speed[i] = random.randint(1, 3)
                changement_speed[i] = random.randint(1, 10)

        n_pos_x =  speed[i] * direction[i][0] + new_pos_poisson_x[i]
        n_pos_y =  speed[i] * direction[i][1] + new_pos_poisson_y[i]

        if n_pos_x < 5 :
            new_pos_poisson_x[i] = - n_pos_x + 5
            direction[i][0] = - direction[i][0]
        if n_pos_x >= GRID_WIDTH-5:
            new_pos_poisson_x[i] = GRID_WIDTH - 5 - POISSON_SPEED
            direction[i][0] = - direction[i][0]
        else :
            new_pos_poisson_x[i] = n_pos_x
        if n_pos_y < 5:
            new_pos_poisson_y[i] = - n_pos_y + 5 
            direction[i][1] = - direction[i][1]
        if n_pos_y >= GRID_HEIGHT-5:
            new_pos_poisson_y[i] =  GRID_HEIGHT -5 -  POISSON_SPEED
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
        if Poissons_Position.index(poisson) == leader or contaminer[Poissons_Position.index(poisson)] == 1:
            poisson_image = pygame.image.load('../image/leviator.png')  # Charger l'image du poisson
            poisson_image = pygame.transform.scale(poisson_image, (TILE_SIZE, TILE_SIZE))  # Redimensionner l'image
            screen.blit(poisson_image, (int(poisson[0] * TILE_SIZE), int(poisson[1] * TILE_SIZE)))
        else:
            poisson_image = pygame.image.load('../image/magicarp.png')  # Charger l'image du poisson
            poisson_image = pygame.transform.scale(poisson_image, (TILE_SIZE, TILE_SIZE))  # Redimensionner l'image
            screen.blit(poisson_image, (int(poisson[0] * TILE_SIZE), int(poisson[1] * TILE_SIZE)))
        
    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter la vitesse de la boucle
    clock.tick(FPS)
    time += 1