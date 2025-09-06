import pygame
import random
import time
import os
import sys 
#from pygame import *
from Sprite import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")
zombie_sheet_path = os.path.join(ASSETS_DIR, "Zombie sprites", "Zombie 1 (32x32).png")
volume_bar_sheet_path = os.path.join(ASSETS_DIR, "UI", "Charging bars and buttons", "Volume bars.png")
def load_image(path, scale=None):
    image = pygame.image.load(path).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image




def get_sprite(sheet,x,y,width,height):
        rect = pygame.Rect(x, y, width, height)
        sprite = sheet.subsurface(rect).copy()
        return sprite
class SpriteButton:
    def __init__(self, image, pos):
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, window):
        window.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Zombie(AnimatedSprite):
    def __init__(self, anim_data, x, y, anim_fps=8):
        lifetime_ms = random.randint(800, 1500)  # thời gian sống random
        super().__init__(anim_data, current_anim=0, anim_fps=anim_fps,
                         x=x, y=y, lifetime_ms=lifetime_ms)
        self.spawn_time = pygame.time.get_ticks()

    def update(self, dt):
        self.UpdateAnim(dt)
        # check lifetime
        if self.lifetime_ms is not None:
            age = pygame.time.get_ticks() - self.spawn_time
            if age >= self.lifetime_ms:
                self.visible = False

    def is_alive(self):
        return self.visible

def load_buttons(path):
    sheet = pygame.image.load(path).convert_alpha()
    print("[DEBUG] Sheet size:", sheet.get_width(), sheet.get_height())
    buttons = {
        "play": get_sprite(sheet, 0, 160, 190, 40),       # PLAY
        "settings": get_sprite(sheet, 0, 180, 190, 40),   # SETTINGS
        "exit": get_sprite(sheet, 0, 200, 190, 40)        # EXIT
    }
    return buttons

def main_menu():
    window = pygame.display.set_mode((Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT))
    pygame.display.set_caption("Whack-a-zombie")
    cursor_image = load_image(os.path.join(ASSETS_DIR, "UI", "cursor.png"), (100, 100))
    pygame.mouse.set_visible(False)
    # Load background cho menu
    menu_bg = load_image(os.path.join(ASSETS_DIR,"Background", "background_new.png"),
                         (Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT))

