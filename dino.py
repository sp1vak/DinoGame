import pygame
from settings import Settings


class DinoObject():
    def __init__(self, ui_game):
        self.screen = ui_game.screen
        self.setting = Settings()
        self.screen_rect = ui_game.screen.get_rect()
        self.image = pygame.image.load('img/dinogo1.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = self.setting.screen_height//2+70
        self.y = float(self.rect.y)
        self.count = 0
        self.images = [pygame.image.load('img/dinogo1.png'), pygame.image.load('img/dinogo2.png')]
         
    def blitme(self):
        if self.count == 16:
            self.count = 0
        znashenna = self.count//8
        self.images[znashenna] = pygame.transform.scale(self.images[znashenna], (80,80))
        self.screen.blit(self.images[znashenna], self.rect)
        self.count += 1
        