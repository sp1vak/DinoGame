import pygame
import sys
import random
from dino import DinoObject
from settings import Settings
from cactus import Cactus
from cloud import Cloud
from dirt import Dirt
from time import monotonic


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (63,224,7)
        self.settings = Settings()
        self.screen = self.settings.screen
    
    def draw(self,x,y,action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        pygame.draw.rect(self.screen, self.inactive_color, (x,y, self.width, self.height))
        if x < mouse[0]<x+self.width:
            if y< mouse[1]<y+self.height:
                pygame.draw.rect(self.screen, self.active_color,(x,y, self.width, self.height) )
                if click[0] == 1:
                    pygame.time.delay(300)
                    if action is not None:
                        action()


class DinoGame():
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = self.settings.screen                                                
        pygame.display.set_caption("Dino")
        icon = pygame.image.load("img/cactus_1.png")
        pygame.display.set_icon(icon)
        self.bg_color = self.settings.bg_color
        self.dinosaur = DinoObject(self)
        self.make_jump = False
        self.counter_jump = 30
        self.usr_width = 42
        self.usr_height = 1000-7-948
        self.usr_x = self.settings.screen_width//3
        self.usr_y = self.settings.screen_height-self.usr_height-100
        self.cactus_arr = []
        self.clock = pygame.time.Clock()
        self.cactus_images = [pygame.image.load('img/cactus_2.png'), pygame.image.load('img/cactus_2.png'), pygame.image.load('img/cactus_3.png')]
        self.cactus_size = [34, self.settings.screen_height-150-35, 34, self.settings.screen_height-150-35, 51, self.settings.screen_height-150-35]
        self.cloud_image = pygame.image.load('img/cloud.png')
        self.cloud_width = 96
        self.dirt_image = pygame.image.load('img/dirt.png')
        self.clouds = []
        self.dirts = []
        self.collision = False
        self.scores = 0
        self.above_cactus = False
        self.jump_sound = pygame.mixer.Sound('img/pryjki-multyashnye.mp3')
        self.max_score = 0
        self.menu_image = pygame.image.load('img/menu_image.jpg')
        self.showmenu = True

    def run_game(self):
        self.array_cactus()        
        for i in range(5):
            x = random.randrange(800, 1500)
            y = random.randint(0, 100) 
            self.clouds.append(Cloud(x, y, self.cloud_width, self.cloud_image, 0.5))

        for i in range(150):
            x = random.randrange(0, 1600)
            y = random.randrange(445, 450)
            self.dirts.append(Dirt(x,y, 3, self.dirt_image, 4))
        mode_game = True
        t=monotonic()

        while mode_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.make_jump = True
            if self.make_jump:
                self.jump()
                
            self.screen.blit(self.settings.phonk, (0,0))
            if monotonic()-t>1:
                self.scores+=1
                t = monotonic()
            self.print_text("Scores: " + str(self.scores), 600 , 10)
            self.dinosaur.blitme() 
            self.clock.tick(60)
            self.draw_cactus_arr()
            for cl in self.clouds:
                cl.move_cloud()
            for di in self.dirts:
                di.move_dirt()
            if keys[pygame.K_ESCAPE]:
                self.pause()
            if self.check_collision():
                pygame.mixer.music.stop()
                if self.scores>self.max_score:
                    self.max_score = self.scores
                self.print_text('Game over, press ENTER to play again. ESC to exit',125,300)
                self.print_text('Max scores: ' + str(self.max_score), 225, 340)
                pygame.display.update()
                mode_game = self.game_over()
            pygame.display.update()
            #self.clock.tick(65)
            pygame.display.flip()

    def show_menu(self):
        start_btn = Button(200, 50)
        exit_btn = Button(200, 50)
        while self.showmenu:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
            self.screen.blit(self.menu_image, (0, 0))
            self.print_text("DINO RUN", 450, 100)
            start_btn.draw(470, 300, self.run_game)
            self.print_text("START GAME", 500, 300)
            exit_btn.draw(470, 380, quit)
            self.print_text("QUIT GAME", 500, 380)
            pygame.display.update()

    def count_scores(self):
        if not self.above_cactus:
            for barrier in self.cactus_arr:
                if barrier.x <= self.usr_x + self.usr_width/2 <= barrier.x+barrier.width:
                    if self.dinosaur.rect.y + self.usr_height-5 <= barrier.y:
                        self.above_cactus = True
                        break
        else:
            if self.counter_jump == -30:
                self.scores += 1
                self.above_cactus = False

    def game_over(self):
        #if self.scores > self.max_score:
        #    self.max_score = self.scores
        stopped = True
        while stopped:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                keys = pygame.key.get_pressed()
                #self.print_text('Max scores ' + str(self.max_score), 225, 340)
                pygame.display.update()
                if keys[pygame.K_RETURN]:
                    stopped = False
                    self.scores = 0
                    self.clouds = []
                    self.make_jump = False
                    self.cactus_arr = []
                    self.run_game()
                    return True
                if keys[pygame.K_ESCAPE]:
                    return False      

    def check_collision(self):
        #перевірка на jump
        for barrier in self.cactus_arr:
            if not self.make_jump:
                if barrier.x <= self.dinosaur.rect.x+45 <=barrier.x+barrier.width:
                    return True
            elif self.counter_jump == 10:
                if self.dinosaur.rect.y+self.usr_height-5 >= barrier.y:
                    if barrier.x <= self.dinosaur.rect.x + self.usr_width - 5 <= barrier.x+barrier.width:
                        return True
            elif self.counter_jump == -1:
                if self.dinosaur.rect.y+self.usr_height-5 >= barrier.y:
                    if barrier.x <= self.dinosaur.rect.x+self.usr_width -38<= barrier.x+barrier.width:
                        return True
            else:
                if self.dinosaur.rect.y+self.usr_height-10>=barrier.y:
                    if barrier.x <= self.usr_x+5 <= barrier.x + 25:
                        return True
        return False

    def pause(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            keys = pygame.key.get_pressed()
            self.print_text("Paused, press enter to continue", 125,300)
            if keys[pygame.K_RETURN]:
                paused = False
                
    def print_text(self, message, x,y, font_color = (0,0,0), font_type='font/GajrajOne-Regular.ttf', fon_size=16):
        self.screen = self.settings.screen
        self.message = message
        self.x = x
        self.y = y
        self.font_color = font_color
        self.font_type = pygame.font.Font(font_type, fon_size)
        self.message = self.font_type.render(message, True, self.font_color)
        self.screen.blit(self.message, (self.x, self.y))

    def jump(self):
        if self.counter_jump >= -30:
            if self.counter_jump == 30:
                pygame.mixer.Sound.play(self.jump_sound)
            self.dinosaur.rect.y -= self.counter_jump//2
            self.counter_jump -= 1
        else:
            self.dinosaur.rect.y = self.settings.screen_height//2+70
            self.counter_jump = 30
            self.make_jump = False

    def array_cactus(self):
        for i in range(3):
            choice = random.randrange(0,3)
            img = self.cactus_images[choice]
            width = self.cactus_size[choice*2]
            height = self.cactus_size[choice*2+1]
            self.cactus_arr.append(Cactus(self.settings.screen_width+300, height, width, img, 4))

    def draw_cactus_arr(self):
        for cactus in self.cactus_arr:
            check = cactus.move()
            if not check:
                radius = self.find_radius()
                choice = random.randrange(0,3)
                img = self.cactus_images[choice]
                width = self.cactus_size[choice*2]
                height = self.cactus_size[choice*2+1]
                cactus.return_cactus(radius, height, width, img)

    def find_radius(self):
        maximum = max([self.cactus_arr[0].x, self.cactus_arr[1].x, self.cactus_arr[2].x])
        if maximum < self.settings.screen_width:
            radius = self.settings.screen_width
            if radius - maximum < 50:
                radius += 150
        else:
            radius = maximum
        choice = random.randrange(0, 5)
        if choice == 0:
            radius = random.randrange(10, 15)
        else:
            radius = random.randrange(700,800)
        return radius
    

if __name__ == '__main__':
    din = DinoGame()
    din.show_menu()