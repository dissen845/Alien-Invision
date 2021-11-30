import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""Класс для управления снарядами корабля"""

	def __init__(self, ai_game):
		"""Создает объект снарядов в текущей позиции корабля."""
		super().__init__() #инициализирует атрибуты класса Sprite
		self.screen = ai_game.screen #присваивает значение от значения экрана основного класса
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color

		#создание снаряда в позиции (0, 0)
		self.rect = pygame.Rect(0, 0, self.settings.bullet_width, 
			self.settings.bullet_height) #Задает координаты 0, 0 и длину и ширину прямоугольника спрайта
		self.rect.midtop = ai_game.ship.rect.midtop #Присваивает значение положения прямоугольника пули к прямоугольнику корабля

		self.y = float(self.rect.y) #координата снаряда в вещественном формате

	def update(self):
		"""Перемещает снаряд вверх по экрану"""
		self.y -= self.settings.bullet_speed
		#Обновление позиции прямоугольника
		self.rect.y = self.y

	def draw_bullet(self):
		"""Рисует снаряд на экране"""
		pygame.draw.rect(self.screen, self.color, self.rect)