import pygame 
import framework as f

screen_w = 1000
screen_h = 600
window = pygame.display.set_mode((screen_w,screen_h))
display = pygame.Surface((screen_w//2, screen_h//2))
pygame.display.set_caption("YUIOP")
run = True
player = f.Player([30,30])
tile1 = pygame.image.load("Assets/tile1.png")
map = f.Map("Assets/map.txt",tile1 )
true_scroll = [0,0]
scroll = [0,0]
while run:
    display.fill((0,0,0))
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    surf = pygame.transform.scale(display, (screen_w, screen_h))
    window.blit(surf, (0, 0))
    pygame.display.update()