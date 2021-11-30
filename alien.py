import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""Инициализирует пришельца и задает его начальную позицию"""

	def __init__(self, ai_game):
		"""Инициализирует пришельца и задает его начальную позицию"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		#загрузка изображения пришельца и назначение атрибута прямоугольника
		self.image = pygame.image.load('images/submarine.bmp')
		self.image = pygame.transform.scale(self.image, (60, 50))
		self.rect = self.image.get_rect()
		#Устанавливаем местоположение пришельца
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		#Сохранение точной позиции пришельца по оси Х
		self.x = float(self.rect.x)

	def check_edges(self):
		"""Возвращает True, если пришелец находится у края экрана"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <=0:
			return True

	def update(self):
		"""Перемещает пришельца"""
		self.x += (self.settings.alien_speed * self.settings.fleet_direction)
		self.rect.x = self.x