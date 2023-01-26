import pygame 
import time as t
import random
import Assets.Scripts.framework as f
import Assets.Scripts.background as backg
import Assets.Scripts.bg_particles as bg_particles
pygame.init()
from pygame.locals import *

#Getting image
def get_image(sheet, frame, width, height, scale, colorkey):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colorkey)
    return image

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
tile1 = pygame.image.load("./Assets/Tiles/tile1.png").convert_alpha()
player_img = pygame.image.load("./Assets/Sprites/player_img.png").convert_alpha()
player_idle_img = pygame.image.load("./Assets/Sprites/player_idle.png").convert_alpha()
#Map
map = f.Map("./Assets/Maps/map.txt",tile1 )
#Player settings
player_idle_animation = []
for x in range(4):
    player_idle_animation.append(get_image(player_idle_img, x, 21, 34, 2, (0,0,0)))
player = f.Player(30,30,32,32, player_img, player_idle_animation)
#Random Variables
true_scroll = [0,0]
scroll = [0,0]
last_time = t.time()
radius = 100
dradius = 1
radius_last_update = 0
radius_update_cooldown = 50
#Mouse Settings
pygame.mouse.set_visible(False)
#lightings
glow_effects = []
for x in range(10):
    glow_effects.append(f.Glow((random.randint(0,1000), random.randint(0,500))))
#background stripes
bg = backg.background()
bg_particle_effect = bg_particles.Master()
#Main Game Loop
while run:
    clock.tick(60)
    dt = t.time() - last_time
    dt *= 60
    last_time = t.time()
    time = pygame.time.get_ticks()
    display.fill((23,32,56))
    #Stripes
    blur_surf = display.copy()
    bg.recursive_call(blur_surf)
    blur_surf.set_alpha(50)
    display.blit(blur_surf, (0,0))
    #Mouse Settings 
    mpos = pygame.mouse.get_pos()
    tile_rects = map.blit_map(display, scroll)
    #Calculating Scroll
    true_scroll[0] += (player.get_rect().x - true_scroll[0] - 262) / 5
    true_scroll[1] += (player.get_rect().y - true_scroll[1] - 162) / 5
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    #Player Blitting
    player.move(tile_rects, time, dt)
    player.draw(display, scroll)
    #Mouse Blitting
    pygame.draw.circle(display,(200,0,0), (mpos[0]//2, mpos[1]//2), 4)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #Background Particles
    bg_particle_effect.recursive_call(time, display, scroll, dt)
    #Blitting the large circle around player
    black_display = pygame.Surface((screen_w//2, screen_h//2))
    black_display.fill((0,0,0))
    pygame.draw.circle(black_display, (255,255,255), (player.get_rect().x - scroll[0] + 16, player.get_rect().y - scroll[1] + 16),radius)
    if time - radius_last_update > radius_update_cooldown:
        radius += dradius
        if radius > 90:
            dradius = -1
        if radius < 40:
            dradius  = 1
        radius_last_update = time
    for glow_effect in glow_effects:
        glow_effect.update(time, black_display, scroll)
    black_display.set_colorkey((0,0,0))
    display.blit(black_display, (0,0), special_flags=BLEND_RGBA_MIN)
    surf = pygame.transform.scale(display, (screen_w, screen_h))
    window.blit(surf, (0, 0))
    pygame.display.flip()