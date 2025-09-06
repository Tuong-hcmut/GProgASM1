import pygame
from dataclasses import dataclass
from typing import List, Optional, Tuple
# This module is using pre-cut frames approach, it can be adapted for atlas approach but i'm too incoherent at this point

class Sprite:
    def __init__(
        self,
        image: pygame.Surface,                             # The sprite image
        x: int,                                            # Horizontal position, top-left corner as anchor, relative to base resolution
        y: int,                                            # Vertical position, top-left corner as anchor, relative to base resolution
        target_height: int,                                # Pixel height to scale to, relative to base resolution
        draw_order: int = 0,                               # Rendering priority (higher = drawn later = on top)
        hitbox_expand: int = 0,                            # Pad the collision box outwards by N pixels, relative to sprite
        visible: bool = True,                              # Flag for whether to draw
        use_hitbox: bool = True,                           # Flag for interactable
        collidable: bool = True,                           # Flag for whether to check collisions
        base_resolution: Tuple[int, int] = (800, 600),     # Intended resolution of the game
        current_resolution: Tuple[int, int] = (800, 600)   # Actual resolution for scaling
    ):
        self.original_image = image                        # Keep unscaled copy
        self.image = image                                 # Scaled copy
        self.x = x * current_resolution[0] / base_resolution[0]
        self.y = y * current_resolution[1] / base_resolution[1]
        self.target_height = target_height
        self.draw_order = draw_order
        self.original_hitbox_expand = hitbox_expand
        self.hitbox_expand = hitbox_expand
        self.visible = visible
        self.use_hitbox = use_hitbox
        self.collidable = collidable
        self.base_resolution = base_resolution
        self.current_resolution = current_resolution
        self.update_scale_static(current_resolution)

    def update_scale_static(self, current_resolution: Tuple[int, int]) -> None:      # Adaptive scaling for static sprites, if animated then use the other one
        sx = current_resolution[0] / self.base_resolution[0]
        sy = current_resolution[1] / self.base_resolution[1]

        w, h = self.original_image.get_size()
        scale_factor = self.target_height / h
        new_size = (int(w * sx * scale_factor), int(h * sy * scale_factor))
        self.image = pygame.transform.scale(self.original_image, new_size)
        self.hitbox_expand = int(self.original_hitbox_expand * sx * scale_factor)

    @property
    def rect(self) -> pygame.Rect:                                        # Le hitbox creator
        if not self.use_hitbox:
            return None
        r = self.image.get_rect(topleft=(self.x, self.y))
        if self.hitbox_expand:                                            # Inflation kink
            r.inflate_ip(2*self.hitbox_expand, 2*self.hitbox_expand)      # Expand by hitbox_expand for each of 4 sides
        return r

    def draw(self, surface: pygame.Surface) -> None:
        if self.visible:
            surface.blit(self.image, (self.x, self.y))                    # Superimpose image onto surface                

    def is_hit(self, point: Tuple[int, int]) -> bool:                     # Literally battleship
        return self.use_hitbox and self.rect.collidepoint(point)


# MetaData
@dataclass
class AnimFrameData:                 # MetaData of a specific animation cycle
    start_frame: int                 # Index of frame 0 of animation, relative to frame 0 of the sprite sheet
    num_frames: int                  # Array length
@dataclass
class AnimData:                          # The sprites and how to navigate them
    images: List[pygame.Surface]         # The sprite sheet
    frame_info: List[AnimFrameData]      # A list of available actions

    def __post_init__(self):             # Input validation
        last_frame = len(self.images)

        for i, anim in enumerate(self.frame_info):
            start = anim.start_frame

            if start < 0:
                raise ValueError(
                    f"AnimFrameData[{i}] start_frame {start} < 0"
                )
            if anim.num_frames <= 0:
                raise ValueError(
                    f"AnimFrameData[{i}] num_frames {anim.num_frames} must be > 0"
                )
            end = start + anim.num_frames
            if end > last_frame:
                raise ValueError(
                    f"AnimFrameData[{i}] overflows image range: "
                    f"end {end} > last frame {last_frame}"
                )


