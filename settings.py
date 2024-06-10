import pygame


class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0, 222, 255)
        self.dino_speed = 1.5
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.phonk = pygame.image.load(r'img/phonk.jpg')
