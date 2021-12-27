import pygame

class Mahlukat(pygame.sprite.Sprite):
    def __init__(self, renk, x, y):
        super().__init__()


        self.image = pygame.image.load("grafikler//"+renk+".png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

        if renk == 'kirmizi':
            self.deger = 100
        elif renk == 'yesil':
            self.deger = 200
        else:
            self.deger = 300

    def update(self, yon):
        self.rect.x += yon


class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_w):
        super().__init__()
        self.image = pygame.image.load("grafikler/extra.png").convert_alpha()

        if side == 'sag':
            x = screen_w + 50
            self.hiz = - 3
        else:
            x = -50
            self.hiz = 3

        self.rect = self.image.get_rect(topleft=(x, 80))

    def update(self):
        self.rect.x += self.hiz