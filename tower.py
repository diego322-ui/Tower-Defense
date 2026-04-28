import pygame
import math


class Tower:
    def __init__(self, x, y, tower_type="basic"):
        self.x = x
        self.y = y
        self.tower_type = tower_type
        self.cooldown = 0
        self.farm_timer = 0

        # BASIC
        if tower_type == "basic":
            self.range = 150
            self.damage = 1
            self.cooldown_max = 60
            self.color = (80, 80, 80)

        # SNIPER
        elif tower_type == "sniper":
            self.range = 300
            self.damage = 3
            self.cooldown_max = 120
            self.color = (30, 30, 180)

        # FARM
        elif tower_type == "farm":
            self.range = 0
            self.damage = 0
            self.cooldown_max = 0
            self.color = (60, 160, 60)
            self.farm_interval = 300
            self.farm_income = 15

    def draw(self, screen):
        x = int(self.x)
        y = int(self.y)

        pygame.draw.circle(screen, (0, 0, 0), (x, y), 24)
        pygame.draw.circle(screen, self.color, (x, y), 20)

        pygame.draw.circle(screen, (255, 255, 255), (x, y), 6)

    def attack(self, enemies, projectiles):

        # FARM
        if self.tower_type == "farm":
            self.farm_timer += 1
            if self.farm_timer >= self.farm_interval:
                self.farm_timer = 0
                return self.farm_income
            return 0

        # COOLDOWN
        if self.cooldown > 0:
            self.cooldown -= 1
            return 0

        # TARGET FINDING
        target = None
        lowest = float("inf")

        for e in enemies:
            d = math.hypot(self.x - e.x, self.y - e.y)
            if d <= self.range and e.hp < lowest:
                lowest = e.hp
                target = e

        # ATTACK
        if target:
            target.hp -= self.damage

            projectiles.append({
                "x": self.x,
                "y": self.y,
                "target": target,
                "speed": 10,
                "color": (255, 255, 255) if self.tower_type == "sniper" else (200, 60, 60)
            })

            self.cooldown = self.cooldown_max

        return 0