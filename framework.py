from cmath import rect
import pygame

class Player():
    def __init__(self, rect_size):
        self.rect = pygame.Rect(50,50,rect_size[0], rect_size[1])
        self.display_x = 0
        self.display_y = 0 
    def draw(self, window, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x = self.rect.x - scroll[0]
        self.rect.y = self.rect.y - scroll[1]
        pygame.draw.rect(window, (255,255,0), self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= 3
        if keys[pygame.K_s]:
            self.rect.y += 3
        if keys[pygame.K_a]:
            self.rect.x -= 3
        if keys[pygame.K_d]:
            self.rect.x += 3
    def get_rect(self):
        return self.rect
#Map 
class Map():
    def __init__(self, map_loc, tile1):
        self.map = [] 
        self.tile1 = tile1
        f = open(map_loc, "r")
        data = f.read()
        f.close()
        data = data.split("\n")
        for row in data:
            self.map.append(list(row))
    
    def blit_map(self, window, scroll):
        x = 0
        y = 0 
        for row in self.map:
            x = 0 
            for element in row:
                if element == "1":
                    window.blit(self.tile1, (x * 16 - scroll[0], y * 16 - scroll[1]) )
                x += 1
            y += 1
#Bullets
class Bullet():
    def __init__(self, bullet_pos) -> None:
        self.bullet_pos = bullet_pos
        self.rect = pygame.rect.Rect(bullet_pos[0], bullet_pos[1], 3,3)
    
    def draw(self, window):
        pygame.draw.circle(window, (255,0,0), self.bullet_pos, 2)
    
    def move_bullet(self):
        self.rect.x += 5
        self.bullet_pos[0] += 5