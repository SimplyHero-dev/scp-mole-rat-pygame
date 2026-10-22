import pygame as pg


class Display:
    def __init__(self, size, fullscreen=False):
        self.size = size
        self.fullscreen = fullscreen
        
        self.game_surface = pg.Surface(size)
        self.window = None
        
        self._create_window()
        
    def _create_window(self):
        if self.fullscreen:
            self.window = pg.display.set_mode(
                (0, 0), pg.FULLSCREEN
            )
        else:
            self.window = pg.display.set_mode(
                (1280, 720), pg.RESIZABLE
            )
            
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self._create_window()

    def present(self):
        """Scale and display the game surface in the current window.
        
        Scales the fixed-resolution game surface to fit the window while
        preserving its aspect ratio. Centers the scaled image and fills
        the remaining space with black bars when necessary.
        """
        
        # black out the entire window/screen.
        self.window.fill((0, 0, 0))
        
        window_width, window_height = self.window.get_size()
        game_width, game_height = self.size
        
        scale = min(
            window_width / game_width,
            window_height / game_height,
        )

        scaled_size = (
            round(game_width * scale),
            round(game_height * scale),
        )
        
        scaled = pg.transform.scale(
            self.game_surface, scaled_size
        )

        x = (window_width - scaled_size[0]) // 2
        y = (window_height - scaled_size[1]) // 2
        
        self.window.blit(scaled, (x, y))
        pg.display.flip()
