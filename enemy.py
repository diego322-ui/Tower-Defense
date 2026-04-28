import pygame
import colors
import math

path = [(50, 550), (200, 550), (200, 400), (500, 400), (500, 200), (850, 200)]


class Enemy:
    def __init__(self, wave, enemy_type="normal"):
        self.x, self.y = path[0]
        self.path_index = 0
        self.enemy_type = enemy_type

        # leichter exponentieller Anstieg
        base = 2 + wave * 0.6
        self.max_hp = base * (1.12 ** wave)
        self.hp = self.max_hp

        self.speed = 2
        self.size = 10

        if enemy_type == "fast":
            self.speed = 4
            self.max_hp *= 0.8
            self.size = 8

        elif enemy_type == "boss":
            self.speed = 1
            self.max_hp *= 2.2
            self.size = 18

        self.hp = self.max_hp
        self.alive = True

    def move(self):
        if self.path_index < len(path) - 1:
            tx, ty = path[self.path_index + 1]

            dx = tx - self.x
            dy = ty - self.y
            dist = math.hypot(dx, dy)

            if dist != 0:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed

            if dist < 5:
                self.path_index += 1

    def draw(self, screen):
        x, y = int(self.x), int(self.y)

        if self.enemy_type == "fast":
            color = colors.BLUE
        elif self.enemy_type == "boss":
            color = (150, 0, 150)
        else:
            color = colors.RED

        pygame.draw.circle(screen, colors.BLACK, (x, y), self.size + 4)
        pygame.draw.circle(screen, color, (x, y), self.size)

        hp_width = max(0, int(30 * (self.hp / self.max_hp)))
        pygame.draw.rect(screen, colors.RED, (x - 15, y - 25, 30, 5))
        pygame.draw.rect(screen, colors.GREEN, (x - 15, y - 25, hp_width, 5))