import sys
import pygame
from settings import Settings
from bullet import Bullet
from alien import Alien
from time import sleep
from scoreboard import Scoreboard

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    """如果子弹还没有到达限制，就发射一颗子弹"""
    #创建新子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)        
        
def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets, stats, play_button, 
        aliens, scoreboard):
    """监测键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('highscore.txt', 'w') as hs:
                hs.write(str(stats.high_score))
            sys.exit()            
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)    
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(play_button, mouse_x, mouse_y, stats, aliens, 
                bullets, ship, ai_settings, screen, scoreboard)
 
def check_play_button(play_button, mouse_x, mouse_y, stats, aliens, bullets, 
        ship, ai_settings, screen, scoreboard):
    """在玩家单击play按钮时开始游戏"""
    play_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if play_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        #重置记分牌图像
        scoreboard.prep_images()
        #清空外星人和子弹
        aliens.empty()
        bullets.empty()
        
        #重新绘制外星人群，并将飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
               
            
def update_screen(ai_settings, screen, ship, aliens, bullets, stats,
        play_button, scoreboard):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.fill(ai_settings.bg_color)
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    scoreboard.show_score()
    
    if not stats.game_active:
        play_button.draw_button()
    
    #让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, 
        scoreboard):
    """更新子弹的位置，并删除已消失的子弹"""
    #更新子弹的位置
    bullets.update()
    
    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, 
            stats, scoreboard)
    
def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, 
        stats, scoreboard):           
    """响应子弹和外星人的碰撞"""
    #如果碰撞了，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)
    if len(aliens) == 0:
        start_new_level(bullets, ai_settings, screen, ship, aliens, stats, 
                scoreboard)

def start_new_level(bullets, ai_settings, screen, ship, aliens, stats, 
        scoreboard):
    #开始新的等级：删除现有的子弹并新建一群外星人
    bullets.empty()
    create_fleet(ai_settings, screen, ship, aliens)
    ai_settings.increase_speed()
    stats.level += 1
    scoreboard.prep_level()
        
def check_high_score(stats, scoreboard):
    #比对最高分，看是否需要更新最高得分榜
    if stats.score >= stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()

def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可以容纳多少外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x
    
def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - ship_height - 
            (3 * alien_height))
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建外星人"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width*alien_number 
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height*row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    """创建一个外星人，并计算每行可容纳多少个外星人"""
    alien = Alien(ai_settings, screen)
    number_aliens_x  = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, 
            alien.rect.height)
    
    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
 
def check_fleet_edges(ai_settings, aliens):
    """检查外星人群是否到达屏幕边缘，有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_deges():
            change_fleet_direction(ai_settings, aliens)
            break
            
def change_fleet_direction(ai_settings, aliens):
    """外星人碰到屏幕边缘后，向下移动，并改变水平移动方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, 
        scoreboard):
    """在外星人到达屏幕边缘时，向下移动并更改水平移动方向"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, scoreboard)
        print("Ship hit!!!")
    #检测外星人是否到达屏幕底部
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, 
            scoreboard)
        
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, scoreboard):
    """响应外星人撞到飞船"""
    #在飞船还有余数的情况下
    if stats.ships_left > 0:
        #飞船数目减一
        stats.ships_left -= 1
        scoreboard.prep_ships()
        #清空子弹和余下的外星人
        bullets.empty()
        aliens.empty()
    
        #创建一群新的外星人
        create_fleet(ai_settings, screen, ship, aliens)
        
        #将飞船放置到屏幕中间
        ship.center_ship()
    
        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, 
        scoreboard):
    """检测外星人到达屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, 
                    scoreboard)
            break

    