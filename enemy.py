# Gegner Klasse
"""
    Diese Klasse repräsentiert einen Gegner im Tower-Defense-Spiel.
    
    Der Gegner startet am ersten Punkt des vorgegebenen Pfades und bewegt
    sich automatisch von Wegpunkt zu Wegpunkt weiter. Die Geschwindigkeit
    bestimmt, wie schnell sich der Gegner entlang des Pfades bewegt.
    
    Jeder Gegner besitzt Lebenspunkte (hp). Wenn er Schaden erhält, verringert
    sich dieser Wert. Über dem Gegner wird ein Lebensbalken angezeigt, der den
    aktuellen Gesundheitszustand visuell darstellt."""

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

