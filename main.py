import pygame
import random
from pygame import *

class Game:
    # Probably move this to a settings.ini file later
    # Maybe make a Sprite class and a UI class
    self.WINDOW_WIDTH = 1920
    self.WINDOW_HEIGHT = 1366
    self.FPS = 60
    self.SPRITE_SIZE = 90
    self.FONT_SIZE = 25
    self.MARGINS = 30
    self.TITLE = "Major Skill Issue - Group 9"
    def __init__(self):
        # Initialize persistent variables
        self.highscore = 0

        # Start game
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption(self.TITLE)
        self.background = pygame.image.load("images/bg.png")


        self.debugger = Debugger("debug")
        self.audio = Audio()
    def start(self):
        # Initialize in-game variables
        self.score = 0
        self.hits = 0
        self.misses = 0
        self.time = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.update()
            pygame.display.flip()
    def update(self):
        # Updates game logic
        if self.score > self.highscore:
            self.highscore = self.score
class Debugger:
    def __init__(self, mode_arg)
        self.mode = mode_arg
    def log(self, message):
        if self.mode == "debug":
            print("Debugger log: " + str(message))
class Audio:
    def __init__(self):
        self.bgm = pygame.mixer.music.load("sounds/main.wav")

pygame.init()

game_instance = Game()
game_instance.start()

pygame.quit()
