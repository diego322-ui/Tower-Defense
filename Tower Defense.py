import pygame
import sys
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

start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 60)

enemies = []
towers = []
projectiles = []

tower_types = ["basic", "sniper", "farm"]

tower_costs = {
    "basic": 50,
    "sniper": 80,
    "farm": 60
}

selected_tower_slot = None

slot_rects = [
    pygame.Rect(WIDTH // 2 - 110, HEIGHT - 70, 60, 60),
    pygame.Rect(WIDTH // 2 - 20, HEIGHT - 70, 60, 60),
    pygame.Rect(WIDTH // 2 + 70, HEIGHT - 70, 60, 60)
]

player_lives = 10
money = 100
error_timer = 0

wave = 1
total_waves = 10
enemies_per_wave = 5
spawned = 0
spawn_timer = 0

info_open = False
info_button = pygame.Rect(WIDTH // 2 + 120, 10, 30, 30)

font_big = pygame.font.SysFont("arial", 60)
font_small = pygame.font.SysFont("arial", 30)
font_tiny = pygame.font.SysFont("arial", 18)


def draw_info_box(screen, tower_type):
    box = pygame.Rect(WIDTH // 2 - 110, 50, 220, 160)
    pygame.draw.rect(screen, (30, 30, 30), box, border_radius=10)
    pygame.draw.rect(screen, WHITE, box, 2, border_radius=10)

    if tower_type == "basic":
        name = "Basic Tower"
        dmg = "Damage: 1"
        rng = "Range: 150"
        desc = "Balanced all-round tower"
        cost = "Cost: 50"

    elif tower_type == "sniper":
        name = "Sniper Tower"
        dmg = "Damage: 3"
        rng = "Range: 300"
        desc = "High damage, slow attack"
        cost = "Cost: 80"

    else:
        name = "Farm Tower"
        dmg = "No attack"
        rng = "No range"
        desc = "Generates money over time"
        cost = "Cost: 60"

    lines = [name, dmg, rng, desc, cost]

    y = box.y + 10
    for line in lines:
        text = font_tiny.render(line, True, WHITE)
        screen.blit(text, (box.x + 10, y))
        y += 28


def update_projectiles():
    for p in projectiles[:]:
        target = p.get("target")

        if not target or not target.alive:
            projectiles.remove(p)
            continue

        dx = target.x - p["x"]
        dy = target.y - p["y"]
        dist = math.hypot(dx, dy)

        if dist < 5:
            projectiles.remove(p)
            continue

        dx, dy = dx / dist, dy / dist
        p["x"] += dx * p["speed"]
        p["y"] += dy * p["speed"]

        pygame.draw.circle(
            SCREEN,
            p.get("color", RED),
            (int(p["x"]), int(p["y"])),
            5
        )


while True:

    # MENU
    if game_state == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    player_lives = 10
                    wave = 1
                    enemies_per_wave = 5
                    spawned = 0
                    enemies.clear()
                    towers.clear()
                    projectiles.clear()
                    selected_tower_slot = None
                    money = 100
                    game_state = "game"

        SCREEN.fill(MENU_BG)

        title = font_big.render("TOWER DEFENSE", True, WHITE)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 180))

        pygame.draw.rect(SCREEN, GREEN, start_button, border_radius=15)
        text = font_small.render("START", True, WHITE)
        SCREEN.blit(text, (
            start_button.centerx - text.get_width() // 2,
            start_button.centery - text.get_height() // 2
        ))

    # GAME
    elif game_state == "game":

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos

                if info_button.collidepoint(click_pos):
                    info_open = not info_open

                slot_clicked = False
                for idx, rect in enumerate(slot_rects):
                    if rect.collidepoint(click_pos):
                        selected_tower_slot = idx
                        slot_clicked = True
                        break

                if selected_tower_slot is not None and not slot_clicked:
                    tower_type = tower_types[selected_tower_slot]
                    cost = tower_costs[tower_type]

                    if money >= cost:
                        towers.append(Tower(click_pos[0], click_pos[1], tower_type))
                        money -= cost
                        selected_tower_slot = None
                    else:
                        error_timer = 60

        SCREEN.fill(GRASS)

        pygame.draw.lines(SCREEN, PATH_OUTER, False, path, 50)
        pygame.draw.lines(SCREEN, PATH_INNER, False, path, 30)

        pygame.draw.circle(SCREEN, (40, 40, 40), path[0], 40)
        pygame.draw.circle(SCREEN, RED, path[0], 30)
        pygame.draw.circle(SCREEN, WHITE, path[0], 15)

        pygame.draw.circle(SCREEN, (40, 40, 40), path[-1], 40)
        pygame.draw.circle(SCREEN, BLUE, path[-1], 30)
        pygame.draw.circle(SCREEN, WHITE, path[-1], 15)

        # SPAWN
        if spawned < enemies_per_wave:
            spawn_timer += 1
            if spawn_timer > 60:
                enemy_type = "normal"

                if wave >= 3 and spawned % 3 == 0:
                    enemy_type = "fast"

                if wave >= 5 and spawned == enemies_per_wave - 1:
                    enemy_type = "boss"

                enemies.append(Enemy(wave, enemy_type))
                spawned += 1
                spawn_timer = 0

        # ENEMIES
        for enemy in enemies[:]:
            enemy.move()
            enemy.draw(SCREEN)

            if enemy.path_index >= len(path) - 1:
                player_lives -= 1
                enemies.remove(enemy)

            elif enemy.hp <= 0:
                enemies.remove(enemy)
                money += 10

        # TOWERS
        for tower in towers:
            tower.draw(SCREEN)
            income = tower.attack(enemies, projectiles)
            if income:
                money += income

        update_projectiles()

        # INFO BUTTON
        pygame.draw.circle(SCREEN, (200, 200, 200), info_button.center, 15)
        text = font_small.render("i", True, BLACK)
        SCREEN.blit(text, (
            info_button.centerx - text.get_width() // 2,
            info_button.centery - text.get_height() // 2
        ))

        # INFO BOX
        if info_open and selected_tower_slot is not None:
            draw_info_box(SCREEN, tower_types[selected_tower_slot])

        # SLOT UI
        for idx, rect in enumerate(slot_rects):
            t = tower_types[idx]
            color = SLOT_ACTIVE if selected_tower_slot == idx else SLOT_BG

            pygame.draw.rect(SCREEN, color, rect, border_radius=10)

            if t == "basic":
                c = (80, 80, 80)
                label = "B"
            elif t == "sniper":
                c = (30, 30, 180)
                label = "S"
            else:
                c = (60, 160, 60)
                label = "F"

            pygame.draw.circle(SCREEN, c, rect.center, 18)

            text = font_tiny.render(label, True, WHITE)
            SCREEN.blit(text, (
                rect.centerx - text.get_width() // 2,
                rect.centery - text.get_height() // 2
            ))

        # HUD
        SCREEN.blit(font_small.render(f"Geld: {money}", True, WHITE),
                    (WIDTH - 180, 20))

        wave_text = font_small.render(f"Welle {wave}/{total_waves}", True, WHITE)
        SCREEN.blit(wave_text, (20, 20))

        lives_text = font_small.render(f"Leben: {player_lives}", True, WHITE)
        SCREEN.blit(lives_text, (20, 50))

        if error_timer > 0:
            err = font_small.render("Nicht genug Geld!", True, RED)
            SCREEN.blit(err, (WIDTH // 2 - 100, HEIGHT - 120))
            error_timer -= 1

        if spawned == enemies_per_wave and len(enemies) == 0 and wave < total_waves:
            wave += 1
            enemies_per_wave += 2
            spawned = 0

            if wave <= 3:
                money += 10
            elif wave <= 6:
                money += 15
            else:
                money += 20

        if player_lives <= 0:
            game_state = "game_over"

    # GAME OVER
    elif game_state == "game_over":
        SCREEN.fill((80, 0, 0))

        txt = font_big.render("GAME OVER", True, WHITE)
        SCREEN.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 50))

        sub = font_small.render("Klick zum Neustart", True, WHITE)
        SCREEN.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                game_state = "menu"

    pygame.display.update()
    clock.tick(60)