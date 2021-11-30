import pygame.font

class Button():
    """Класс кнопки для вывода на экран"""

    def __init__(self, ai_game, msg):
        """инициализирует атрибуты кнопки"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # Размер и свойства кнопки
        self.width = 200
        self.height = 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        #Построение прямоугольника кнопки и выравнивание её по центру
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Преобразует текст msg в прямоугольник и выравнивает по центру экрана"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """отображение пустой кнопки и вывод сообщания"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)