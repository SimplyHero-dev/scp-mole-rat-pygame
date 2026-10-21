import pygame as pg
import random
from dataclasses import dataclass
from scp.state import GameState
from scp.display import Display
from scp.grid import create_tile_map, tile_positions 
from scp.sprites import Background
from scp.asset_loader import IMAGE_SPRITES
from scp.sprite_manager import Spritemanager

DESIRED_FPS = 60

def create_surface(size, flags = pg.SRCALPHA):
    return pg.Surface(size, flags = flags)

@dataclass
class GameLoop:
    game: "ScpGame"
    
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.set_state(GameState.quitting)
            
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.set_state(GameState.quitting)
                    
                elif event.key == pg.K_f:
                    self.game.display.toggle_fullscreen()
                
            self.handle_event(event)
            
    def loop(self):
        while self.state != GameState.quitting:
            self.handle_events()
            
    def handle_event(self, event):
        pass
        
    def set_state(self, new_state):
        self.game.set_state(new_state)
    
    @property
    def screen(self):
        return self.game.screen
    
    @property
    def state(self):
        return self.game.state

class GameMenu(GameLoop):

    def create_level(self):
        background_tiles = create_tile_map()
        for (gy, gx, x, y) in tile_positions():
            background_tile = Background.create_from_tile(
                groups = [],
                index = "blank",
            )
            background_tile.rect.topleft = (x, y)
            background_tiles[gy][gx] = background_tile
        return background_tiles

    def draw_background(self):
        self.background.blit(IMAGE_SPRITES[(False, False, "backdrop")], (0, 0))
        for (gy, gx, x, y) in tile_positions():
            background_tile = self.level[gy][gx]
            self.background.blit(background_tile.image, (x, y))

    def loop(self):
        clock = pg.time.Clock()
        self.background = create_surface(self.game.screen_rect.size)

        self.level = self.create_level()
        self.draw_background()

        group = pg.sprite.LayeredUpdates()

        while self.state == GameState.main_menu:
            self.handle_events()
            #repaint background
            self.screen.blit(self.background, (0, 0))
            # Instruct all sprites to update
            group.update()
            # Tell the group where to draw
            group.draw(self.screen)
            self.game.display.present()
            pg.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)

    def handle_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_e:
            self.game.game_editing.level = self.level
            self.game.game_editing.sprite_manager.level = self.level
            self.set_state(GameState.map_editing)

@dataclass
class GameEditing(GameLoop):
    layers: pg.sprite.LayeredUpdates
    sprite_manager: Spritemanager
    level: list
    spawn: callable = None
    
    @property
    def mouse_position(self):
        return pg.mouse.get_pos() 
 
    def loop(self):
        clock = pg.time.Clock()
        background = create_surface(self.game.screen_rect.size)
        background.blit(IMAGE_SPRITES[(False, False, "backdrop")], (0, 0))
    
        while self.state in (GameState.map_editing, GameState.game_playing):
            self.handle_events()
            self.screen.blit(background, (0, 0))
            self.layers.update()   
            self.layers.draw(self.screen)
    
            self.game.display.present()
            pg.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)  
