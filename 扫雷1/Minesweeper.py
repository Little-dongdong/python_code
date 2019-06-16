import pygame
import os
from sys import exit 
import random

# 初始化pygame
pygame.init()

# 背景图地址
bg_img = 'ui/background_2.jpg'

# 图标地址
# 前8是数字，9是旗帜, 10是问号, 11是地雷
num_img = ('ui/num_0.png',
           'ui/num_1.png',
           'ui/num_2.png',
           'ui/num_3.png',
           'ui/num_4.png',
           'ui/num_5.png',
           'ui/num_6.png',
           'ui/num_7.png',
           'ui/num_8.png',
           'ui/num_9.png',
           'ui/num_10.png',
           'ui/num_11.png'
           )

# GUI 对象
screen = pygame.display.set_mode((900, 510), 0, 32)
pygame.display.set_caption('扫雷')
background = pygame.image.load(bg_img).convert()
font = pygame.font.Font(None, 32)
pos_t = pygame.font.Font(None, 32)


# 游戏变量
GameOver = 0
ms_number = 99
grid_number = 30 * 16 - ms_number
vis = [[0 for x in range(18)] for y in range(32)]
vv = [[0 for x in range(18)] for y in range(32)]
di = [[0, 1], [0, -1], [-1, 0], [1, 0], [1, -1], [-1, 1], [1, 1], [-1, -1]]


def init():
    global GameOver
    GameOver = 0
    global ms_number
    ms_number = 99
    global grid_number
    grid_number = 16 * 30 - ms_number

    for i in range(0, 30):
        for j in range(0, 16):
            vis[i][j] = 0
            vv[i][j] = 0
    
    ans = 0
    while ans < ms_number:
        x = random.randint(0, 29)
        y = random.randint(0, 15)
        
        if(vis[x][y] == 0):
            vis[x][y] = -1
            ans += 1
            
    for i in range(0, 30):
        for j in range(0, 16):
            if vis[i][j] == 0:
                for k in range(0, 8):
                    xx = i + di[k][0]
                    yy = j + di[k][1]
                    if (0 <= xx < 30) and (0 <= yy < 16) and (vis[xx][yy] == -1):
                        vis[i][j] += 1


def dfs(x, y):
    vv[x][y] = 1
    ans = 1
    if vis[x][y] == 0:
        for k in range(0, 8):
            xx = x + di[k][0]
            yy = y + di[k][1]
            if (0 <= xx < 30) and (0 <= yy < 16) and (vv[xx][yy] == 0) and (vis[xx][yy] != -1):
                ans += dfs(xx, yy)
    return ans


init()


# 显示(x, y)位置的图片
def blit_png(num, x, y):

    x = x * 30
    y = y * 30 + 30
    image_png = pygame.image.load(num_img[num]).convert_alpha()
    screen.blit(image_png, (x, y))


# 遍历所有位置
def display(game_f):
    
    for i in range(0, 30):
        for j in range(0, 16):
            if vv[i][j] > 0:
                blit_png(vis[i][j], i, j)
            # 标记旗帜
            elif vv[i][j] == -1:
                blit_png(9, i, j)
            # 问号
            elif vv[i][j] == -2:
                blit_png(10, i, j)

            # 如果游戏结束，输出所有地雷
            if (game_f == -1) and (vis[i][j] == -1) and (vv[i][j] == 0):
                blit_png(11, i, j)


while True:
    event = pygame.event.wait()

    # 退出
    if event.type == pygame.QUIT:
        exit()

    # 绘画背景和已确定格子
    screen.blit(background, (0, 0))
    display(GameOver)
    
    # 左上角显示剩余地雷数
    text = font.render("number of mines: %d" % ms_number, 1, (0, 0, 0))
    screen.blit(text, (0, 0))
    
    if GameOver == 0:
        # 按下鼠标按钮
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 定位鼠标按下时候的x,y坐标，相对于显示屏左上角
            x, y = pygame.mouse.get_pos()
            # 返回表示所有鼠标按钮状态的布尔序列 get_pressed() -> (button1, button2, button3)
            pressed_array = pygame.mouse.get_pressed()

            if y < 30:
                continue

            xx = x // 30
            yy = (y - 30) // 30
                
            # 点击鼠标左键
            if pressed_array[0]:
                # 点中地雷
                if vis[xx][yy] == -1 and vv[xx][yy] == 0:
                    GameOver = -1
                    continue
                
                # 相邻8个位置有至少一个雷
                elif vis[xx][yy] >= 0:
                    grid_number -= dfs(xx, yy)
            
            # 单击鼠标右键
            elif pressed_array[2]:
                
                if vv[xx][yy] <= 0:
                
                    vv[xx][yy] = (vv[xx][yy] - 1) % -3
                    
                    if vv[xx][yy] == -1:
                        ms_number -= 1
                    elif vv[xx][yy] == -2:
                        ms_number += 1
            
            # 游戏胜利
            if grid_number == 0:
                GameOver = 1

    # 游戏胜利
    elif GameOver == 1:
        text = font.render("Accepted!", 1, (150, 0, 0))
        screen.blit(text, (400, 170))

    # 游戏失败
    elif GameOver == -1:
        text = font.render("Sorry, game over...", 1, (0, 0, 0))
        screen.blit(text, (350, 200))

    if (GameOver != 0) and (event.type == pygame.MOUSEBUTTONDOWN):
        init()

    pygame.display.update()
