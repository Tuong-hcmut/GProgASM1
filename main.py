import pygame
import random
import sys
import os
import time
from Sprite import *  # Use Sprite, AnimatedSprite, AnimData, from_multiline_sheet
from Audio import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")
ZOMBIE_SHEET_PATH = os.path.join(ASSETS_DIR, "Zombie sprites", "Zombie 1 (32x32).png")
HIT_EFFECT_SHEET_PATH = os.path.join(ASSETS_DIR, "vfx", "Hit effect VFX", "5_100x100px.png")
GRAVE_SHEET_PATH = os.path.join(ASSETS_DIR, "Background", "Decoration", "grave_new_animated.png")
CURSOR_SHEET_PATH = os.path.join(ASSETS_DIR, "UI", "cursor.png")
BACKGROUND_PATH = os.path.join(ASSETS_DIR,"Background", "background_new.png")
HAMMER_SHEET_PATH = os.path.join(ASSETS_DIR, "UI", "pixel_hammer.png")
PLAY_BUTTON_PATH = os.path.join(ASSETS_DIR,"Play_button.png")
SETTINGS_BUTTON_PATH = os.path.join(ASSETS_DIR,"Settings_button.png")
EXIT_BUTTON_PATH = os.path.join(ASSETS_DIR,"Exit.png")

BASE_WIDTH = 3200
BASE_HEIGHT = 1792
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
SPRITE_HEIGHT = 120
FPS = 60

base_resolution = (BASE_WIDTH,BASE_HEIGHT)
window_resolution = (WINDOW_WIDTH,WINDOW_HEIGHT)
sx = WINDOW_WIDTH / BASE_WIDTH
sy = WINDOW_HEIGHT / BASE_HEIGHT

pygame.init()
clock = pygame.time.Clock()

def load_image(path, scale=None):
    image = pygame.image.load(path).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

# ===== Sprite subclasses =====
class Grave(AnimatedSprite):
    def __init__(self, x, y, anim_data, target_height=SPRITE_HEIGHT, base_res=base_resolution, curr_res=window_resolution):
        super().__init__(anim_data=anim_data, anim_fps= 7,x=x, y=y, target_height=target_height, base_resolution=base_res, current_resolution=curr_res)

class HitEffect(AnimatedSprite):
    def __init__(self, x, y, anim_data, target_height=SPRITE_HEIGHT*10, base_res=base_resolution, curr_res=window_resolution):
        super().__init__(anim_data=anim_data, anim_fps= 10,x=x, y=y, target_height=target_height, base_resolution=base_res, current_resolution=curr_res)

class Hammer:
    def __init__(self, x=0, y=0, target_height= SPRITE_HEIGHT, base_res=base_resolution, curr_res=window_resolution):
        print("start hammer init")
        self.sprite = Sprite(image=pygame.image.load(HAMMER_SHEET_PATH).convert_alpha(), x=x, y=y, target_height=target_height, base_resolution=base_res, current_resolution=curr_res)
        print("bruh")
        self.image = self.sprite.image
        self.angle = 0
        self.swinging = False
        self.swing_time = 0.0
        self.swing_duration = 0.15  # seconds
        print("finish init")

    def swing(self):
        self.swinging = True
        self.swing_time = time.time()
        self.angle = -45

    def update(self):
        if self.swinging:
            elapsed = time.time() - self.swing_time
            if elapsed < self.swing_duration:
                self.angle = -45
            else:
                self.swinging = False
                self.angle = 0

    def draw(self, surface):
        self.update()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rotated = pygame.transform.rotate(self.image, self.angle)
        rect = rotated.get_rect(center=(mouse_x, mouse_y))
        surface.blit(rotated, rect)

