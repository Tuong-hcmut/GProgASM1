import pygame
import random
import time
#from pygame import *
from Sprite import *

class Game:
    # Probably move this to a settings.ini file later
    # Maybe make a UI class
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    FPS = 60
    SPRITE_SIZE = 90
    FONT_SIZE = 25
    MARGINS = 30
    TITLE = "Major Skill Issue - Group 9"
    def __init__(self):
        # Initialize persistent variables
        self.highscore = 0

        # Start game
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption(self.TITLE)
        a, b = from_multiline_sheet(load_sheets(["Assets/Zombie sprites/Zombie 1 (32x32).png"])[0],32,32,[8,7,8,13,9,8])
        self.anim_data = AnimData(a, b)
        self.debugger = Debugger("debug")
        self.audio = Audio()
    def start(self):
        # Initialize in-game variables
        self.score = 0
        self.hits = 0
        self.misses = 0
        self.time = 0

        anim_index = 0
        anim_change_time = time.time()
        sprite = AnimatedSprite(self.anim_data, current_anim=0, anim_fps=8, x=100, y=100)
        while True:
            dt = clock.tick(60) / 1000.0  # delta time in seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.update()
            self.background = pygame.image.load("images/bg.png")
            self.window.blit(self.background,(0,0))
            # Switch animation every 5 seconds
            if time.time() - anim_change_time > 5.0:
                anim_index = (anim_index + 1) % len(self.anim_data.frame_info)
                sprite.ChangeAnim(anim_index)
                anim_change_time = time.time()
            # Update sprite animation
            sprite.UpdateAnim(dt)
            sprite.draw(self.window)
            pygame.display.flip()
    def update(self):
        # Updates game logic
        if self.score > self.highscore:
            self.highscore = self.score
class Debugger:
    def __init__(self, mode_arg):
        self.mode = mode_arg
    def log(self, message):
        if self.mode == "debug":
            print("Debugger log: " + str(message))
class Audio:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/[01] Eternal Night Vignette ~ Eastern Night.flac")
        pygame.mixer.music.play(-1)

pygame.init()
clock = pygame.time.Clock()
game_instance = Game()
game_instance.start()

pygame.quit()



"""# Move this out of the module, handle this on zombie
        if self.lifetime_ms is not None:
            self.age_ms += int(delta_time * 1000)
            if self.age_ms >= self.lifetime_ms:
                self.visible = False
                return
        # To here"""