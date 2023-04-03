#TODO -> Weapons and Inventory for the player
#           1 -> katana
#           2 -> gun
#TODO -> Health Bar For Player
#TODO -> Make enemies spawn 

import pygame 
import time as t
import random
import math
import Assets.Scripts.framework as f
import Assets.Scripts.background as backg
import Assets.Scripts.bg_particles as bg_particles
import Assets.Scripts.grass as g
import Assets.Scripts.circle_back as back_circles
import Assets.Scripts.bullet as bullet_class
pygame.init()
from pygame.locals import *

#Getting image
def get_image(sheet, frame, width, height, scale, colorkey):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colorkey)
    return image

def blit_grass(grasses, display, scroll, player):
    for grass in grasses:
        if grass.get_rect().colliderect(player.get_rect()):
            grass.colliding()
        grass.draw(display, scroll)

def blit_inventory(display, inventory, font):
    left = 400
    pygame.draw.line(display, (255,255,255), (left - 10, 300), (left, 270))
    pygame.draw.line(display, (255,255,255), (left, 270), (500, 270))
    for x in range(len(inventory)):
        pygame.draw.rect(display, (150,0,0), pygame.rect.Rect(left, 275, 20, 20), border_radius=5)
        draw_text(str(x+1), font, (255,255,255), left + 9, 294, display)
        pygame.draw.rect(display, (0,0,0), pygame.rect.Rect(left + 2, 275 + 2.5, 20 - 2.5, 20 - 2.5), border_radius=4)
        left += 25

def draw_text(text, font, text_col, x, y, display):
    img = font.render(text, True, text_col)
    display.blit(img, (x, y))

#Display settings 
screen_w = 1000
screen_h = 600
window = pygame.display.set_mode((screen_w,screen_h))
display = pygame.Surface((screen_w//2, screen_h//2))
pygame.display.set_caption("YUIOP")
#Game Attributes
run = True
clock = pygame.time.Clock()
#Loading Images
tiles = []
for x in range(9):
    current_tile = pygame.image.load("./Assets/Tiles/tile{tile_pos}.png".format(tile_pos = str(x+1))).convert_alpha()
    tile_dup = current_tile.copy()
    tile_dup = pygame.transform.scale(tile_dup, (32,32))
    tiles.append(tile_dup)
player_img = pygame.image.load("./Assets/Sprites/player_img.png").convert_alpha()
player_idle_img = pygame.image.load("./Assets/Sprites/player_idle.png").convert_alpha()
player_run_img = pygame.image.load("./Assets/Sprites/player_run.png").convert_alpha()
player_land_img_copy = pygame.image.load("./Assets/Sprites/player_land.png").convert_alpha()
player_land_img = player_land_img_copy.copy()
player_land_img = pygame.transform.scale(player_land_img_copy, (player_land_img_copy.get_width() * 1.2, player_land_img_copy.get_height() * 1.2))
player_land_img.set_colorkey((0,0,0))
tree_img_copy = pygame.image.load("./Assets/Sprites/tree.png").convert_alpha()
tree_img = tree_img_copy.copy()
tree_img = pygame.transform.scale(tree_img_copy, (tree_img_copy.get_width()*3, tree_img_copy.get_height()*3))
tree_img.set_colorkey((235,237,233))
#Grass
grasses = []
grass_loc = []
grass_spawn = True
grass_last_update = 0
grass_cooldown = 50
#Map
map = f.Map("./Assets/Maps/map.txt",tiles,tree_img)
#Player settings
player_idle_animation = []
player_run_animation = []
for x in range(4):
    player_idle_animation.append(get_image(player_idle_img, x, 21, 33, 1.2, (0,0,0)))
for x in range(4):
    player_run_animation.append(get_image(player_run_img, x, 21, 33, 1.2, (0,0,0)))
player = f.Player(30,30,player_idle_animation[0].get_width(),player_idle_animation[0].get_height(), player_img, player_idle_animation, player_run_animation, player_land_img)
#Random Variables
true_scroll = [0,0]
scroll = [0,0]
last_time = t.time()
circle_back = back_circles.CircleGen()
#Mouse Settings
pygame.mouse.set_visible(False)
#Fonts
inven_font = pygame.font.Font("./Assets/Fonts/jayce.ttf", 5)
#lightings
glow_effects = []
for x in range(150):
    glow_effects.append(f.Glow((random.randint(-1000, 3000), random.randint(-100,700))))
#background stripes
bg = backg.background()
bg_particle_effect = bg_particles.Master()
#Inventory
inventory = ["", "", "", ""]
#Bullets
bullet_list = []
#Main Game Loop
while run:
    clock.tick(60)
    dt = t.time() - last_time
    dt *= 60
    last_time = t.time()
    time = pygame.time.get_ticks()
    #display.fill((21,29,40 * 1.5))
    display.fill((0,0,0))
    #VFX
    for glow_effect in glow_effects:
        glow_effect.update(time, display, scroll)
    bg.recursive_call(display)
    #Mouse Settings 
    mpos = pygame.mouse.get_pos()
    #Blitting the Map
    tile_rects, grass_loc = map.blit_map(display, scroll)
    #Creating Items
    if grass_spawn:
        for loc in grass_loc:
            x_pos = loc[0]
            while x_pos < loc[0] + 32:
                x_pos += 2.5
                grasses.append(g.grass([x_pos, loc[1]+14], 2, 18))
        grass_spawn = False
    #Movement of grass
    if time - grass_last_update > grass_cooldown:
        for grass in grasses:
            grass.move()
        grass_last_update = time
    #Calculating Scroll
    true_scroll[0] += (player.get_rect().x - true_scroll[0] - 262) / 5
    true_scroll[1] += (player.get_rect().y - true_scroll[1] - 162) / 5
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    #Player Blitting
    player.move(tile_rects, time, dt, display, scroll)
    player.draw(display, scroll)
    #Blitting Items After Blitting The Player
    blit_grass(grasses, display, scroll, player)
    blit_inventory(display, inventory, inven_font)
    for bullet in bullet_list:
        bullet.move()
        bullet.draw(display)
    #Mouse Blitting
    pygame.draw.circle(display,(200,0,0), (mpos[0]//2, mpos[1]//2), 4)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print("Clicked", mpos[0]//2, mpos[1]//2, player.get_rect().x - scroll[0], player.get_rect().y - scroll[1])
                if player.right_facing():
                    player_x = player.get_rect().x + 32
                    player_y = player.get_rect().y + 15
                else:
                    player_x = player.get_rect().x - 14
                    player_y = player.get_rect().y + 15
                angle = math.atan2((player_y - scroll[1] - mpos[1]//2) , (player_x - scroll[0] - mpos[0]//2))
                print(angle)
                angle = angle * -1
                bullet_list.append(bullet_class.Bullet((player_x - scroll[0], player_y - scroll[1]), 10, 10, None, angle))
    #Background Particles
    bg_particle_effect.recursive_call(time, display, scroll, dt)
    surf = pygame.transform.scale(display, (screen_w, screen_h))
    window.blit(surf, (0, 0))
    pygame.display.flip()