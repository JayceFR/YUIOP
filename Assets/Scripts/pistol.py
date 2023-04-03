import pygame

class pistol():
    def __init__(self, loc, width, height, pistol_img) -> None:
        self.rect = pygame.rect.Rect(loc[0], loc[1], width, height)
        self.dup_x = 0
        self.dup_y = 0
        self.pistol_img = pistol_img
        self.bullets = []
    
    def draw(self, display, scroll):
        self.dup_x = self.rect.x
        self.dup_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        display.blit(self.pistol_img, self.rect)
        self.rect.x = self.dup_x
        self.rect.y = self.dup_y
    
    def update(self):
        pass

    def shoot(self):
        #Creating a bullet
        pass
