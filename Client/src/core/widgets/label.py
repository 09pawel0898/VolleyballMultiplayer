from src.core.widgets.widget import Widget
from src.core.util.vector import Vec2
from src.core.util.utilis import parse_color
import pygame

class Label(Widget):
    def __init__(self,
                 pos: Vec2,
                 text: str,
                 font_size: int,
                 font_color:  str = 'black',
                 font: str = 'Arial',
                 background: str = "clear") -> None:
        super().__init__(pos)
        pygame.sprite.Sprite.__init__(self)
        self._text = text
        self._font_color = parse_color(font_color)
        self._font_face = pygame.font.match_font(font)
        self._font_size = font_size
        self._background = background
        self._font = pygame.font.Font(self._font_face, self._font_size)
        self.update_rendered_content()
        self.rect.topleft = [self.pos.x, self.pos.y]

    def update(self,dt):
        pass

    def render(self):
        pass

    def set_text(self, new_text: str):
        self._text = new_text
        old_top_left = self.rect.topleft
        self.update_rendered_content()
        self.rect.topleft = old_top_left

    def update_rendered_content(self):
        line_surfaces = []
        text_lines = self._text.split("<br>")
        max_width , max_height = 0, 0
        for line in text_lines:
            line_surfaces.append(self._font.render(line, True, self._font_color))
            this_rect = line_surfaces[-1].get_rect()
            if this_rect.width > max_width:
                max_width = this_rect.width
            if this_rect.height > max_height:
                max_height = this_rect.height
        self.image = pygame.Surface((max_width, (self._font_size + 1) * len(text_lines) + 5), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        if self._background != "clear":
            self.image.fill(parse_color(self._background))
        line_pos = 0
        for lineSurface in line_surfaces:
            self.image.blit(lineSurface, [0, line_pos])
            line_pos += self._font_size + 1
        self.rect = self.image.get_rect()