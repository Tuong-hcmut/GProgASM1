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
HIT_ATTACK_SHEET_PATH = os.path.join(ASSETS_DIR, "vfx", "Hit effect VFX", "5_100x100px.png")

BASE_WIDTH = 3200
BASE_HEIGHT = 1792
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60
pygame.init()
clock = pygame.time.Clock()

def load_image(path, scale=None):
    image = pygame.image.load(path).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image
        
# ===== Sprite subclasses =====
class Grave(Sprite):
    def __init__(self, x, y, target_height=80, base_res=(800, 600), curr_res=(1280,720)):
        full_image = pygame.image.load(
            os.path.join(ASSETS_DIR, "Background", "Decoration", "grave_new.png")
        ).convert_alpha()
        
        # Cut the upper half (RIP gravestone)
        width = full_image.get_width()
        height = full_image.get_height() // 2   # divide in half
        image = full_image.subsurface((0, 0, width, height)).copy()

        super().__init__(image, x, y, target_height, base_resolution=base_res, current_resolution=curr_res)

class Cursor(Sprite):
    def __init__(self, x=0, y=0, target_height=100, base_res=(800,600), curr_res=(1280,720)):
        image = pygame.image.load(os.path.join(ASSETS_DIR, "UI", "cursor.png")).convert_alpha()
        super().__init__(image, x, y, target_height, base_resolution=base_res, current_resolution=curr_res)

    def draw_centered(self, surface):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rect = self.image.get_rect(center=(mouse_x, mouse_y))
        surface.blit(self.image, rect.topleft)

