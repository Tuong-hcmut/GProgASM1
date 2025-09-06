import pygame
import random
import sys
import os
from Sprite import *  # Use Sprite, AnimatedSprite, AnimData, from_multiline_sheet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")
zombie_sheet_path = os.path.join(ASSETS_DIR, "Zombie sprites", "Zombie 1 (32x32).png")

pygame.init()
clock = pygame.time.Clock()

# ===== Sprite subclasses =====
class Grave(Sprite):
    def __init__(self, x, y, target_height=80, base_res=(800, 600), curr_res=(800,600)):
        full_image = pygame.image.load(
            os.path.join(ASSETS_DIR, "Background", "Decoration", "grave_new.png")
        ).convert_alpha()
        
        # Cut the upper half (RIP gravestone)
        width = full_image.get_width()
        height = full_image.get_height() // 2   # divide in half
        image = full_image.subsurface((0, 0, width, height)).copy()

        super().__init__(image, x, y, target_height, base_resolution=base_res, current_resolution=curr_res)

class Cursor(Sprite):
    def __init__(self, x=0, y=0, target_height=100, base_res=(800,600), curr_res=(800,600)):
        image = pygame.image.load(os.path.join(ASSETS_DIR, "UI", "cursor.png")).convert_alpha()
        super().__init__(image, x, y, target_height, base_resolution=base_res, current_resolution=curr_res)

    def draw_centered(self, surface):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rect = self.image.get_rect(center=(mouse_x, mouse_y))
        surface.blit(self.image, rect.topleft)

class Button(Sprite):
    def __init__(self, image_path, x, y, target_height=60, base_res=(800,600), curr_res=(800,600)):
        image = pygame.image.load(image_path).convert_alpha()
        super().__init__(image, x, y, target_height, base_resolution=base_res, current_resolution=curr_res)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# ===== Debugger =====
class Debugger:
    def __init__(self, mode_arg):
        self.mode = mode_arg
    def log(self, message):
        if self.mode == "debug":
            print("Debugger log: " + str(message))

# ===== Audio =====
class Audio:
    def __init__(self):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(os.path.join(BASE_DIR, "sounds", "[01] Eternal Night Vignette ~ Eastern Night.flac"))
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Error loading audio: " + str(e))

