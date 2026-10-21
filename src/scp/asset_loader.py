import pygame as pg
import importlib.resources

def load(module_path, name):
    ref = importlib.resources.files(module_path) / name
    return importlib.resources.as_file(ref)

def import_image(asset_name: str):
    with load("scp.assets.gfx", asset_name) as resource:
        return pg.image.load(resource).convert_alpha()

def import_sound(asset_name: str):
    with load("scp.assets.audio", asset_name) as resource:
        return pg.mixer.Sound(resource)
    
channels = {
    "score": None,
}

def import_spritesheet(asset_name: str, frame_width: int, frame_height: int):
    """
    Loads a spritesheet and slices it into individual frame Surfaces, reading left-to-right, top-to-bottom.
    """
    with load ("scp.assets.gfx", asset_name) as resource:
        sheet = pg.image.load(resource).convert_alpha()
        
    sheet_width, sheet_height = sheet.get_size()
    frames = []
    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            frame = sheet.subsurface(pg.Rect(x, y, frame_width, frame_height)).copy()
            frames.append(frame)
    return frames

def load_all_sounds():
    for channel_id, channel_name in enumerate(channels):
        channels[channel_name] = pg.mixer.Channel(channel_id)
        # Configure the volume here
        channels[channel_name].set_volume(1.0)
        

SPRITES = {
    "backdrop": "background.png",
    "blank": "blank.png",
}

IMAGE_SPRITES = {}

def load_all_images():
    for sprite_index, sprite_name in SPRITES.items():
        img = import_image(sprite_name)
        for flipped_x in (True, False):
            for flipped_y in (True, False):
                new_img = pg.transform.flip(img, flip_x = flipped_x, flip_y = flipped_y)
                IMAGE_SPRITES[(flipped_x, flipped_y, sprite_index)] = new_img
