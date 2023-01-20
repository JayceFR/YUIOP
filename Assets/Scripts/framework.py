from cmath import rect
import pygame

class Player():
    def __init__(self, x,y,width,height, player_img):
        self.rect = pygame.Rect(x,y,width*2,height*2)
        self.display_x = 0
        self.display_y = 0 
        self.moving_left = False
        self.moving_right = False
        self.facing_left = False
        self.facing_right = True
        self.movement = [0,0]
        self.player_img = player_img.copy()
        self.player_img = pygame.transform.scale(self.player_img, (player_img.get_width()*2, player_img.get_height()*2))
        self.player_img.set_colorkey((0,0,0))
        self.gravity = 5
        self.speed = 10

    def draw(self, window, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x = self.rect.x - scroll[0]
        self.rect.y = self.rect.y - scroll[1]
        window.blit(self.player_img, self.rect)
        #pygame.draw.rect(window, (255,255,0), self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y

    def collision_test(self, tiles):
        hitlist = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hitlist.append(tile)
        return hitlist
    
    def collision_checker(self, tiles):
        collision_types = {"top": False, "bottom": False, "right": False, "left": False}
        self.rect.x += self.movement[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[0] > 0:
                self.rect.right = tile.left
                collision_types["right"] = True
            elif self.movement[0] < 0:
                self.rect.left = tile.right
                collision_types["left"] = True
        self.rect.y += self.movement[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                self.rect.bottom = tile.top
                collision_types["bottom"] = True
            if self.movement[1] < 0:
                self.rect.top = tile.bottom
                collision_types["top"] = True
        return collision_types

    def move(self, tiles, dt):
        self.movement = [0, 0]
        if self.moving_right:
            self.movement[0] += self.speed * dt
            self.moving_right = False
            if self.facing_left:
                self.facing_right = True
                self.facing_left = False
        if self.moving_left:
            self.movement[0] -= self.speed * dt
            self.moving_left = False
            if self.facing_right:
                self.facing_left = True
                self.facing_right = False

        key = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.moving_left = True
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.moving_right = True
        if key[pygame.K_SPACE] or key[pygame.K_w]:
            if current_time - self.jump_last_update > self.jump_cooldown:
                self.jump = True
                self.jump_last_update = current_time
                if self.air_timer < 6:
                    gravity = -60

        self.movement[1] += self.gravity

        collision_type = self.collision_checker(tiles)

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
        tile_rects = []
        for row in self.map:
            x = 0 
            for element in row:
                if element == "1":
                    window.blit(self.tile1, (x * 16 - scroll[0], y * 16 - scroll[1]) )
                if element != "0":
                    tile_rects.append(pygame.rect.Rect(x*16,y*16,16,16))
                x += 1
            y += 1
        return tile_rects
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

class Circles():
    def __init__(self,x,y,radius, cooldown, dradius) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.max_radius = radius + radius * 0.5
        self.min_radius = radius - radius * 0.5
        self.last_update = 0
        self.cooldown = cooldown
        self.dradius = dradius
        
    
    def move(self, time):
        if time - self.last_update > self.cooldown:
            self.radius += self.dradius
            if self.radius > self.max_radius:
                self.dradius *= -1
            if self.radius < self.min_radius:
                self.dradius *= -1
            self.last_update = time
    

    def draw(self, display, scroll):
        pygame.draw.circle(display, (255,255,255), (self.x - scroll[0], self.y - scroll[1]),self.radius)