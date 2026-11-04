import math
import random
import pygame

# simple celebratory particles on goal reach
class Particle:
    def __init__(self, x, y, color):
        self.x = float(x)
        self.y = float(y)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2.5, 6.5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 1.0
        self.decay = random.uniform(0.015, 0.035)
        self.size = float(random.randint(3, 6))
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15  # gravity pull
        self.life -= self.decay
        self.size = max(1.0, self.size - 0.05)

    @property
    def is_alive(self):
        return self.life > 0.0

    def draw(self, screen):
        if not self.is_alive:
            return
        rad = max(1, int(self.size))
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), rad)
