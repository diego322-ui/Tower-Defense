# Gegner Klasse
"""
    Diese Klasse repräsentiert einen Gegner im Tower-Defense-Spiel.
    
    Der Gegner startet am ersten Punkt des vorgegebenen Pfades und bewegt
    sich automatisch von Wegpunkt zu Wegpunkt weiter. Die Geschwindigkeit
    bestimmt, wie schnell sich der Gegner entlang des Pfades bewegt.
    
    Jeder Gegner besitzt Lebenspunkte (hp). Wenn er Schaden erhält, verringert
    sich dieser Wert. Über dem Gegner wird ein Lebensbalken angezeigt, der den
    aktuellen Gesundheitszustand visuell darstellt."""

import pygame
import colors

path = [(50, 550), (200, 550), (200, 400), (500, 400), (500, 200), (850, 200)]

class Enemy:
    def __init__(self):
        self.x, self.y = path[0]
        self.speed = 2
        self.path_index = 0
        self.hp = 3
        self.alive = True

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

    def draw(self, SCREEN):
        x = int(self.x)
        y = int(self.y)

        pygame.draw.circle(SCREEN, colors.BLACK, (x, y), 14)
        pygame.draw.circle(SCREEN, colors.RED, (x, y), 10)

        hp_width = max(0, int(20 * (self.hp / 3)))

        pygame.draw.rect(SCREEN, colors.RED, (x - 10, y - 20, 20, 4))
        pygame.draw.rect(SCREEN, colors.GREEN, (x - 10, y - 20, hp_width, 4))
