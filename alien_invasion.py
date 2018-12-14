import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard                  

def run_game():
    """初始化游戏并设置屏幕"""
    pygame.init()
    ai_settings = Settings() 
    screen = pygame.display.set_mode((ai_settings.screen_width, 
            ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    #创建一个play按钮
    play_button = Button(screen, "play")
    
    #创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    
    #创建一艘飞船、一个子弹编组和一个外星人编组
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    
    #创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    #创建得分板
    scoreboard = Scoreboard(ai_settings, screen, stats)
        
    #开始游戏主循环
    while True:
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, 
                aliens, scoreboard)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets,
                    stats, scoreboard)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, 
                    scoreboard)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets, stats, 
                play_button, scoreboard)

run_game()
