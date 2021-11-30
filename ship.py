import pygame
from settings import Settings
from pygame.sprite import Sprite

class Ship(Sprite):
	"""Класс корабля"""

	def __init__(self, ai_game):
		"""Инициализирует корабль и задает его начальную позицию"""
		super().__init__()
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		self.settings = Settings()

		#Загружаем изображение корабля и получаем прямоугольник
		self.image = pygame.image.load('images/ship_01.png')
		self.image = pygame.transform.scale(self.image, (40, 60))
		self.rect = self.image.get_rect()

		#Каждый новый корабль появляется у нижнего края экрана
		self.rect.midbottom = self.screen_rect.midbottom
		#Флаг перемещения вправо
		self.moving_right = False
		#Флаг перемещения влево
		self.moving_left = False

		self.x = float(self.rect.x)

	def update(self):
		"""Обновляет позицию корабля с учетом флага"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed

		self.rect.x = self.x

	def blitme(self):
		"""Рисует корабль в текущей позиции."""
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		"""размещает корабль по центру низа экрана"""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)