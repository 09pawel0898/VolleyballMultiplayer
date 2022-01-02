import pygame

class Texture:
    def __init__(self) -> None:
        self.image = None
        self.path = None

    def load_from_file(self, path: str) -> bool:
        self.image = pygame.image.load(path).convert_alpha()
        if self.image is not None:
            self.path = path
            return True
        else:
            return False