# Load sprite sheet button 
    start_button_img = load_image(os.path.join(ASSETS_DIR, "Play_button.png"), (300, 60))
    settings_button_img = load_image(os.path.join(ASSETS_DIR, "Settings_button.png"), (300, 60))
    exit_button_img = load_image(os.path.join(ASSETS_DIR, "Exit.png"), (300, 60))


    def center_button(img, y):
        return SpriteButton(img, (Game.WINDOW_WIDTH//2 - img.get_width()//2, y))

    start_button = center_button(start_button_img, 250)
    settings_button = center_button(settings_button_img, 360)
    exit_button = center_button(exit_button_img, 470)


    clock = pygame.time.Clock()
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
                # Xử lý event của volume bar
                game_instance.handle_volume_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    in_settings = False

        # Vẽ background
        window.blit(menu_bg, (0, 0))
        
        

        if not in_settings:
            # Font cho tiêu đề
            title_font = pygame.font.SysFont("Arial", 80, bold=True)

            # Màu chữ chính
            creepy_color = (180, 0, 0)  # đỏ máu

            # Render chữ chính và outline
            text = "Whack A Zombie"
            title_label = title_font.render(text, True, creepy_color)
            outline = title_font.render(text, True, (0, 0, 0))

            # Tọa độ trung tâm
            x = Game.WINDOW_WIDTH // 2 - title_label.get_width() // 2
            y = 120

            # Vẽ outline dày hơn bằng cách dịch nhiều hướng
            for dx in [-3, -2, -1, 0, 1, 2, 3]:
                for dy in [-3, -2, -1, 0, 1, 2, 3]:
                    if dx != 0 or dy != 0:
                        window.blit(outline, (x + dx, y + dy))

            # Vẽ chữ chính ở trên cùng
            window.blit(title_label, (x, y))

            start_button.draw(window)
            settings_button.draw(window)
            exit_button.draw(window)
        else:
            # Vẽ menu settings (volume bar)
            # Font cho tiêu đề
            title_font = pygame.font.SysFont("Arial", 80, bold=True)

            # Màu chữ chính
            creepy_color = (180, 0, 0)  # đỏ máu

            # Render chữ chính và outline
            text = "Settings"
            title_label = title_font.render(text, True, creepy_color)
            outline = title_font.render(text, True, (0, 0, 0))

            # Tọa độ trung tâm
            x = Game.WINDOW_WIDTH // 2 - title_label.get_width() // 2
            y = 120

            # Vẽ outline dày hơn bằng cách dịch nhiều hướng
            for dx in [-3, -2, -1, 0, 1, 2, 3]:
                for dy in [-3, -2, -1, 0, 1, 2, 3]:
                    if dx != 0 or dy != 0:
                        window.blit(outline, (x + dx, y + dy))

            # Vẽ chữ chính ở trên cùng
            window.blit(title_label, (x, y))


            game_instance.draw_volume_bar()

            small_font = pygame.font.SysFont("Arial", 20)
            esc_label = small_font.render("Press ESC to return", True, (200, 200, 200))
            window.blit(esc_label, (Game.WINDOW_WIDTH//2 - 90, 500))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        cursor_rect = cursor_image.get_rect(center=(mouse_x, mouse_y))
        window.blit(cursor_image, cursor_rect.topleft)
        pygame.display.flip()
        clock.tick(60)

class Game:
    # Probably move this to a settings.ini file later
    # Maybe make a UI class
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    FPS = 60
    FONT_SIZE = 25
    MARGINS = 30
    TITLE = "Major Skill Issue - Group 9"
    def __init__(self):
        # Initialize persistent variables
        self.highscore = 0
        self.volume = 0.5
        pygame.mixer.music.set_volume(self.volume)

        self.spawn_points = [
        (400, 200), (590, 200), (780, 200),
        (400, 300), (590, 300), (780, 300),
        (400, 400), (590, 400), (780, 400)
        ]
        self.zombies = []
        self.next_spawn_time = time.time() + random.uniform(1.0, 2.0)


        # Start game
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption(self.TITLE)

        volume_bar_images, volume_bar_frame_info = from_concat_sheet(load_sheets([volume_bar_sheet_path])[0],48, 32,[1,1,1,1,1,1,1,1])
        volume_bar_anim_data = AnimData(volume_bar_images, volume_bar_frame_info)
        self.volume_bar = AnimatedSprite(anim_data=volume_bar_anim_data, anim_fps=0, x=3000, y=60, target_height=120, base_resolution=(3200,1792), current_resolution=(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        #self.volume_bar = pygame.Rect(1000,60, 200, 20)
        self.dragging_volume = False

        zombie_images, zombie_frame_info = from_multiline_sheet(load_sheets([zombie_sheet_path])[0],32, 32,[8, 7, 8, 13, 9, 8])
        self.zombie_anim_data = AnimData(zombie_images, zombie_frame_info)
        self.debugger = Debugger("debug")
        self.audio = Audio()
<<<<<<< HEAD

=======
        self.debugger.log("init done")
>>>>>>> ce31c5f98439ac6b3725fdd8cec949a33cecb14f
    def start(self):
        # Initialize in-game variables
        self.score = 0
        self.hits = 0
        self.misses = 0
        self.time = 0

        anim_index = 0
        anim_change_time = 0.0

        zombie_sprite = AnimatedSprite(anim_data=self.zombie_anim_data, anim_fps=8, x=200, y=400, target_height=50, base_resolution=(800,451), current_resolution=(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        # Load background
        self.background = load_image(os.path.join(ASSETS_DIR, "Background", "background_new.png"), 
                        (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        # Load graves
        grave_image = load_image(os.path.join(ASSETS_DIR, "Background", "Decoration", "grave_new.png"))
        self.grave = pygame.transform.scale(get_sprite(grave_image, 0, 0, 32, 32), (80, 80))
        self.grave2 = self.grave.copy()
        self.grave3 = self.grave.copy()
        self.grave4 = self.grave.copy()
        self.grave5 = self.grave.copy()
        self.grave6 = self.grave.copy()
        self.grave7 = self.grave.copy()
        self.grave8 = self.grave.copy()
        self.grave9 = self.grave.copy()

        # broken_window_image = load_image(os.path.join(ASSETS_DIR, "Background", "Decoration", "Dungeon_01.png"), (100, 100))
        # self.broken_window_image = broken_window_image
        # self.broken_window_image2 = broken_window_image.copy()

        # Door
        # door_image = load_image(os.path.join(ASSETS_DIR, "Background", "Decoration", "Dungeon_09.png"), (150, 150))
        # self.door = door_image
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
        
        # Load custom cursor
        cursor_image = load_image(os.path.join(ASSETS_DIR, "UI", "cursor.png"), (100, 100))
        self.cursor = cursor_image
        running = True
        self.debugger.log("pre-loop done")
        while running:
            dt = clock.tick(60) / 1000.0  # delta time in seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    return "menu"
                self.handle_volume_event(event)
            self.update()
            self.draw()
            self.draw_volume_bar()
            

            
            # Switch animation every 5 seconds
            anim_change_time += dt

            if anim_change_time >= 5.0:

                anim_index = (anim_index + 1) % len(self.zombie_anim_data.frame_info)
                zombie_sprite.ChangeAnim(anim_index)

                anim_change_time = 0.0
            # Update sprite animation
            
           # Update sprite animation
            zombie_sprite.UpdateAnim(dt)
            zombie_sprite.draw(self.window)
            pygame.display.flip()
    def update(self):
        # Updates game logic
        if self.score > self.highscore:
            self.highscore = self.score

    def spawn_zombie(self):
        x, y = random.choice(self.spawn_points)
        z = Zombie(self.zombie_anim_data, x, y, anim_fps=8)
        self.zombies.append(z)
    
    def handle_click(self, pos):
        hit_any = False
        for z in self.zombies:
            if z.visible and z.is_hit(pos):
                self.hits += 1
                self.score += 1
                z.visible = False
                hit_any = True
                break
        if not hit_any:
            self.misses += 1

    def handle_volume_event(self, event):
        #self.debugger.log("enter handle_volume_event")
        knob_radius = 8
        fill_width = int(self.volume * self.volume_bar.image.get_width())
        knob_x = self.volume_bar.x + fill_width
        knob_y = 64

        # Tạo rect bao quanh knob để click dễ hơn
        knob_rect = pygame.Rect(knob_x - knob_radius, knob_y - knob_radius,
                                knob_radius * 2, knob_radius * 2)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.debugger.log("enter MOUSEBUTTONDOWN")
            mx, my = event.pos
            

            if self.volume_bar.is_hit(event.pos) or knob_rect.collidepoint(event.pos):
                self.dragging_volume = True
                self.update_volume(mx)
            self.debugger.log("exit MOUSEBUTTONDOWN")

        elif event.type == pygame.MOUSEBUTTONUP:
            self.debugger.log("enter MOUSEBUTTONUP")
            self.dragging_volume = False
            self.debugger.log("exit MOUSEBUTTONUP")

        elif event.type == pygame.MOUSEMOTION and self.dragging_volume:
            self.debugger.log("enter MOUSEMOTION")
            mx, my = event.pos
            # Debug log khi kéo
            # print(f"[DEBUG] Drag at: ({mx}, {my}) | knob_y={knob_y}")
            self.update_volume(mx)
            self.debugger.log("exit MOUSEMOTION")
        #self.debugger.log("exit handle_volume_event")


    def update_volume(self, mouse_x, mouse_y=None):
        self.debugger.log("enter update_volume")
        # Tính volume theo vị trí chuột (chỉ cần trục X)
        relative_x = mouse_x - self.volume_bar.x
        new_volume = max(0, min(1, relative_x / self.volume_bar.image.get_width()))

        self.volume = new_volume  # lưu lại volume hiện tại
        pygame.mixer.music.set_volume(self.volume)  # chỉ nhận 1 tham số
        self.debugger.log("exit update_volume")


    # def draw_grid(self, grid_size=64, color=(50, 50, 50)):
    #     """Vẽ lưới hỗ trợ căn tọa độ, giống Unity"""
    #     # Vẽ các đường dọc
    #     for x in range(0, self.WINDOW_WIDTH, grid_size):
    #         pygame.draw.line(self.window, color, (x, 0), (x, self.WINDOW_HEIGHT))
    #         # In tọa độ lên đầu lưới
    #         font = pygame.font.SysFont("Arial", 14)
    #         label = font.render(str(x), True, (200, 200, 200))
    #         self.window.blit(label, (x+2, 2))

    #     # Vẽ các đường ngang
    #     for y in range(0, self.WINDOW_HEIGHT, grid_size):
    #         pygame.draw.line(self.window, color, (0, y), (self.WINDOW_WIDTH, y))
    #         font = pygame.font.SysFont("Arial", 14)
    #         label = font.render(str(y), True, (200, 200, 200))
    #         self.window.blit(label, (2, y+2))

    # def draw_colliders(self):
    #     """Vẽ collider (hitbox) của object để debug"""
    #     # Ví dụ: collider của mộ bia
    #     colliders = [
    #         pygame.Rect(303, 540, self.grave.get_width(), self.grave.get_height()),
    #         pygame.Rect(303, 300, self.grave2.get_width(), self.grave2.get_height()),
    #         pygame.Rect(868, 540, self.grave3.get_width(), self.grave3.get_height()),
    #         pygame.Rect(868, 300, self.grave4.get_width(), self.grave4.get_height()),
    #         pygame.Rect(587, 300, self.grave5.get_width(), self.grave5.get_height()),
    #         pygame.Rect(587, 540, self.grave6.get_width(), self.grave6.get_height()),
    #         pygame.Rect(150, 100, self.broken_window_image.get_width(), self.broken_window_image.get_height()),
    #         pygame.Rect(1050, 100, self.broken_window_image2.get_width(), self.broken_window_image2.get_height()),
    #         pygame.Rect(565, 70, self.door.get_width(), self.door.get_height()),
    #         pygame.Rect(1000, 60, self.volume_bar.image.get_width(), self.volume_bar.image.get_height()),
    #     ]

    #     for rect in colliders:
    #         pygame.draw.rect(self.window, (255, 0, 0), rect, 2)  # viền đỏ


    
    def draw(self):
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.grave, ( 400, 200))
        self.window.blit(self.grave2, (590, 200))
        self.window.blit(self.grave3, (780, 200))
        self.window.blit(self.grave4, (400, 300))
        self.window.blit(self.grave5, (590, 300))
        self.window.blit(self.grave6, (780, 300))
        self.window.blit(self.grave7, (400, 400))
        self.window.blit(self.grave8, (590, 400))
        self.window.blit(self.grave9, (780, 400))
        # self.window.blit(self.broken_window_image, (150, 100))
        # self.window.blit(self.broken_window_image2, (1050, 100))
        # self.window.blit(self.door, (565, 70))
        # self.draw_colliders()
        self.draw_volume_bar()
        # self.draw_grid(grid_size=64, color=(80, 80, 80))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        cursor_rect = self.cursor.get_rect(center=(mouse_x, mouse_y))
        self.window.blit(self.cursor, cursor_rect.topleft)

        # HUD
        font = pygame.font.SysFont("Arial", 28, bold=True)
        accuracy = (self.hits / (self.hits + self.misses) * 100) if (self.hits + self.misses) > 0 else 0
        hud_text = f"Hits: {self.hits}  Misses: {self.misses}  Score: {self.score}  Accuracy: {accuracy:.1f}%"
        hud_surface = font.render(hud_text, True, (255, 255, 255))
        self.window.blit(hud_surface, (20, 20))
        
    def draw_volume_bar(self):
        # Draw volume bar
        #pygame.draw.rect(self.window, (200, 200, 200), self.volume_bar, 2)
        
        # fill parts
        #fill_width = int(self.volume * self.volume_bar.image.get_width())
        #fill_rect = pygame.Rect(self.volume_bar.x, self.volume_bar.y, fill_width, self.volume_bar.image.get_height())
        #pygame.draw.rect(self.window, (0, 200, 0), fill_rect)

        # Drag knob
        #knob_x = self.volume_bar.x + fill_width
        #knob_y = self.volume_bar.y + self.volume_bar.image.get_height() // 2
        
        self.volume_bar.ChangeAnim(7- int(self.volume * 7))
        self.volume_bar.draw(self.window)
        # The max/min to keep knob within bar
        #knob_x = max(self.volume_bar.x, min(knob_x, self.volume_bar.x + self.volume_bar.image.get_width()))
        #pygame.draw.circle(self.window, (255, 0, 0), (knob_x, knob_y), 8)

class Debugger:
    def __init__(self, mode_arg):
        self.mode = mode_arg
    def log(self, message):
        if self.mode == "debug":
            print("Debugger log: " + str(message))
            
    def log_rect(self, name, rect):
        if self.mode == "debug":
            print(f"[DEBUG] {name}: pos={rect.topleft}, size={rect.size}")
class Audio:
    def __init__(self):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(os.path.join(ASSETS_DIR, "Background", "Background music (INGAME).mp3"))
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Error loading audio: " + str(e))

pygame.init()
clock = pygame.time.Clock()
game_instance = Game()

try:
    while True:
        choice = main_menu()
        if choice == "start":
            result = game_instance.start()
            if result == "menu":
                continue
        else:
            break   
finally:
    pygame.quit()
    sys.exit()  






"""# Move this out of the module, handle this on zombie
        if self.lifetime_ms is not None:
            self.age_ms += int(delta_time * 1000)
            if self.age_ms >= self.lifetime_ms:
                self.visible = False
                return
        # To here"""