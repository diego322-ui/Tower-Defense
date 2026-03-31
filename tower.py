# Turm Klasse
"""
    Diese Klasse repräsentiert einen Verteidigungsturm im Tower-Defense-Spiel.
    
    Der Turm wird an einer festen Position platziert und greift automatisch
    Gegner innerhalb seiner Reichweite an. Dabei sucht er den nächsten Gegner,
    richtet sich auf ihn aus und fügt ihm Schaden zu.
    
    Nach jedem Angriff hat der Turm eine Abklingzeit (cooldown), bevor er
    erneut schießen kann. Zusätzlich wird beim Angriff ein Projektil erzeugt
    und der Turm dreht sich visuell in Richtung seines Ziels."""

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