class Cursor(Sprite):
    def __init__(self, x=0, y=0, target_height= SPRITE_HEIGHT, base_res=base_resolution, curr_res=window_resolution):
        image = pygame.image.load(CURSOR_SHEET_PATH).convert_alpha()
        super().__init__(image, x, y, target_height, base_resolution=base_res, current_resolution=curr_res)

    def draw_centered(self, surface):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rect = self.image.get_rect(center=(mouse_x, mouse_y))
        surface.blit(self.image, rect.topleft)

class Button(Sprite):
    def __init__(self, image_path, x, y, target_height=SPRITE_HEIGHT, base_res=base_resolution, curr_res=window_resolution):
        image = pygame.image.load(image_path).convert_alpha()
        super().__init__(image, x, y, target_height, base_resolution=base_res, current_resolution=curr_res)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Zombie:
    def __init__(self, x, y, anim_data, lifetime_ms):
        self.sprite = AnimatedSprite(anim_data, anim_fps=8, x=x, y=y, target_height=SPRITE_HEIGHT, base_resolution=base_resolution,
                                       current_resolution=window_resolution)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = lifetime_ms
        self.hit = False
    def update(self, dt):
        self.sprite.UpdateAnim(dt)
        if self.hit:
            return False
        # kiểm tra lifetime
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            return False
        return True

    def draw(self, surface):
        if not self.hit:
            self.sprite.draw(surface)

    def check_hit(self, pos):
        if self.sprite.rect.collidepoint(pos) and not self.hit:
            self.hit = True
            return True
        return False
# class Blood:
#     def __init__(self, x, y, image_path, lifetime_ms=500):
#         self.image = pygame.image.load(image_path).convert_alpha()
#         self.x = x
#         self.y = y
#         self.spawn_time = pygame.time.get_ticks()
#         self.lifetime = lifetime_ms
#         self.rect = self.image.get_rect(center=(x, y))

#     def update(self):
#         # Kiểm tra thời gian tồn tại
#         if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
#             return False
#         return True

#     def draw(self, surface):
#         surface.blit(self.image, self.rect.topleft)

# ===== Debugger =====
class Debugger:
    def __init__(self, mode_arg):
        self.mode = mode_arg
    def log(self, message):
        if self.mode == "debug":
            print("Debugger log: " + str(message))


