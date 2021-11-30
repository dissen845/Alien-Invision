import sys
import pygame
from time import sleep
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button


class AlienInvasion():
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.stats = GameStats(self) #экземпляр для хранения игровой статистики
        self.sb = Scoreboard(self) #Экземпляр панели результатов
        self.ship = Ship(self) #создает экземпляр корабля
        self.bullets = pygame.sprite.Group() #создает группу спрайтов выстрелов
        self.aliens = pygame.sprite.Group() # создает группу спрайтов пришельцев

        self._create_fleet()

        # создание кнопки Play
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()    # 1 обрабатывает нажатие клавиш и т.д.

            if self.stats.game_active:
                self.ship.update()      # 2 Перемещает корабль
                self._update_bullets()  # 3 Перемещение снаряда
                self._update_aliens()   # 4 Перемещает пришельца

            self._update_screen()   # 5 отвечает за то, что происходит на экране

    def _check_events(self):
        """Обрабатывает нажатие клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            if event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def start_game(self, key):
        """запускает игру нажатием на кнопку Play или нажатием кнопки P"""
        if key and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            # очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
            # создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()
            # скрывает указатель мыши
            pygame.mouse.set_visible(False)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        self.start_game(button_clicked)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиши"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()  # при нажатии на пробел создает экземпляр снаряда и записывает в группу bullets
        elif event.key == pygame.K_p:
            self.start_game(event)
        elif event.key == pygame.K_1:
            self.settings.optional_level_01()
        elif event.key == pygame.K_2:
            self.settings.optional_level_02()
        elif event.key == pygame.K_0:
            self.settings.initialize_dynamic_settings()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиши"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создает новый снаряд и включает его в группу Bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)  # При нажатии на пробел создает экземпляр класса снаряда
            self.bullets.add(new_bullet)  # Добавляет экземпляр класса в группу спрайтов

    def _update_bullets(self):
        """Обновляет позиции снарядов и удаляет старые снаряды"""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets)) #Проверка удаляюются ли снаряды
        self._check_collisions()

    def _check_collisions(self):
        """Обработка коллизиц снарядов в пришельцами"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            #увеличение уровня
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Обновляет позицию всех пришельцев"""
        self._check_fleet_edges()
        self.aliens.update()
        # Проверка колизии "пришелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем"""
        if self.stats.ship_left > 0:
            #уменьшает кол-во оставшихся кораблей в настройках
            self.stats.ship_left -= 1
            self.sb.prep_ships()
            #очищает список выстрелов и пришельцев
            self.aliens.empty()
            self.bullets.empty()
            #создает новый флот пришельцев и размещает корабль в центр
            self._create_fleet()
            self.ship.center_ship()
            #создает небольшую паузу
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Проверяет добрались ли пришельцы до нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _create_fleet(self):
        """метод для создания флота вторжения"""
        alien = Alien(self)  # Создание одного экземпляра пришельца
        alien_width, alien_height = alien.rect.size  # атрибут для хранения ширини и высоты пришельца
        # вычислили ширину в которую можно поместить пришельцев (с двух сторон отступы в шиирину пришельца)
        available_space_x = self.settings.screen_width - (2 * alien_width)
        # находим общее кол-во пришельцев, которые поместятся в линию
        number_aliens_x = available_space_x // (2 * alien_width)

        """определяем кол-во рядов"""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.y = alien_height + 2 * alien_height * row_number
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Обновляет изображение экрана и отображает новый экран"""
        self.clock.tick(self.FPS)
        self.screen.fill(self.settings.bg_color)  # Фон нашего окна
        self.ship.blitme()  # Создает модель в центре корабля
        for bullet in self.bullets.sprites():  # из группы спрайтов bullets переносит в переменную bullet спрайты
            bullet.draw_bullet()  # рисует спрайт из группы
        self.sb.show_score()
        self.aliens.draw(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button()
        # отображение последнего прорисованного экрана
        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
