import pygame
import random

class CircleGen():
    def __init__(self) -> None:
        self.circles = []
        for x in range(10):
            self.circles.append(CircleNode(random.randint(0,500), random.randint(150,300), random.randint(10,20)))
        self.circle_gen_last_update = 0
        self.circle_gen_cooldown = 700
    
    def update(self, time, display):
        for circle in self.circles:
            circle.update(5, time)
            if circle.get_y() < 0:
                circle.alive = False
        if time - self.circle_gen_last_update > self.circle_gen_cooldown:
            circle_count = random.randint(0,10)
            for x in range(circle_count):
                self.circles.append(CircleNode(random.randint(0,500), random.randint(300,400), random.randint(10,20)))
            self.circle_gen_last_update = time

        for pos, circle in sorted(enumerate(self.circles), reverse=True):
            if not circle.alive:
                self.circles.pop(pos)
            else:
                circle.draw(display)

class CircleNode():
    def __init__(self, x, y, radius) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.alive = True
        self.last_update = 0
        self.cooldown = 50
        self.dradius = 5
    
    def draw(self, display):
        pygame.draw.circle(display, (0,0,0), (self.x, self.y), self.radius)
    
    def update(self, speed, time):
        if time - self.last_update > self.cooldown:
            self.y -= speed
            self.last_update = time
    
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y