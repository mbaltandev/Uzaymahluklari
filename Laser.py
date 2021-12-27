import pygame

class Laser(pygame.sprite.Sprite):
	def __init__(self,pos,hiz,ekran_yukseklik):
		super().__init__()
		self.image = pygame.Surface((4,20))
		self.image.fill('white')
		self.rect = self.image.get_rect(center = pos)
		self.hiz = hiz
		self.yukseklik_y_kisitlama = ekran_yukseklik




	def update(self):
		self.rect.y += self.hiz
