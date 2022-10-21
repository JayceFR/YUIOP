import pygame 
import framework as f
pygame.init()
#Display settings 
screen_w = 1000
screen_h = 600
window = pygame.display.set_mode((screen_w,screen_h))
display = pygame.Surface((screen_w//2, screen_h//2))
pygame.display.set_caption("YUIOP")

#Game Attributes
run = True
clock = pygame.time.Clock()
player = f.Player([30,30])
tile1 = pygame.image.load("Assets/tile1.png")
map = f.Map("Assets/map.txt",tile1 )
true_scroll = [0,0]
scroll = [0,0]

#Mouse Settings
pygame.mouse.set_visible(False)

#Main Game Loop
while run:
    clock.tick(60)
    display.fill((0,0,0))
    #Mouse Settings 
    mpos = pygame.mouse.get_pos()
    map.blit_map(display, scroll)
    #Calculating Scroll
    true_scroll[0] += (player.get_rect().x - true_scroll[0] - 262) / 20
    true_scroll[1] += (player.get_rect().y - true_scroll[1] - 162) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    #Player Blitting
    player.move()
    player.draw(display, scroll)
    #Mouse Blitting
    pygame.draw.circle(display,(200,0,0), (mpos[0]//2, mpos[1]//2), 4)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    surf = pygame.transform.scale(display, (screen_w, screen_h))
    window.blit(surf, (0, 0))
    pygame.display.update()