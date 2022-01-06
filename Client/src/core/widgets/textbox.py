from src.core.widgets.widget import Widget
from src.core.util.vector import Vec2
from src.core.util.utilis import parse_color
import pygame

class TextBox(Widget):
    def __init__(self,
                 pos: Vec2,
                 initial_text,
                 width, case,
                 max_length,
                 font,
                 font_size,
                 background = "white",
                 border = True):
        super().__init__(pos)
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        self.width = width
        self.case = case
        self.maxLength = max_length
        self.font = font
        self.fontSize = font_size
        self.background = background
        self.border = border
        self.initialText = initial_text
        self.boxSize = int(font_size * 1.7)
        self.bInitialized = False
        self.bCovered = False
        self.bInputEnabled = False

        self._init_text_box()

    def _init_text_box(self):
        self.image = pygame.Surface((self.width, self.boxSize), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos.x, self.pos.y]

        if self.background != "clear":
            self.image.fill(parse_color(self.background))

        if self.border is not False:
            pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
        self.rect = self.image.get_rect()
        self.fontFace = pygame.font.match_font(self.font)
        self.fontColour = pygame.Color("black")
        self.initialColour = (180, 180, 180)
        self.font = pygame.font.Font(self.fontFace, self.fontSize)
        self.image.blit(self.font.render(self.initialText, True, self.initialColour), [10, 5])
        self.rect.left -= 1000

    def render(self):
        pass

    def update(self):
        if not self.bInitialized:
            self.bInitialized = True
            self.rect.topleft = [self.pos.x, self.pos.y]
        mouse_pos = pygame.mouse.get_pos()
        if self._cursor_in_bounds(mouse_pos):
            self.bCovered = True
            #print("Covered")
        else:
            #print("NotCovered")
            self.bCovered = False

    def check_for_onclick(self):
        if self.bCovered:
            if not self.bInputEnabled:
                print("InputEnabled")
                self.enable_input_to_this(True)

    def enable_input_to_this(self, enabled):
        self.bInputEnabled = enabled


    def _cursor_in_bounds(self, mouse_pos):
        if self.rect.left <= mouse_pos[0] <= self.rect.right and self.rect.top <= mouse_pos[1] <= self.rect.bottom:
            return True
        else:
            return False

    def handle_input_events(self, events):
        if self.bInputEnabled:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.clear()
                    elif event.key == pygame.K_ESCAPE:
                        self.enable_input_to_this(False)
                        #self.image.blit(self.font.render(self.initialText, True, self.initialColour), [10, 5])
                        print("InputDisabled")
                    elif event.key != pygame.K_ESCAPE:
                        self._try_add_character(event)


    def _try_add_character(self, key_event : pygame.event.Event):
        pass
        key = key_event.key
        unicode = key_event.unicode
        if (31 < key < 127 or 255 < key < 266) and (
                self.maxLength == 0 or len(self.text) < self.maxLength):  # only printable characters
            if key_event.mod in (1, 2,4096) and self.case == 1 and 97 <= key <= 122:
                # force lowercase letters
                self.text += chr(key)
            elif key_event.mod == 0 and self.case == 2 and 97 <= key <= 122:
                self.text += chr(key - 32)
            else:
                # use the unicode char
                self.text += unicode

        elif key == 8:
            # backspace. repeat until clear
            next_time = pygame.time.get_ticks() + 200
            deleting = True
            while deleting:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_BACKSPACE]:
                    this_time = pygame.time.get_ticks()
                    if this_time > next_time:
                        self.text = self.text[0:len(self.text) - 1]
                        self.image.fill((255, 255, 255))
                        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
                        self.image.blit(self.font.render(self.text, True, self.fontColour), [10, 5])
                        next_time = this_time + 50
                        pygame.event.clear()
                else:
                    deleting = False

        if self.background != "clear":
            self.image.fill(parse_color(self.background))

        if self.border is not False:
            pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)

        self.image.blit(self.font.render(self.text, True, self.fontColour), [10, 5])

    def move(self, x_pos, y_pos, centre=False):
        if centre:
            self.rect.topleft = [x_pos, y_pos]
        else:
            self.rect.center = [x_pos, y_pos]

    def clear(self):
        if self.background != "clear":
            self.image.fill(parse_color(self.background))

        if self.border is not False:
            pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
        self.image.blit(self.font.render(self.initialText, True, self.initialColour), [10, 5])