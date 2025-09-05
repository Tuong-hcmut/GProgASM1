import pygame
import random
import time
#from pygame import *
from Sprite import *


def get_sprite(sheet,x,y,width,height):
        rect = pygame.Rect(x, y, width, height)
        sprite = sheet.subsurface(rect).copy()
        return sprite
class Game:
    # Probably move this to a settings.ini file later
    # Maybe make a UI class
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
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
        a, b = from_multiline_sheet(load_sheets(["D:/new-whack-a-zombie/GProgASM1/Assets/Zombie sprites/Zombie 1 (32x32).png"])[0],32,32,[8,7,8,13,9,8])
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
        # Load background
        background = pygame.image.load("D:/new-whack-a-zombie/GProgASM1/Assets/Background/background.png")
        self.background = pygame.transform.scale(background, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        # Load graves
        grave_image = pygame.image.load("D:/new-whack-a-zombie/GProgASM1/Assets/Background/Decoration/graveyards.png").convert_alpha()
        self.grave = pygame.transform.scale(get_sprite(grave_image, 0, 0, 32, 32), (96, 96))
        self.grave2 = self.grave.copy()
        self.grave3 = self.grave.copy()
        self.grave4 = self.grave.copy()
        self.grave5 = self.grave.copy()
        self.grave6 = self.grave.copy()

        broken_window_image = pygame.image.load("D:/new-whack-a-zombie/GProgASM1/Assets/Background/Decoration/Dungeon_01.png").convert_alpha()
        self.broken_window_image = pygame.transform.scale(broken_window_image, (100, 100))
        self.broken_window_image2 = self.broken_window_image.copy()
        
        door_image = pygame.image.load("D:/new-whack-a-zombie/GProgASM1/Assets/Background/Decoration/Dungeon_09.png").convert_alpha()
        self.door = pygame.transform.scale(door_image, (150, 150))
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
        
        # Load custom cursor
        cursor_image = pygame.image.load("D:/new-whack-a-zombie/GProgASM1/Assets/UI/cursor.png").convert_alpha()
        self.cursor = pygame.transform.scale(cursor_image, (100, 100))
        running = True
        while running:
            dt = clock.tick(60) / 1000.0  # delta time in seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
            self.update()
            self.draw()
            

            
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
            
    def draw(self):
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.grave, (303, 540))
        self.window.blit(self.grave2, (303, 300))
        self.window.blit(self.grave3, (868, 540))
        self.window.blit(self.grave4, (868, 300))
        self.window.blit(self.grave5, (587, 300))
        self.window.blit(self.grave6, (587, 540))
        self.window.blit(self.broken_window_image, (150, 100))
        self.window.blit(self.broken_window_image2, (1050, 100))
        self.window.blit(self.door, (565, 70))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.window.blit(self.cursor, (mouse_x, mouse_y))
class Debugger:
    def __init__(self, mode_arg):
        self.mode = mode_arg
    def log(self, message):
        if self.mode == "debug":
            print("Debugger log: " + str(message))
class Audio:
    def __init__(self):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("D:/new-whack-a-zombie/GProgASM1/sounds/[01] Eternal Night Vignette ~ Eastern Night.flac")
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Error loading audio: " + str(e))

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