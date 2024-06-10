import pygame
from settings import Settings


class Dirt:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image 
        self.speed = speed
        self.setting = Settings()
        self.screen = self.setting.screen
        
    def move_dirt(self):
        if self.x >= -self.width:
            self.screen.blit(self.image, (self.x,self.y))
            self.x -= self.speed
        else:
            self.x = self.setting.screen_width
