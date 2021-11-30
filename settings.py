class Settings():
	"""Класс для хранения всех настроек игры Alien Invasion"""

	def __init__(self):
		"""Инициализирует настройки игры"""
		#параметры экрана
		self.screen_width = 1200
		self.screen_height = 900
		self.bg_color = (23, 10, 25)
		#Параметры корабля
		self.ship_limit = 3
		#параметры снаряда
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (255, 0, 0)
		self.bullets_allowed = 3
		#Параметры пришельца
		self.fleet_drop_speed = 15
		#темп ускорения
		self.speedup_scale = 2.2
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Инициализирует настройки, изменяющиеся в ходе игры"""

		self.ship_speed = 4.5
		self.bullet_speed = 4.5
		self.alien_speed = 1.0
		self.fleet_direction = 1
		self.alien_points = 50

	def increase_speed(self):
		"""Увеличение настроек сложности"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)

	def optional_level_01(self):
		"""изменяемая сложность"""
		self.ship_speed = 5.5
		self.bullet_speed = 5.5
		self.alien_speed = 2.0

	def optional_level_02(self):
		"""изменяемая сложность"""
		self.ship_speed = 7.5
		self.bullet_speed = 7.5
		self.alien_speed = 5.0