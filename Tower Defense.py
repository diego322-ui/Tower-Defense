import pygame
import sys
from pygame.locals import QUIT
import math

from colors import *
from enemy import Enemy, path
from tower import Tower

pygame.init()

WIDTH, HEIGHT = 900, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")

clock = pygame.time.Clock()
game_state = "menu"

# Start Button
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 60)

# Gegner Liste
enemies = []

# Türme Liste
towers = []

# Projektil Liste
projectiles = []

# Turm-Bau Modus
selected_tower_slot = None

# Slot-Kästchen unten zentriert
slot_rects = [pygame.Rect(WIDTH // 2 - 30, HEIGHT - 70, 60, 60)]


def update_projectiles():
    for p in projectiles[:]:
        target = p['target']

        # Wenn Ziel tot → Projektil löschen
        if not target.alive:
            projectiles.remove(p)
            continue

        tx, ty = target.x, target.y
        dx, dy = tx - p['x'], ty - p['y']
        distance = math.hypot(dx, dy)

        if distance < 5:
            projectiles.remove(p)
            continue

        dx, dy = dx / distance, dy / distance
        p['x'] += dx * p['speed']
        p['y'] += dy * p['speed']

        pygame.draw.circle(SCREEN, RED, (int(p['x']), int(p['y'])), 5)


wave = 1
total_waves = 10
enemies_per_wave = 5
spawned = 0
spawn_timer = 0

font_big = pygame.font.SysFont("arial", 60)
font_small = pygame.font.SysFont("arial", 30)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                if start_button.collidepoint(event.pos):
                    game_state = "game"

            elif game_state == "game":
                click_pos = event.pos

                slot_clicked = False
                for idx, rect in enumerate(slot_rects):
                    if rect.collidepoint(click_pos):
                        selected_tower_slot = idx
                        slot_clicked = True
                        break

                if selected_tower_slot is not None and not slot_clicked:
                    can_place = True
                    for i in range(len(path) - 1):
                        px, py = path[i]
                        nx, ny = path[i + 1]
                        dx = nx - px
                        dy = ny - py

                        if dx == 0 and dy == 0:
                            continue

                        denominator = dx * dx + dy * dy
                        if denominator == 0:
                            t = 0
                        else:
                            t = max(0, min(1, ((click_pos[0] - px) * dx + (click_pos[1] - py) * dy) / denominator))

                        closest_x = px + t * dx
                        closest_y = py + t * dy
                        distance = math.hypot(click_pos[0] - closest_x, click_pos[1] - closest_y)

                        if distance < 50:
                            can_place = False
                            break

                    if can_place:
                        towers.append(Tower(*click_pos))
                        selected_tower_slot = None

    # MENU
    if game_state == "menu":
        SCREEN.fill(MENU_BG)
        title = font_big.render("TOWER DEFENSE", True, WHITE)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 180))

        pygame.draw.rect(SCREEN, GREEN, start_button, border_radius=15)
        text = font_small.render("START", True, WHITE)
        SCREEN.blit(text, (start_button.centerx - text.get_width() // 2,
                           start_button.centery - text.get_height() // 2))

    # GAME
    if game_state == "game":
        SCREEN.fill(GRASS)

        pygame.draw.lines(SCREEN, PATH_OUTER, False, path, 50)
        pygame.draw.lines(SCREEN, PATH_INNER, False, path, 30)

        pygame.draw.circle(SCREEN, (40, 40, 40), path[0], 40)
        pygame.draw.circle(SCREEN, RED, path[0], 30)
        pygame.draw.circle(SCREEN, WHITE, path[0], 15)

        pygame.draw.circle(SCREEN, (40, 40, 40), path[-1], 40)
        pygame.draw.circle(SCREEN, BLUE, path[-1], 30)
        pygame.draw.circle(SCREEN, WHITE, path[-1], 15)

        if spawned < enemies_per_wave:
            spawn_timer += 1
            if spawn_timer > 60:
                enemies.append(Enemy())
                spawned += 1
                spawn_timer = 0

        for enemy in enemies[:]:
            enemy.move()
            enemy.draw(SCREEN)
            if enemy.path_index >= len(path) - 1 or enemy.hp <= 0:
                enemy.alive = False
                enemies.remove(enemy)

        for tower in towers:
            tower.draw(SCREEN)
            tower.attack(enemies, projectiles)

        update_projectiles()

        for idx, rect in enumerate(slot_rects):
            color = SLOT_ACTIVE if selected_tower_slot == idx else SLOT_BG
            pygame.draw.rect(SCREEN, color, rect)
            pygame.draw.circle(SCREEN, BLACK, rect.center, 15)
            pygame.draw.circle(SCREEN, RED, rect.center, 10)
            pygame.draw.circle(SCREEN, WHITE, rect.center, 5)

        if spawned == enemies_per_wave and len(enemies) == 0:
            if wave < total_waves:
                wave += 1
                enemies_per_wave += 2
                spawned = 0

        text = font_small.render(f"Welle {wave}/{total_waves}", True, WHITE)
        SCREEN.blit(text, (20, 20))

    pygame.display.update()
    clock.tick(60)