# ===== Game =====
class Game:
    def __init__(self):
        self.window = pygame.display.set_mode(window_resolution)
        pygame.display.set_caption("Whack-a-zombie")
        self.debugger = Debugger("debug")
        self.audio = Audio(window_resolution)
        # Game state
        self.highscore = 0
        self.hits = 0
        self.misses = 0
        self.score = 0

        # self.bloods = []

        # Load zombie animation
        a, b = from_multiline_sheet(load_sheets([ZOMBIE_SHEET_PATH])[0], 32, 32, [8,7,8,13,9,8])
        self.zombie_anim_data = AnimData(a, b)
        c, d = from_wrapped_sheet(load_sheets([HIT_EFFECT_SHEET_PATH])[0], 100, 100, [30])
        self.hit_effect_anim_data = AnimData(c, d)
        e,f = from_concat_sheet(load_sheets([GRAVE_SHEET_PATH])[0],34,42,[1,7])
        self.grave_anim_data = AnimData(e,f)

        # Cursor
        self.cursor = Cursor(curr_res=window_resolution)

        # ===== Graves =====
        self.graves = []

        num_graves = 9
        spacing_x, spacing_y = SPRITE_HEIGHT*0.5*sx, SPRITE_HEIGHT*sy   # minimum distance

        # Blue area (hard-coded coordinates or from background)
        area_rect = pygame.Rect(1000*sx, 600*sy, 1100*sx, 600*sy)
        def is_far_enough(x, y, graves, min_dx, min_dy):
            for g in graves:
                if abs(x - g.x) < min_dx and abs(y - g.y) < min_dy:
                    return False
            return True

        attempts = 0
        max_attempts = 1000  # safety to avoid infinite loops

        while len(self.graves) < num_graves and attempts < max_attempts:
            attempts += 1
            # Random point inside area_rect (relative to base resolution)
            x = random.randint(area_rect.left, area_rect.right)
            y = random.randint(area_rect.top, area_rect.bottom)

            if is_far_enough(x, y, self.graves, spacing_x, spacing_y):
                print(x,y)
                self.graves.append(
                    Grave(
                        x // sx, y // sy,
                        self.grave_anim_data,
                        target_height=SPRITE_HEIGHT,
                        base_res=base_resolution,
                        curr_res=window_resolution
                    )
                )
          
    # ===== Volume bar =====
    def handle_volume_event(self, event):
        #print("enter handle_volume_event")
        self.audio.music_bar.handle_event(event)
        self.audio.hit_bar.handle_event(event)

    def draw_volume_bar(self):
        self.audio.music_bar.draw(self.window)
        self.audio.hit_bar.draw(self.window)

    # ========= DRAW HUD ==========

    def draw_hud(self):
        font = pygame.font.SysFont("Arial",24,bold=True)
        accuracy = 0
        total = self.hits + self.misses
        if total > 0:
            accuracy = int(self.hits/total*100)
        text = f"Hits: {self.hits}  Misses: {self.misses}  Accuracy: {accuracy}%"
        label = font.render(text, True, (255,255,255))
        self.window.blit(label, (10,10))

    def draw_hammer(self):
        self.hammer.draw(self.window)
    # ===== Main menu =====
    def main_menu(self):
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()
        menu_bg = pygame.image.load(BACKGROUND_PATH).convert_alpha()
        menu_bg = pygame.transform.scale(menu_bg, window_resolution)

        # Initialize buttons
        start_button = Button(PLAY_BUTTON_PATH, 0, 650, curr_res=window_resolution)
        settings_button = Button(SETTINGS_BUTTON_PATH, 0, 910, curr_res=window_resolution)
        exit_button = Button(EXIT_BUTTON_PATH, 0, 1170, curr_res=window_resolution)

        BUTTON_HEIGHT = int(SPRITE_HEIGHT * 1.2)  # adjust multiplier to tune size
        start_y = 650
        spacing = BUTTON_HEIGHT + 40
        start_button = Button(PLAY_BUTTON_PATH, 0, start_y, target_height=BUTTON_HEIGHT, curr_res=window_resolution)
        settings_button = Button(SETTINGS_BUTTON_PATH, 0, start_y + spacing, target_height=BUTTON_HEIGHT, curr_res=window_resolution)
        exit_button = Button(EXIT_BUTTON_PATH, 0, start_y + spacing*2, target_height=BUTTON_HEIGHT, curr_res=window_resolution)
        
        # Center x based on scaled image width
        for btn in [start_button, settings_button, exit_button]:
            btn.x = WINDOW_WIDTH//2 - btn.rect.width//2


        in_menu = True
        in_settings = False
        title_font = pygame.font.SysFont("Arial", 80, bold=True)

        while in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if not in_settings:
                    if start_button.is_clicked(event):
                        return "start"
                    elif settings_button.is_clicked(event):
                        in_settings = True
                    elif exit_button.is_clicked(event):
                        pygame.quit()
                        sys.exit()
                else:
                    self.handle_volume_event(event)
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        in_settings = False

            # Draw background
            self.window.blit(menu_bg, (0,0))

            # Draw title
            text = "Whack A Zombie" if not in_settings else "Settings"
            creepy_color = (180,0,0)
            title_label = title_font.render(text, True, creepy_color)
            outline = title_font.render(text, True, (0,0,0))
            x = WINDOW_WIDTH//2 - title_label.get_width()//2
            y = 120
            for dx in [-3,-2,-1,0,1,2,3]:
                for dy in [-3,-2,-1,0,1,2,3]:
                    if dx!=0 or dy!=0:
                        self.window.blit(outline, (x+dx, y+dy))
            self.window.blit(title_label, (x, y))

            if not in_settings:
                start_button.draw(self.window)
                settings_button.draw(self.window)
                exit_button.draw(self.window)
            else:
                self.draw_volume_bar()
                small_font = pygame.font.SysFont("Arial", 20)
                esc_label = small_font.render("Press ESC to return", True, (200,200,200))
                self.window.blit(esc_label, (WINDOW_WIDTH//2-90, 500))

            # Draw cursor
            self.cursor.draw_centered(self.window)


            pygame.display.flip()
            clock.tick(60)

    # ===== Game start =====
    def start(self):
        print("start")
        self.score = 0
        spawn_timer = 0

        self.background = pygame.image.load(BACKGROUND_PATH).convert_alpha()
        self.background = pygame.transform.scale(self.background, window_resolution)
        self.zombies = []
        self.spawning = []
        self.active_effects = []   # danh sách các hiệu ứng hit
        self.hammer = Hammer()

        print("preloop")
        running = True
        while running:
            dt = clock.tick(FPS)/1000.0
            spawn_timer += dt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    return "menu"
                self.handle_volume_event(event)

                #print("good")
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    clicked = False
                    # Swing hammer
                    self.hammer.swing()
                    for z in self.zombies:

                        if not z.hit and z.check_hit(event.pos):

                            self.hits += 1

                            self.audio.play_hit()
                            # self.bloods.append(Blood(z.sprite.rect.centerx, z.sprite.rect.centery,
                            #      os.path.join(ASSETS_DIR, "vfx", "Hit effect VFX", "1", "1_0.png"), lifetime_ms=300))
                            # Tạo hiệu ứng hit tại chỗ zombie
                            effect = HitEffect((z.sprite.rect.centerx)//sx - TARGET_HEIGHT*3/2, (z.sprite.rect.bottom)//sy  - TARGET_HEIGHT*3/2,self.hit_effect_anim_data,TARGET_HEIGHT*3)
                            print("sx sy: ",sx,sy)
                            print("zom x y: ",z.sprite.rect.centerx,z.sprite.rect.centery)
                            print("offset: ",-0.5* TARGET_HEIGHT*3,0.5* TARGET_HEIGHT*3)
                            print("vfx x y: ",effect.x,effect.y)
                            print(" ")
                            self.active_effects.append(effect)
                            clicked = True

                            break

                    if not clicked:
                        self.misses += 1



            # Spawn zombie mỗi 1 giây

            if spawn_timer >= 1.0:
                grave = random.choice(self.graves)
                self.spawning.append(grave)
                grave.ChangeAnim(1)
                spawn_timer = 0

            # Update zombies

            self.zombies = [z for z in self.zombies if z.update(dt)]
            for effect in self.active_effects[:]:
                effect.UpdateAnim(dt)
                if effect.frame_num >= 28:
                    self.active_effects.remove(effect)

            # Update blood effects
            # self.bloods = [b for b in self.bloods if b.update()] 
            # Draw everything

            self.window.blit(self.background,(0,0))

            for grave in self.spawning:
                grave.UpdateAnim(dt)
                if grave.frame_num >= 5:
                    grave.ChangeAnim(0)
                    lifetime = random.randint(800,1500)
                    self.zombies.append(Zombie(grave.x // sx, grave.y // sy, self.zombie_anim_data, lifetime))
                    self.spawning.remove(grave)
            for grave in self.graves:

                grave.draw(self.window)

            for z in self.zombies:

                z.draw(self.window)
            # Vẽ hiệu ứng hit
            for effect in self.active_effects:
                effect.draw(self.window)

            self.draw_volume_bar()

            self.cursor.draw_centered(self.window)

            self.draw_hud()

            self.draw_hammer()

            pygame.display.flip()


# ===== Main loop =====
game_instance = Game()
try:
    while True:
        choice = game_instance.main_menu()
        if choice == "start":
            result = game_instance.start()
            if result == "menu":
                continue
        else:
            break
finally:
    pygame.quit()
    sys.exit()
