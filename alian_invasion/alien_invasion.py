import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from button import Button
import game_functions as gf
from game_stats import GameStats
from scoreboard import Scoreboard


def run_game():
    # 初始化pygame，标题，设置和屏幕对象
    pygame.init()
    pygame.display.set_caption("Alien Invasion")
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.
                                     screen_height))

    # 创建一艘飞船，一个子弹编组，一个外星人编组
    ship = Ship(screen, ai_settings)
    bullets = Group()
    aliens = Group()

    # 创建外星人群
    gf.creat_fleet(ai_settings, screen, ship, aliens)
    # 创建play按钮
    play_button = Button(ai_settings, screen, "Play")
    # 创建一个用于储存游戏统计信息的实例, 并创建计分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ship, screen, bullets, ai_settings, stats, play_button, aliens, sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb)
        gf.update_screen(ai_settings, screen, stats, ship, bullets, aliens, play_button, sb)


run_game()