class Button(Sprite):
    def __init__(self, image_path, x, y, target_height=60, base_res=(800,600), curr_res=(1280,720)):
        image = pygame.image.load(image_path).convert_alpha()
        super().__init__(image, x, y, target_height, base_resolution=base_res, current_resolution=curr_res)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Zombie:
    def __init__(self, x, y, anim_data, lifetime_ms):
        self.sprite = AnimatedSprite(anim_data, anim_fps=8, x=x, y=y, target_height=80, base_resolution=(800,451),
                                       current_resolution=(WINDOW_WIDTH, WINDOW_HEIGHT))
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
        self.debugger = Debugger("debug")
        self.audio = Audio()
        # Game state
        self.highscore = 0
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.volume = 0.5

        # self.bloods = []
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        

        pygame.mixer.music.set_volume(self.volume)
        if self.hit_sound:
            self.hit_sound.set_volume(self.volume)
        self.volume_bar = VolumeBar(VOLUME_BAR_SHEET_PATH,1000,60,(1280,720),(WINDOW_WIDTH,WINDOW_HEIGHT)),100,
        if WINDOW_WIDTH == 1280 and WINDOW_HEIGHT == 720:
            self.volume_bar = VolumeBar(
            VOLUME_BAR_SHEET_PATH,
            x=1000, y=60, levels=10
        )

        self.dragging_volume = False

        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Whack-a-zombie")

        # Load zombie animation
        sheets = load_sheets([ZOMBIE_SHEET_PATH])
        a, b = from_multiline_sheet(sheets[0], 32, 32, [8,7,8,13,9,8])
        c, d = from_multiline_sheet(load_sheets([HIT_ATTACK_SHEET_PATH])[0],
                                    100, 100, [6, 6, 6, 6, 6])
        self.zombie_anim_data = AnimData(a, b)
        self.hit_anim_data = AnimData(c, d)

        

        # Cursor
        self.cursor = Cursor(curr_res=(WINDOW_WIDTH, WINDOW_HEIGHT))

        # ===== Graves =====
        self.graves = []

        rows, cols = 3, 3
        spacing_x, spacing_y = 100, 100   # distance between graves
        target_height = 70

        # Blue area (hard-coded coordinates or from background)
        # Example: x=250, y=160, w=400, h=300
        if WINDOW_WIDTH == 800 and WINDOW_HEIGHT == 600:
            area_rect = pygame.Rect(170, 120, 400, 300)
        elif WINDOW_WIDTH == 1280 and WINDOW_HEIGHT == 720:
            area_rect = pygame.Rect(70, 80, 600, 400)
        elif WINDOW_WIDTH == 1280 and WINDOW_HEIGHT == 800:
            area_rect = pygame.Rect(50, 100, 600, 400)
        # Calculate grid size
        grid_width = (cols - 1) * spacing_x
        grid_height = (rows - 1) * spacing_y

        # Grid top-left (centered inside blue area)
        start_x = area_rect.centerx - grid_width // 2
        start_y = area_rect.centery - grid_height // 2

        for row in range(rows):
            for col in range(cols):
                x = start_x + col * spacing_x
                y = start_y + row * spacing_y
                self.graves.append(
                    Grave(x, y, target_height=target_height,
                        curr_res=(WINDOW_WIDTH, WINDOW_HEIGHT))
                )

          
    # ===== Volume bar =====
    def handle_volume_event(self, event):
        self.volume_bar.handle_event(event)
        self.volume = self.volume_bar.volume

    def draw_volume_bar(self):
        self.volume_bar.draw(self.window)
    
    # ===== Spawn zombie =====
    def spawn_zombie(self):

        grave = random.choice(self.graves)

        lifetime = random.randint(800,1500)

        self.zombies.append(Zombie(grave.x, grave.y, self.zombie_anim_data, lifetime))

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
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.hammer_swinging:
            elapsed = time.time() - self.hammer_swing_time
            if elapsed < 0.15:
                self.hammer_angle = -45
            else:
                self.hammer_swinging = False
                self.hammer_angle = 0

        rotated = pygame.transform.rotate(self.hammer, self.hammer_angle)
        rect = rotated.get_rect(center=(mouse_x, mouse_y))
        self.window.blit(rotated, rect)
    # ===== Main menu =====
    def main_menu(self):
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()
        menu_bg = pygame.image.load(os.path.join(ASSETS_DIR,"Background", "background_new.png")).convert_alpha()
        menu_bg = pygame.transform.scale(menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Load temporarily to get scaled image width
        start_btn_img = os.path.join(ASSETS_DIR,"Play_button.png")
        settings_btn_img = os.path.join(ASSETS_DIR,"Settings_button.png")
        exit_btn_img = os.path.join(ASSETS_DIR,"Exit.png")

        # Initialize buttons
        start_button = Button(start_btn_img, 0, 250, curr_res=(WINDOW_WIDTH, WINDOW_HEIGHT))
        settings_button = Button(settings_btn_img, 0, 360, curr_res=(WINDOW_WIDTH, WINDOW_HEIGHT))
        exit_button = Button(exit_btn_img, 0, 470, curr_res=(WINDOW_WIDTH, WINDOW_HEIGHT))

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
        self.score = 0
        spawn_timer = 0
        
        sprite_hit = AnimatedSprite(self.hit_anim_data, current_anim=0,
                                anim_fps=8)

        self.background = pygame.image.load(os.path.join(ASSETS_DIR,"Background","background_new.png")).convert_alpha()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.zombies = []
        self.active_effects = []   # danh sách các hiệu ứng hit

        self.hammer = load_image(os.path.join(ASSETS_DIR, "UI", "hammer.png"), (100, 100))
        self.hammer_angle = 0
        self.hammer_swinging = False
        self.hammer_swing_time = 0

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

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    clicked = False
                    # Swing hammer
                    self.hammer_swinging = True
                    self.hammer_swing_time = time.time()
                    for z in self.zombies:

                        if not z.hit and z.check_hit(event.pos):

                            self.hits += 1

                            self.hit_sound.play()
                            # self.bloods.append(Blood(z.sprite.rect.centerx, z.sprite.rect.centery,
                            #      os.path.join(ASSETS_DIR, "vfx", "Hit effect VFX", "1", "1_0.png"), lifetime_ms=300))
                            # Tạo hiệu ứng hit tại chỗ zombie
                            effect = AnimatedSprite(self.hit_anim_data, current_anim=0, anim_fps=20, 
                                                    x=z.sprite.rect.centerx-15, y=z.sprite.rect.top)
                            self.active_effects.append(effect)
                            clicked = True

                            break

                    if not clicked:
                        self.misses += 1



            # Spawn zombie mỗi 1 giây

            if spawn_timer >= 1.0:
                self.spawn_zombie()
                spawn_timer = 0

            # Update zombies

            self.zombies = [z for z in self.zombies if z.update(dt)]
            for effect in self.active_effects[:]:
                effect.UpdateAnim(dt)
                if effect.frame_num >= effect.anim_data.frame_info[effect.anim_num].num_frames - 1:
                    self.active_effects.remove(effect)

            # Update blood effects
            # self.bloods = [b for b in self.bloods if b.update()] 
            # Draw everything

            self.window.blit(self.background,(0,0))

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
