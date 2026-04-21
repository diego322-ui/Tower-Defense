# Gegner Klasse
"""
    Diese Klasse repräsentiert einen Gegner im Tower-Defense-Spiel.
    
    Der Gegner startet am ersten Punkt des vorgegebenen Pfades und bewegt
    sich automatisch von Wegpunkt zu Wegpunkt weiter. Die Geschwindigkeit
    bestimmt, wie schnell sich der Gegner entlang des Pfades bewegt.
    
    Jeder Gegner besitzt Lebenspunkte (hp). Wenn er Schaden erhält, verringert
    sich dieser Wert. Über dem Gegner wird ein Lebensbalken angezeigt, der den
    aktuellen Gesundheitszustand visuell darstellt.
"""

import pygame
import colors

path = [(50, 550), (200, 550), (200, 400), (500, 400), (500, 200), (850, 200)]

class Enemy:
    def __init__(self, wave, enemy_type="normal"):
        self.x, self.y = path[0]
        self.path_index = 0

        self.enemy_type = enemy_type

        # Standardwerte
        self.speed = 2
        self.max_hp = 3 + wave
        self.hp = self.max_hp
        self.size = 10

        # Schneller Gegner
        if self.enemy_type == "fast":
            self.speed = 4
            self.max_hp = 2 + wave // 2
            self.hp = self.max_hp
            self.size = 8

        # Boss Gegner
        elif self.enemy_type == "boss":
            self.speed = 1
            self.max_hp = (3 + wave) * 3
            self.hp = self.max_hp
            self.size = 18

        self.alive = True

    def move(self):
        if self.path_index < len(path) - 1:
            tx, ty = path[self.path_index + 1]

            dx = tx - self.x
            dy = ty - self.y
            distance = (dx**2 + dy**2) ** 0.5

            if distance != 0:
                dx /= distance
                dy /= distance

                self.x += dx * self.speed
                self.y += dy * self.speed

            if distance < 5:
                self.path_index += 1

    def draw(self, SCREEN):
        x = int(self.x)
        y = int(self.y)

        # Visueller Unterschied
        if self.enemy_type == "fast":
            color = colors.BLUE
        elif self.enemy_type == "boss":
            color = (150, 0, 150)
        else:
            color = colors.RED

        pygame.draw.circle(SCREEN, colors.BLACK, (x, y), self.size + 4)
        pygame.draw.circle(SCREEN, color, (x, y), self.size)

        hp_width = max(0, int(30 * (self.hp / self.max_hp)))

        pygame.draw.rect(SCREEN, colors.RED, (x - 15, y - 25, 30, 5))
        pygame.draw.rect(SCREEN, colors.GREEN, (x - 15, y - 25, hp_width, 5))