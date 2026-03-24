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
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GREEN = (50, 220, 90)
RED = (200, 60, 60)
BLUE = (60, 60, 200)
MENU_BG = (40, 40, 80)
SLOT_BG = (60, 60, 60)
SLOT_ACTIVE = (100, 100, 255)

game_state = "menu"

# Start Button
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 60)

# Wegpunkte
path = [(50, 550), (200, 550), (200, 400), (500, 400), (500, 200), (850, 200)]

# Gegner Liste
enemies = []

# Türme Liste
towers = []

# Projektil Liste
projectiles = []

# Turm-Bau Modus
selected_tower_slot = None

# Slot-Kästchen unten zentriert
slot_rects = [pygame.Rect(WIDTH // 2 - 30, HEIGHT - 70, 60, 60)]  # 60x60 Kästchen

# Gegner Klasse
class Enemy:
    def __init__(self):
        self.x, self.y = path[0]
        self.speed = 2
        self.path_index = 0
        self.hp = 3

    def move(self):
        if self.path_index < len(path) - 1:
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
        pygame.draw.circle(SCREEN, BLACK, (int(self.x), int(self.y)), 14)
        pygame.draw.circle(SCREEN, RED, (int(self.x), int(self.y)), 10)
        # Lebensbalken
        pygame.draw.rect(SCREEN, RED, (self.x - 10, self.y - 20, 20, 4))
        pygame.draw.rect(SCREEN, GREEN, (self.x - 10, self.y - 20, 20 * (self.hp / 3), 4))


# Turm Klasse
class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 120
        self.color = (80, 80, 80)
        self.cooldown = 0
        self.target_angle = 0

    def draw(self):
        pygame.draw.circle(SCREEN, self.color, (self.x, self.y), 20)
        pygame.draw.circle(SCREEN, RED, (self.x, self.y), 10)
        pygame.draw.circle(SCREEN, WHITE, (self.x, self.y), 5)
        length = 20
        end_x = self.x + math.cos(self.target_angle) * length
        end_y = self.y + math.sin(self.target_angle) * length
        pygame.draw.line(SCREEN, BLACK, (self.x, self.y), (end_x, end_y), 5)

    def attack(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        nearest_enemy = None
        nearest_dist = float('inf')
        for enemy in enemies:
            distance = math.hypot(self.x - enemy.x, self.y - enemy.y)
            if distance <= self.range and distance < nearest_dist:
                nearest_enemy = enemy
                nearest_dist = distance
        if nearest_enemy:
            dx = nearest_enemy.x - self.x
            dy = nearest_enemy.y - self.y
            self.target_angle = math.atan2(dy, dx)
            nearest_enemy.hp -= 1
            self.cooldown = 60
            projectiles.append({'x': self.x, 'y': self.y, 'target': nearest_enemy, 'speed': 8})


def update_projectiles():
    for p in projectiles[:]:
        tx, ty = p['target'].x, p['target'].y
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

                # Prüfen ob Slot angeklickt
                slot_clicked = False
                for idx, rect in enumerate(slot_rects):
                    if rect.collidepoint(click_pos):
                        selected_tower_slot = idx
                        slot_clicked = True
                        break

                # Wenn Bau-Modus aktiv und nicht auf Slot geklickt → Turm platzieren
                if selected_tower_slot is not None and not slot_clicked:
                    can_place = True
                    for i in range(len(path) - 1):
                        px, py = path[i]
                        nx, ny = path[i + 1]
                        dx = nx - px
                        dy = ny - py
                        if dx == 0 and dy == 0:
                            continue
                        t = max(0, min(1, ((click_pos[0] - px) * dx + (click_pos[1] - py) * dy) / (dx * dx + dy * dy)))
                        closest_x = px + t * dx
                        closest_y = py + t * dy
                        distance = math.hypot(click_pos[0] - closest_x, click_pos[1] - closest_y)
                        if distance < 50:
                            can_place = False
                            break
                    if can_place:
                        towers.append(Tower(*click_pos))
                        selected_tower_slot = None  # Bau-Modus deaktivieren nach Platzierung

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
            enemy.draw()
            if enemy.path_index >= len(path) - 1 or enemy.hp <= 0:
                enemies.remove(enemy)

        for tower in towers:
            tower.draw()
            tower.attack()

        update_projectiles()

        # Slot-Kästchen zeichnen
        for idx, rect in enumerate(slot_rects):
            color = SLOT_ACTIVE if selected_tower_slot == idx else SLOT_BG
            pygame.draw.rect(SCREEN, color, rect)
            # Turm-Symbol in Slot
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