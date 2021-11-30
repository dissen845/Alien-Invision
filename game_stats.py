import json

class GameStats():
    """Статистика игры Alien Invasion"""

    def __init__(self, ai_game):
        """Инициализирует статистику"""
        filename = 'numbers.json'
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        #Рекорд. Рекорд не должен сбрасываться
        with open(filename) as f:
            numbers = json.load(f)
        self.hight_score = numbers

    def reset_stats(self):
        """Инициализирует статистику во время игры"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1