# Animated Sprite
class AnimatedSprite(Sprite):                          # Inherited stuff from Sprite and others, refer to original class if no comment available. Alternatively, "git gud"
    def __init__(
        self,
        anim_data: AnimData,
        current_anim: int = 0,                         # Animation currently playing, refer to frame_info
        anim_fps: float = 24.0,
        x: int = 0,
        y: int = 0,
        target_height: int = 50,
        draw_order: int = 0,
        hitbox_expand: int = 0,
        visible: bool = True,
        use_hitbox: bool = True,
        collidable: bool = True,
        base_resolution: Tuple[int, int] = (800, 600),
        current_resolution: Tuple[int, int] = (800, 600)
    ):
        # Set initial image from starting animation's first frame
        start_frame_index = anim_data.frame_info[current_anim].start_frame
        image = anim_data.images[start_frame_index]

        super().__init__(image, x, y, target_height, draw_order, hitbox_expand, visible, use_hitbox, collidable, base_resolution, current_resolution)

        self.original_images = anim_data.images       
        self.anim_data = anim_data
        self.anim_num = current_anim
        self.frame_num = 0
        self.frame_time = 0.0
        self.anim_fps = float(anim_fps)
        self.update_scale(current_resolution)

    def update_scale(self, current_resolution: Tuple[int, int]) -> None:      # Adaptive scaling
        sx = current_resolution[0] / self.base_resolution[0]
        sy = current_resolution[1] / self.base_resolution[1]

        # Rescale every frame in AnimData
        scaled_images = []
        for img in self.original_images:
            w, h = img.get_size()
            scale_factor = self.target_height / h
            new_size = (int(w * sx * scale_factor), int(h * sy * scale_factor))
            scaled_images.append(pygame.transform.scale(img, new_size))

        self.anim_data.images = scaled_images
        self.image = scaled_images[self.anim_data.frame_info[self.anim_num].start_frame]
        self.hitbox_expand = int(self.original_hitbox_expand * sx * scale_factor)


    def OverrideSprite(self, myData: AnimData, startingAnimNum: int) -> None:      # If we ever got around to making multi-phase bossfights, for now, redundant
        self.anim_data = myData
        self.ChangeAnim(startingAnimNum)

    def ChangeAnim(self, num: int) -> None:                                        # Switch to sequencing another animation
        if num < 0 or num >= len(self.anim_data.frame_info):
            raise ValueError(
                f"Invalid animation index {num}. "
                f"Must be between 0 and {len(self.anim_data.frame_info) - 1}."
            )
        self.anim_num = num
        self.frame_num = 0
        self.frame_time = 0.0

        image_num = self.anim_data.frame_info[self.anim_num].start_frame
        self.image = self.anim_data.images[image_num]

    def UpdateAnim(self, delta_time: float) -> None:                                # Play animation sequence, delta_time refer to time elapsed since last check, fed externally
        # Note: Do NOT forget to set delta_time back to zero after(not here, ofc)
        if (not self.visible) or (self.anim_data.frame_info[self.anim_num].num_frames < 2):                                                        # U can't see me       
            return
        self.frame_time += delta_time                                               # Accumulate frame time
        frame_interval = 1.0 / max(self.anim_fps, 0.0001)                           # Advance frames if it's time, value capped so you don't end up with overflow
        if self.frame_time >= frame_interval:
            steps = int(self.frame_time * self.anim_fps)
            self.frame_num += steps                                                 # Kingu Kurimuzon, skip ahead several frames
            total = self.anim_data.frame_info[self.anim_num].num_frames
            if total > 0:
                self.frame_num %= total                                             # Wrap around, assuming animation is a CYCLE, totally not going to bite me in the ass later
            base = self.anim_data.frame_info[self.anim_num].start_frame
            image_num = base + self.frame_num
            self.image = self.anim_data.images[image_num]                           # Update image to the according coordinates
            self.frame_time = self.frame_time % frame_interval                      # Keep fractional remainder


# Helpers
def _validate_frame_size(sheet: pygame.Surface, frame_w: int, frame_h: int) -> None:
    sheet_w, sheet_h = sheet.get_size()
    if frame_w <= 0 or frame_h <= 0:
        raise ValueError(f"Frame dimensions must be > 0, got {frame_w}x{frame_h}")
    if frame_w > sheet_w or frame_h > sheet_h:
        raise ValueError(
            f"Frame size {frame_w}x{frame_h} larger than sheet {sheet_w}x{sheet_h}"
        )

def _safe_append_frame_info(
    frame_info: List[AnimFrameData],
    start_index: int,
    num_frames: int,
    max_frames: int
) -> None:
    if num_frames <= 0:
        raise ValueError(f"num_frames must be > 0, got {num_frames}")
    if start_index + num_frames > max_frames:
        raise ValueError(
            f"Animation overflows available frames: "
            f"end {start_index + num_frames}, max {max_frames}"
        )
    frame_info.append(AnimFrameData(start_frame=start_index, num_frames=num_frames))
# Sheet Parsing
def load_sheets(
    frame_files: List[str]
) -> List[pygame.Surface]:
    # Loads sheets from file, feed the output from this into the functions below
    return [pygame.image.load(p).convert_alpha() for p in frame_files]

