import pygame
import math

class Bullet():
    def __init__(self, loc, width, height, img, angle) -> None:
        self.rect = pygame.rect.Rect(loc[0], loc[1], width, height)
        self.img = img
        self.angle = angle
        self.speed = 5

    def move(self):
        self.rect.x -= math.cos(self.angle) * self.speed
        self.rect.y += math.sin(self.angle) * self.speed
    
    def draw(self, display):
        pygame.draw.circle(display, (255,255,255), (self.rect.x, self.rect.y), 4)
