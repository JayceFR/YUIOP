import pygame
import math
import random

class grass():
    def __init__(self, loc, width, height, img) -> None:
        self.loc = loc
        self.dup_y = loc[1] + 3
        self.actual_y = loc[1]
        self.width = width
        self.height = height
        self.actual_height = height
        self.dup_height = height // 1.2
        self.rect = pygame.rect.Rect(self.loc[0], self.loc[1], self.width, self.height)
        self.display_x = 0
        self.display_y = 0
        self.angle = 0
        self.img = img
        self.img_rect = self.img.get_rect()
        self.img_rect.center = (self.loc[0] + self.width//2, self.loc[1] + self.height//2)
        self.new_rect = self.img_rect
        self.speed = 6
        self.current_img = img
        self.change_angle = random.random()*10 + 2
    
    def draw(self, display, scroll):
        '''points = [
            [self.loc[0] - scroll[0] + math.cos(math.radians(self.angle)) * self.speed,
            self.loc[1] - scroll[1] - math.sin(math.radians(self.angle)) * self.speed], 
            [self.loc[0] + self.width - scroll[0] + math.cos(math.radians(self.angle)) * self.speed, 
            self.loc[1] - scroll[1] - math.sin(math.radians(self.angle)) * self.speed], 
            [self.loc[0] + self.width - scroll[0],self.loc[1]+self.height - scroll[1]], 
            [self.loc[0] - scroll[0],self.loc[1] + self.height - scroll[1]]
            ]
        #25,51,45
        #pygame.draw.polygon(display, (25,51,45), points)
        pygame.draw.polygon(display, (20,20,50), points)'''
        self.current_img = pygame.transform.rotate(self.img, self.angle)
        self.new_rect = self.current_img.get_rect()
        self.new_rect.center = self.img_rect.center
        display.blit(self.current_img, (self.new_rect.x - scroll[0], self.new_rect.y - scroll[1]))
    

    def move(self):
        if self.angle == 270:
            self.height = self.actual_height
            self.loc[1] = self.actual_y
            self.angle = 0
        if self.angle > 360:
            self.change_angle = 0 - self.change_angle
        if self.angle < 0:
            self.change_angle = 0 - self.change_angle
        self.angle += self.change_angle
        #if self.angle >= 360:
        #    self.angle = 0
    
    def get_rect(self):
        return self.rect
    
    def colliding(self):
        self.angle = 270
        self.loc[1] = self.dup_y
        self.height = self.dup_height

