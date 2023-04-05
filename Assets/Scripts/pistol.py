import pygame
import math
import Assets.Scripts.bullet as b

class Pistol():
    def __init__(self, loc, width, height, pistol_img, bullet_img) -> None:
        self.rect = pygame.rect.Rect(loc[0], loc[1], width, height)
        self.dup_x = 0
        self.facing_right = True
        self.dup_y = 0
        self.pistol_img = pistol_img
        self.bullet_img = bullet_img
        self.bullets = []
    
    def draw(self, display, scroll, angle):
        self.dup_x = self.rect.x
        self.dup_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        display_gun = self.pistol_img.copy()
        display_gun = pygame.transform.rotate(display_gun, math.degrees(angle))
        if math.degrees(angle) < -93.0 or math.degrees(angle) > 91.0:
            if math.degrees(angle) > -130 and math.degrees(angle) < 0:
                self.rect.x += 8
            if math.degrees(angle) > 90.0 and math.degrees(angle) < 180:
                print("I am here")
                self.rect.x += 8
                self.rect.y -= 10
            display_gun_copy = self.pistol_img.copy()
            display_gun_copy = pygame.transform.flip(display_gun_copy, False, True)
            display_gun_copy = pygame.transform.rotate(display_gun_copy, math.degrees(angle))
            display.blit(display_gun_copy, self.rect)
            self.facing_right = False
        else: 
            if math.degrees(angle) > 92 and math.degrees(angle) < 160:
                self.rect.y -= 10
                self.rect.x += 9
            if math.degrees(angle) > 9.0 and math.degrees(angle) < 88.0:
                self.rect.y -= 9
            display.blit(display_gun, self.rect)
            self.facing_right = True
        self.rect.x = self.dup_x
        self.rect.y = self.dup_y
        for bullet in self.bullets:
            bullet.draw(display)
    
    def update(self, new_loc):
        for pos, bullet in sorted(enumerate(self.bullets), reverse=True):
            if bullet.alive:
                bullet.move()
            else:
                self.bullets.pop(pos)
        self.rect.x = new_loc[0]
        self.rect.y = new_loc[1]
    
    def facing_direction(self):
        return self.facing_right
            

    def shoot(self, loc, width, height, angle):
        #Creating a bullet
        self.bullets.append(b.Bullet(loc, width, height, self.bullet_img, angle))
    
    def get_rect(self):
        return self.rect