# Takes output from load_sheets and returns output fit for assigning to AnimData
def from_strip_sheets(
    sheets: List[pygame.Surface],
    frame_w: int,
    frame_h: int
) -> Tuple[List[pygame.Surface], List[AnimFrameData]]:
    # Sheets from the same entity, each a strip of animation
    images: List[pygame.Surface] = []
    frame_info: List[AnimFrameData] = []
    start_index = 0

    for sheet in sheets:
        _validate_frame_size(sheet, frame_w, frame_h)
        sheet_w, _ = sheet.get_size()
        num_frames = sheet_w // frame_w

        for i in range(num_frames):
            rect = pygame.Rect(i * frame_w, 0, frame_w, frame_h)
            images.append(sheet.subsurface(rect).copy())      # Subsurface is reference to surface entity

        _safe_append_frame_info(frame_info, start_index, num_frames, len(images))
        start_index += num_frames

    return images, frame_info


def from_frame_list(
    sheets: List[pygame.Surface],
    frame_counts: List[int]
) -> Tuple[List[pygame.Surface], List[AnimFrameData]]:
    # Sheets from the same entity, each a frame of animation
    images: List[pygame.Surface] = [s.copy() for s in sheets]
    frame_info: List[AnimFrameData] = []
    start_index = 0

    for count in frame_counts:
        _safe_append_frame_info(frame_info, start_index, count, len(images))
        start_index += count

    return images, frame_info


def from_multiline_sheet(
    sheet: pygame.Surface,
    frame_w: int,
    frame_h: int,
    frame_counts: List[int]
) -> Tuple[List[pygame.Surface], List[AnimFrameData]]:
    # A complete sprite sheet, newline = new animation
    _validate_frame_size(sheet, frame_w, frame_h)

    images: List[pygame.Surface] = []
    frame_info: List[AnimFrameData] = []
    start_index = 0

    _, sheet_h = sheet.get_size()
    rows = sheet_h // frame_h
    max_rows = min(rows, len(frame_counts))      # Safety check

    for row in range(max_rows):
        row_frames = frame_counts[row]
        for i in range(row_frames):
            rect = pygame.Rect(i * frame_w, row * frame_h, frame_w, frame_h)
            images.append(sheet.subsurface(rect).copy())

        _safe_append_frame_info(frame_info, start_index, row_frames, len(images))
        start_index += row_frames

    return images, frame_info


def from_concat_sheet(
    sheet: pygame.Surface,
    frame_w: int,
    frame_h: int,
    split_points: List[int]
) -> Tuple[List[pygame.Surface], List[AnimFrameData]]:
    """
    A complete sprite sheet, animations laid end-to-end horizontally
    split_points = [frames_in_anim1, frames_in_anim2, ...]
    """
    _validate_frame_size(sheet, frame_w, frame_h)

    images: List[pygame.Surface] = []
    frame_info: List[AnimFrameData] = []
    start_index = 0

    for count in split_points:
        for i in range(count):
            rect = pygame.Rect((start_index + i) * frame_w, 0, frame_w, frame_h)
            images.append(sheet.subsurface(rect).copy())

        _safe_append_frame_info(frame_info, start_index, count, len(images))
        start_index += count

    return images, frame_info


def from_wrapped_sheet(
    sheet: pygame.Surface,
    frame_w: int,
    frame_h: int,
    frame_counts: List[int]
) -> Tuple[List[pygame.Surface], List[AnimFrameData]]:
    """
    A complete sprite sheet, animations laid end-to-end, wrapped
    frame_counts = [frames_in_anim1, frames_in_anim2, ...]
    Frames are read left-to-right, top-to-bottom until count is satisfied.
    """
    _validate_frame_size(sheet, frame_w, frame_h)

    images: List[pygame.Surface] = []
    frame_info: List[AnimFrameData] = []
    start_index = 0

    sheet_w, sheet_h = sheet.get_size()
    total_frames = (sheet_w // frame_w) * (sheet_h // frame_h)

    # Flatten all frames in reading order
    all_frames: List[pygame.Surface] = []
    for y in range(0, sheet_h, frame_h):
        for x in range(0, sheet_w, frame_w):
            if len(all_frames) >= total_frames:
                break
            rect = pygame.Rect(x, y, frame_w, frame_h)
            all_frames.append(sheet.subsurface(rect).copy())

    if sum(frame_counts) > len(all_frames):
        raise ValueError(
            f"Requested {sum(frame_counts)} frames, but only {len(all_frames)} available"
        )

    images.extend(all_frames)

    # Add frame data
    for count in frame_counts:
        _safe_append_frame_info(frame_info, start_index, count, len(images))
        start_index += count

    return images, frame_info