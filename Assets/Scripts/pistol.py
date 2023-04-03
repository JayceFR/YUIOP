import pygame
import bullet as b

class pistol():
    def __init__(self, loc, width, height, pistol_img, bullet_img) -> None:
        self.rect = pygame.rect.Rect(loc[0], loc[1], width, height)
        self.dup_x = 0
        self.dup_y = 0
        self.pistol_img = pistol_img
        self.bullet_img = bullet_img
        self.bullets = []
    
    def draw(self, display, scroll):
        self.dup_x = self.rect.x
        self.dup_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        display.blit(self.pistol_img, self.rect)
        self.rect.x = self.dup_x
        self.rect.y = self.dup_y
        for bullet in b.Bullet:
            bullet.draw(display)
    
    def update(self):
        for bullet in b.Bullet:
            bullet.move()
            

    def shoot(self, loc, width, height, angle):
        #Creating a bullet
        self.bullets.append(b.Bullet(loc, width, height, self.bullet_img, angle))
