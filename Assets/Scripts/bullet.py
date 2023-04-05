import pygame
import math

class Bullet():
    def __init__(self, loc, width, height, img, angle) -> None:
        self.rect = pygame.rect.Rect(loc[0], loc[1], width, height)
        self.img = img.copy()
        self.img = pygame.transform.rotate(self.img, math.degrees(angle))
        self.alive = True
        self.angle = angle
        self.speed = 30

    def move(self):
        self.rect.x += math.cos(self.angle) * self.speed
        self.rect.y -= math.sin(self.angle) * self.speed
        if self.rect.x >= 10000 or self.rect.x < -1000 or self.rect.y <= -100 or self.rect.y >= 1000:
            self.alive = False
    
    def draw(self, display):
        #pygame.draw.circle(display, (255,255,255), (self.rect.x, self.rect.y), 4)
        display.blit(self.img, (self.rect.x, self.rect.y))
