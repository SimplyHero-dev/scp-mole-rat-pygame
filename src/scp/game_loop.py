import pygame as pg
from dataclasses import dataclass
from scp.state import GameState
from scp.asset_loader import IMAGE_SPRITES
from scp.player import Player

DESIRED_FPS = 60

def create_surface(size, flags = pg.SRCALPHA):
    """Create a blank surface.

    Args:
        size: (width, height) of the surface in pixels
        flags: Pygame surface flags. The default gives the surface a
            per-pixel alpha channel so it can be drawn with transparency.

    Returns:
        A new, fully transparent 'pg.Surface'.
    """
    return pg.Surface(size, flags = flags)

@dataclass
class GameLoop:
    """Base class for a screen's event handling and main loop.
    
    Attributes:
        game: Game object that provides the screen, the display wrapper, and the shared game state.
    """
    game: "ScpGame"
    
    def handle_events(self):
        """Process all pending pygame events.
        
        Handles all the shared quit and fullscreen keys, then passes every event
        to 'handle_event' so subclasses can react to it as well.
        """
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
        """Handle a single event. Override in subclasses.

        Args:
            event: The pygame event to handle
        """
        
    def set_state(self, new_state):
        self.game.set_state(new_state)
    
    @property
    def screen(self):
        return self.game.screen
    
    @property
    def state(self):
        """The current 'GameState'."""
        return self.game.state

class GameMenu(GameLoop):
    """The main menu screen."""

    def loop(self):
        """Run the menu until the state is no longer 'GameState.main_menu'."""
        clock = pg.time.Clock()
        background = create_surface(self.game.screen_rect.size)
        background.blit(IMAGE_SPRITES[(False, False, "backdrop")], (0, 0))

        while self.state == GameState.main_menu:
            self.handle_events()
            #repaint background
            self.screen.blit(background, (0, 0))
            # Instruct all sprites to update
            self.game.display.present()
            pg.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)

    def handle_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            self.set_state(GameState.game_playing)

@dataclass
class GamePlaying(GameLoop):
    """The gameplay screen."""
    
    layers: pg.sprite.LayeredUpdates
    player: "Player"
    
    @property
    def mouse_position(self):
        return pg.mouse.get_pos() 
 
    def loop(self):
        clock = pg.time.Clock()
    
        while self.state == GameState.game_playing:
            self.handle_events()
            self.screen.blit(self.game.level_surface, (0, 0))
            self.layers.update()   
            self.layers.draw(self.screen)
            self.game.display.present()
            pg.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)  
