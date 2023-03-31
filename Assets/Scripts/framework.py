import random
import pygame

class Player():
    def __init__(self, x,y,width,height, player_img, idle_animation, run_animation):
        self.rect = pygame.Rect(x,y,width,height)
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
        self.idle_animation = idle_animation
        self.run_animation = run_animation
        self.frame = 0 
        self.frame_last_update = 0
        self.frame_cooldown = 200
        self.gravity = 5
        self.jump = False
        self.jump_last_update = 0
        self.jump_cooldown = 600
        self.jump_up_spped = 6
        self.air_timer = 0
        self.collision_type = {}

        self.speed = 5
        self.acceleration = 0.02
        self.deceleration = 0.2

    def draw(self, window, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x = self.rect.x - scroll[0]
        self.rect.y = self.rect.y - scroll[1]
        if not self.moving_left and  not self.moving_right:
            if self.facing_right:
                window.blit(self.idle_animation[self.frame], self.rect)
            else:
                flip = self.idle_animation[self.frame].copy()
                flip = pygame.transform.flip(self.idle_animation[self.frame], True, False)
                flip.set_colorkey((0,0,0))
                window.blit(flip, self.rect)
        else:
            if self.facing_right:
                window.blit(self.run_animation[self.frame], self.rect)
            else:
                flip = self.run_animation[self.frame].copy()
                flip = pygame.transform.flip(self.run_animation[self.frame], True, False)
                flip.set_colorkey((0,0,0))
                window.blit(flip, self.rect)
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

    def move(self, tiles, time, dt):
        self.movement = [0, 0]
        if (self.moving_left or self.moving_right) and not self.jump:
            self.speed += self.acceleration
            if self.speed > 8:
                self.speed = 8
            self.frame_cooldown -= self.deceleration
            if self.frame_cooldown < 100:
                self.frame_cooldown = 100
        else:
            self.speed = 5
            self.frame_cooldown = 200
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
        if self.jump:
            if self.air_timer < 20:
                self.air_timer += 1
                self.movement[1] -= self.jump_up_spped
                self.jump_up_spped -= 0.5
            else:
                self.air_timer = 0
                self.jump = False
                self.jump_up_spped = 6

        #Frame
        if time - self.frame_last_update > self.frame_cooldown:
            self.frame += 1
            if self.frame > 3:
                self.frame = 0
            self.frame_last_update = time

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.moving_left = True
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.moving_right = True
        if key[pygame.K_SPACE] or key[pygame.K_w]:
            if not self.jump and self.collision_type['bottom']:
                if time - self.jump_last_update > self.jump_cooldown:
                    self.jump = True
                    self.jump_last_update = time
        
        if not self.jump:
            self.movement[1] += self.gravity

        self.collision_type = self.collision_checker(tiles)

    def get_rect(self):
        return self.rect
#Map 
class Map():
    def __init__(self, map_loc, tiles, tree):
        self.map = [] 
        self.tiles = tiles
        self.tree = tree
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
        grass_loc = []
        for row in self.map:
            x = 0 
            for element in row:
                if element != "t" and element != "g" and element != "0":
                    window.blit(self.tiles[int(element)-1], (x * 32 - scroll[0], y * 32 - scroll[1]))
                if element == "t":
                    window.blit(self.tree, (x * 32 - scroll[0] - 70, y * 32 - scroll[1] - 150))
                if element == "g":
                    grass_loc.append((x*32, y*32))
                if element != "0" and element != "t" and element != "g":
                    tile_rects.append(pygame.rect.Rect(x*32,y*32,32,32))
                x += 1
            y += 1
        return tile_rects, grass_loc
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

class Glow():
    def __init__(self, loc):
        self.master_glow = []
        for x in range(30):
            self.master_glow.append(Circles(loc[0] + random.randint(-30,30), loc[1] + random.randint(-30,30), random.randint(5,20), random.randint(50,70), random.randint(-2,2)))

    def update(self, time, display, scroll):
        for glow in self.master_glow:
            glow.draw(display, scroll)
            glow.move(time)

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
        pygame.draw.circle(display, (21,29,40), (self.x - scroll[0], self.y - scroll[1]),self.radius)
