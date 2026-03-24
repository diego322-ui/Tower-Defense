import pygame
import sys
from pygame.locals import QUIT
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")

clock = pygame.time.Clock()

# Farben
GRASS = (90, 200, 90)
PATH_OUTER = (170, 120, 70)
PATH_INNER = (130, 90, 50)
WHITE = (255,255,255)
BLACK = (30,30,30)
GREEN = (50,220,90)
RED = (200,60,60)
BLUE = (60,60,200)
MENU_BG = (40,40,80)

game_state = "menu"

# Start Button
start_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 60)

# Wegpunkte
path = [(50,550),(200,550),(200,400),(500,400),(500,200),(850,200)]

# Gegner Liste
enemies = []

# Gegner Klasse
class Enemy:
    def __init__(self):
        self.x, self.y = path[0]
        self.speed = 2
        self.path_index = 0

    def move(self):
        if self.path_index < len(path)-1:

            tx, ty = path[self.path_index + 1]

            if self.x < tx:
                self.x += self.speed
            if self.x > tx:
                self.x -= self.speed
            if self.y < ty:
                self.y += self.speed
            if self.y > ty:
                self.y -= self.speed

            if abs(self.x - tx) < 5 and abs(self.y - ty) < 5:
                self.path_index += 1

    def draw(self):
        pygame.draw.circle(SCREEN, BLACK, (int(self.x),int(self.y)), 14)
        pygame.draw.circle(SCREEN, RED, (int(self.x),int(self.y)), 10)

# Wellen
wave = 1
total_waves = 10
enemies_per_wave = 5
spawned = 0
spawn_timer = 0

# Schrift
font_big = pygame.font.SysFont("arial", 60)
font_small = pygame.font.SysFont("arial", 30)

# Hauptschleife
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_state == "menu":
                if start_button.collidepoint(event.pos):
                    game_state = "game"

    # MENU
    if game_state == "menu":

        SCREEN.fill(MENU_BG)

        title = font_big.render("TOWER DEFENSE", True, WHITE)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 180))

        pygame.draw.rect(SCREEN, GREEN, start_button, border_radius=15)

        text = font_small.render("START", True, WHITE)
        SCREEN.blit(text, (
            start_button.centerx - text.get_width()//2,
            start_button.centery - text.get_height()//2
        ))

    # GAME
    if game_state == "game":

        SCREEN.fill(GRASS)

        # Weg zeichnen
        pygame.draw.lines(SCREEN, PATH_OUTER, False, path, 50)
        pygame.draw.lines(SCREEN, PATH_INNER, False, path, 30)

        # Türme zeichnen
        pygame.draw.circle(SCREEN, (40,40,40), path[0], 40)
        pygame.draw.circle(SCREEN, RED, path[0], 30)
        pygame.draw.circle(SCREEN, WHITE, path[0], 15)

        pygame.draw.circle(SCREEN, (40,40,40), path[-1], 40)
        pygame.draw.circle(SCREEN, BLUE, path[-1], 30)
        pygame.draw.circle(SCREEN, WHITE, path[-1], 15)
    
       # Gegner spawnen
        if spawned < enemies_per_wave:

            spawn_timer += 1

            if spawn_timer > 60:
                enemies.append(Enemy())
                spawned += 1
                spawn_timer = 0

        # Gegner bewegen
        for enemy in enemies[:]:

            enemy.move()
            enemy.draw()

            if enemy.path_index >= len(path)-1:
                enemies.remove(enemy)

        # Neue Welle starten
        if spawned == enemies_per_wave and len(enemies) == 0:

            if wave < total_waves:
                wave += 1
                enemies_per_wave += 2
                spawned = 0
        # Anzeige
        text = font_small.render(f"Welle {wave}/{total_waves}", True, WHITE)
        SCREEN.blit(text,(20,20))
    pygame.display.update()
    clock.tick(60)