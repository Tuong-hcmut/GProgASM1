import pygame
import random
import sys
import os
import time
from Sprite import *  # Use Sprite, AnimatedSprite, AnimData, from_multiline_sheet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")

VOLUME_BAR_SHEET_PATH = os.path.join(ASSETS_DIR, "UI", "Charging bars and buttons", "Volume bars.png")

HIT_SOUND_PATH = os.path.join(ASSETS_DIR, "sfx", "SFX hit.mp3")
MUSIC_PATH = os.path.join(ASSETS_DIR, "Background", "Background music (INGAME).mp3")

BASE_RESOLUTION = (1280,720)
TARGET_HEIGHT = 70
# ===== Audio =====
class Audio:
    def __init__(self,current_resolution):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(MUSIC_PATH)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Error loading music:", e)

        try:
            self.hit_sound = pygame.mixer.Sound(HIT_SOUND_PATH)
        except Exception as e:
            print("Error loading hit sound:", e)
            self.hit_sound = None

        # Volume bars
        self.music_bar = VolumeBar(
            x=1000, y=60,  # user-defined positions
            base_resolution=BASE_RESOLUTION,
            current_resolution=current_resolution,
            target_height=TARGET_HEIGHT,
            sound_obj=pygame.mixer.music
        )

        self.hit_bar = None
        if self.hit_sound:
            self.hit_bar = VolumeBar(
                x=1000, y=200,  # below the music bar
                base_resolution=BASE_RESOLUTION,
                current_resolution=current_resolution,
                target_height=TARGET_HEIGHT,
                sound_obj=self.hit_sound
            )

    def play_hit(self):
        """Play hit sound with current volume."""
        if self.hit_sound:
            self.hit_sound.play()

class VolumeBar:
    def __init__(self, x, y, base_resolution, current_resolution, target_height, sound_obj):
        images, frame_info = from_concat_sheet(
            load_sheets([VOLUME_BAR_SHEET_PATH])[0],
            48, 32,
            [1,1,1,1,1,1,1,1]
        )
        volume_bar_anim_data = AnimData(images, frame_info)

        self.sprite = AnimatedSprite(
            anim_data=volume_bar_anim_data,
            anim_fps=0,
            x=x, y=y,
            target_height=target_height,
            base_resolution=BASE_RESOLUTION,
            current_resolution=current_resolution
        )

        self.sound_obj = sound_obj
        self.volume = 0.5
        self.dragging = False
        self._apply_volume()

    def handle_event(self, event):
        knob_radius = 8
        fill_width = int(self.volume * self.sprite.image.get_width())
        knob_x = self.sprite.x + fill_width
        knob_y = self.sprite.y + self.sprite.image.get_height() // 2

        knob_rect = pygame.Rect(
            knob_x - knob_radius,
            knob_y - knob_radius,
            knob_radius * 2,
            knob_radius * 2
        )

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.sprite.is_hit(event.pos) or knob_rect.collidepoint(event.pos):
                self.dragging = True
                self.update_volume(event.pos[0])

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_volume(event.pos[0])

    def update_volume(self, mouse_x):
        relative_x = mouse_x - self.sprite.x
        self.volume = max(0, min(1, relative_x / self.sprite.image.get_width()))
        self._apply_volume()
    
    def _apply_volume(self):
        if self.sound_obj is not None:
            if self.sound_obj == pygame.mixer.music:
                pygame.mixer.music.set_volume(self.volume)
            else:
                self.sound_obj.set_volume(self.volume)

    def draw(self, surface):
        self.sprite.ChangeAnim(7 - int(self.volume * 7))
        self.sprite.draw(surface)