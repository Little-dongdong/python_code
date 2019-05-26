import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


'''键鼠事件'''
def check_events(ship, screen, bullets, ai_settings, stats, play_button, aliens, sb):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ship, screen, bullets, ai_settings)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y, sb)

'''按钮'''
def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y, sb):
    """在玩家单价play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #  重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #  隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计数据
        stats.reset_stats()
        sb.show_score()
        stats.game_active = True
        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并让飞船居中
        creat_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_keydown_event(event, ship, screen, bullets, ai_settings):
    # 按下方向键
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    if event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    # 创建一颗子弹， 并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_event(event, ship):
    # 松开方向键
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False




'''子弹'''
def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
    '''更新子弹的位置，并删除已消失的子弹'''
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, sb, stats)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, sb, stats):
    '''相应发生碰撞的子弹和外星人'''
    # 检测是否有子弹击中外星人，并删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # 若消灭完外星人就删除现有子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        # 提高等级
        stats.level += 1
        sb.prep_level()
        creat_fleet(ai_settings, screen, ship, aliens)




'''外星人'''
def creat_fleet(ai_settings, screen, ship, aliens):
    '''创建外星人群'''
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            creat_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(ai_settings, alien_width):
    '''计算每行可容纳多少个外星人'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''计算屏幕可容纳多少行外星人'''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def creat_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''创建一个外星人并将其放在当前行'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien_height = alien.rect.height
    alien.y = alien_height + 2 * alien_height * row_number
    alien.rect.y = alien.y
    aliens.add(alien)

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
    '''检查是否有外星人位于屏幕边缘，并更新整群外星人的位置'''
    change_direction(ai_settings, aliens)
    aliens.update()
    # 检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
    # 检测是否有外星人到达了底部
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)

def change_direction(ai_settings, aliens):
    '''一直向下运动，到达边缘换方向'''
    for alien in aliens.sprites():
        alien.y += ai_settings.fleet_drop_speed
        alien.rect.y = alien.y
    for alien in aliens.sprites():
        if alien.check_edges():
            ai_settings.fleet_direction *= -1
            break

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    '''检查是否有外星人到达了屏幕底部'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到了一样处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break




'''飞船'''
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    '''响应被外星人撞到的飞船'''
    if stats.ships_left > 0:
        # 将ship_left减1
        stats.ships_left -= 1
        # 清空记分牌
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底部中央
        creat_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)





''''计分'''
def check_high_score(stats, sb):
    '''检查是否诞生了新的最高分'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()






'''屏幕刷新'''
def update_screen(ai_settings, screen, stats, ship, bullets, aliens, play_bullon, sb):
    '''更新屏幕上的图像，并切换到新屏幕'''
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 显示得分
    sb.show_score()

    # 如果游戏处于非活跃状态，就绘制Play按钮
    if not stats.game_active:
        play_bullon.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()