# ===== Game =====
class Game:
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    FPS = 60
    def __init__(self):
        self.highscore = 0
        self.volume = 0.5
        pygame.mixer.music.set_volume(self.volume)
        if self.WINDOW_WIDTH == 1280 and self.WINDOW_HEIGHT == 720:
            self.volume_bar = pygame.Rect(1000,60, 200, 20)
        elif self.WINDOW_WIDTH == 800 and self.WINDOW_HEIGHT == 600:
            self.volume_bar = pygame.Rect(600,50, 150, 15)
        self.dragging_volume = False

        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Whack-a-zombie")

        # Load zombie animation
        sheets = load_sheets([zombie_sheet_path])
        a, b = from_multiline_sheet(sheets[0], 32, 32, [8,7,8,13,9,8])
        self.zombie_anim_data = AnimData(a, b)

        self.debugger = Debugger("debug")
        self.audio = Audio()

        # Cursor
        self.cursor = Cursor(curr_res=(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        # ===== Graves =====
        self.graves = []

        rows, cols = 3, 3
        spacing_x, spacing_y = 100, 100   # distance between graves
        target_height = 70

        # Blue area (hard-coded coordinates or from background)
        # Example: x=250, y=160, w=400, h=300
        if self.WINDOW_WIDTH == 800 and self.WINDOW_HEIGHT == 600:
            area_rect = pygame.Rect(170, 120, 400, 300)
        elif self.WINDOW_WIDTH == 1280 and self.WINDOW_HEIGHT == 720:
            area_rect = pygame.Rect(70, 80, 600, 400)

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
                        curr_res=(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
                )


    # ===== Volume bar =====
    def handle_volume_event(self, event):
        knob_radius = 8
        fill_width = int(self.volume * self.volume_bar.width)
        knob_x = self.volume_bar.x + fill_width
        knob_y = self.volume_bar.y + self.volume_bar.height // 2   # consistent with draw_volume_bar

        knob_rect = pygame.Rect(knob_x - knob_radius, knob_y - knob_radius,
                                knob_radius * 2, knob_radius * 2)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.volume_bar.collidepoint(event.pos) or knob_rect.collidepoint(event.pos):
                self.dragging_volume = True
                self.update_volume(event.pos[0])

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_volume = False

        elif event.type == pygame.MOUSEMOTION and self.dragging_volume:
            self.update_volume(event.pos[0])


    def update_volume(self, mouse_x):
        relative_x = mouse_x - self.volume_bar.x
        self.volume = max(0, min(1, relative_x / self.volume_bar.width))
        pygame.mixer.music.set_volume(self.volume)

    def draw_volume_bar(self):
        pygame.draw.rect(self.window, (200,200,200), self.volume_bar, 2)
        fill_width = int(self.volume * self.volume_bar.width)
        pygame.draw.rect(self.window, (0,200,0), (self.volume_bar.x, self.volume_bar.y, fill_width, self.volume_bar.height))
        knob_x = self.volume_bar.x + fill_width
        knob_y = self.volume_bar.y + self.volume_bar.height // 2
        knob_x = max(self.volume_bar.x, min(knob_x, self.volume_bar.x + self.volume_bar.width))
        pygame.draw.circle(self.window, (255,0,0), (knob_x, knob_y), 10)

    # ===== Main menu =====
    def main_menu(self):
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()
        menu_bg = pygame.image.load(os.path.join(ASSETS_DIR,"Background", "background_new.png")).convert_alpha()
        menu_bg = pygame.transform.scale(menu_bg, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        # Load temporarily to get scaled image width
        start_btn_img = os.path.join(ASSETS_DIR,"Play_button.png")
        settings_btn_img = os.path.join(ASSETS_DIR,"Settings_button.png")
        exit_btn_img = os.path.join(ASSETS_DIR,"Exit.png")

        # Initialize buttons
        start_button = Button(start_btn_img, 0, 250, curr_res=(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        settings_button = Button(settings_btn_img, 0, 360, curr_res=(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        exit_button = Button(exit_btn_img, 0, 470, curr_res=(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        # Center x based on scaled image width
        for btn in [start_button, settings_button, exit_button]:
            btn.x = self.WINDOW_WIDTH//2 - btn.rect.width//2


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
            x = self.WINDOW_WIDTH//2 - title_label.get_width()//2
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
                self.window.blit(esc_label, (self.WINDOW_WIDTH//2-90, 500))

            # Draw cursor
            self.cursor.draw_centered(self.window)


            pygame.display.flip()
            clock.tick(60)

    # ===== Game start =====
    def start(self):
        self.score = 0
        anim_index = 0
        anim_change_time = 0.0

        zombie_sprite = AnimatedSprite(self.zombie_anim_data, anim_fps=8, x=200, y=400,
                                       target_height=50, base_resolution=(800,451),
                                       current_resolution=(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        self.background = pygame.image.load(os.path.join(ASSETS_DIR,"Background","background_new.png")).convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        running = True
        while running:
            dt = clock.tick(self.FPS)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    return "menu"
                self.handle_volume_event(event)

            # Update zombie animation
            anim_change_time += dt
            if anim_change_time >= 5.0:
                anim_index = (anim_index +1) % len(self.zombie_anim_data.frame_info)
                zombie_sprite.ChangeAnim(anim_index)
                anim_change_time = 0.0
            zombie_sprite.UpdateAnim(dt)

            # Draw
            self.window.blit(self.background, (0,0))
            for grave in self.graves:
                grave.draw(self.window)
            zombie_sprite.draw(self.window)
            self.draw_volume_bar()
            self.cursor.draw_centered(self.window)


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
