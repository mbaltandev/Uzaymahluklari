import pygame

import Mahlukatlar
from Laser import Laser
from Mahlukatlar import *

class Kahraman(pygame.sprite.Sprite):
    def __init__(self,pos,kisitlama,hiz,can):
        super().__init__()
        self.image=pygame.image.load("grafikler\player.png").convert_alpha()
        self.rect=self.image.get_rect(midbottom=pos)
        self.hiz = hiz
        self.max_x_kisitlama = kisitlama
        self.hazir = True
        self.lazer_suresi = 0
        self.lazer_bekleme_suresi = 600
        self.lazerler = pygame.sprite.Group()
        self.can = can
        self.lazer_ses= pygame.mixer.Sound("sesler/laser.wav")
        self.lazer_ses.set_volume(0.5)

    def kisitlama(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_kisitlama:
            self.rect.right = self.max_x_kisitlama

    def tuslama(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.hiz
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.hiz
        if keys[pygame.K_SPACE] and self.hazir:
            self.lazer_ses.set_volume(0.02)
            self.lazer_ates()
            self.hazir = False
            self.lazer_suresi = pygame.time.get_ticks()
            self.lazer_ses.play()

    def sarj(self):
        if not self.hazir:
            zaman = pygame.time.get_ticks()
            if zaman - self.lazer_suresi >= self.lazer_bekleme_suresi:
                self.hazir = True

    def lazer_ates(self):
        print("ates ediyo")
        self.lazerler.add(Laser(self.rect.center, -8, self.rect.bottom))

    def update(self):
        self.tuslama()
        self.kisitlama()
        self.sarj()
        self.lazerler.update()


