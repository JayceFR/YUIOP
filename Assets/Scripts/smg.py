import pygame
import math
import random
import Assets.Scripts.bullet as b
import Assets.Scripts.sparks as sparks

class SMG():
    def __init__(self, loc, width, height, pistol_img, bullet_img) -> None:
        self.rect = pygame.rect.Rect(loc[0], loc[1], width, height)
        self.dup_x = 0
        self.facing_right = True
        self.dup_y = 0
        self.pistol_img = pistol_img
        self.bullet_img = bullet_img
        self.bullets = []
        self.particles = []
        self.recoil = False
        self.recoil_cooldown = 50
        self.recoil_last_update = 0
    
    def draw(self, display, scroll, angle):
        if self.recoil:
            if self.facing_right:
                angle += 0.25
            else:
                angle -= 0.25
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
                self.rect.x += 2
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
        if self.particles != []:
            for particle in self.particles:
                particle.move(1)
                particle.draw(display)
    
    def update(self, time):
        for pos, bullet in sorted(enumerate(self.bullets), reverse=True):
            if bullet.alive:
                bullet.move()
            else:
                self.bullets.pop(pos)
        if self.recoil:
            if time - self.recoil_last_update > self.recoil_cooldown:
                self.recoil = False
    
    def facing_direction(self):
        return self.facing_right
            

    def shoot(self, loc, width, height, angle, time):
        #Creating a bullet
        self.bullets.append(b.Bullet(loc, width, height, self.bullet_img, angle))
        angle *= -1
        self.recoil = True
        self.recoil_last_update = time
        for x in range(5):
            self.particles.append(sparks.Spark([loc[0], loc[1]],math.radians(random.randint(int(math.degrees(angle)) - 20, int(math.degrees(angle)) + 20)) , random.randint(3,6), (120,120,120), 0.4, 1))
    
    def get_rect(self):
        return self.rect