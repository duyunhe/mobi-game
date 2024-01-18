# -*- coding: utf-8 -*-
# @time     : 2023/12/8 14:10
# @author   : yhdu@tongwoo.cn
# @desc     :    
# @file     : soduko.py
# @software : PyCharm

import pygame
from pygame.locals import *
import sys
import copy
from itertools import permutations
import random
from loguru import logger
from typing import Tuple

ans = []
N = 4
mat = [[-1] * 4 for _ in range(4)]
raw_mat = []
choose_pos = (-1, -1)
image_on = True
success = False
row_error = [0] * N
col_error = [0] * N
dfs_fin = 0
sys_font = "C:\\Windows\\Fonts\\msyh.ttc"
hint = "你好，杜楚予"
X0 = 100
Y0 = 100
GRID_WIDTH = 100
time_index = 0
cat_images = []

direction = {
    "left": [0, -1],
    "right": [0, 1],
    "up": [-1, 0],
    "down": [1, 0]
}


def dfs(r):
    global dfs_fin
    if r == N:
        dfs_fin = 1
        return
    if dfs_fin:
        return
    v = [i + 1 for i in range(N)]
    for t in permutations(v):
        ok = 1
        for i in range(4):
            mat[r][i] = t[i]
            if not check_col(mat, i):
                ok = 0
        if ok:
            dfs(r + 1)
        if dfs_fin:
            return
        for i in range(4):
            mat[r][i] = -1


def gene_soduko():
    # 生成答案
    v = [i + 1 for i in range(N)]
    random.seed(0)
    ri = random.randint(0, 23)
    idx = 0
    for t in permutations(v):
        if idx >= ri:
            for i in range(4):
                mat[0][i] = t[i]
            break
        idx += 1
    dfs(1)
    # 放四个?
    for i in range(N):
        ri = random.randint(0, N - 1)
        mat[i][ri] = -1
    # 再放四个?
    ticket = 4
    while ticket:
        ri = random.randint(0, 15)
        r, c = ri // N, ri % N
        if mat[r][c] != -1:
            ticket -= 1
            mat[r][c] = -1


def check_ans():
    """
    检查是否完成数独
    :return:
    """
    for i in range(N):
        for j in range(N):
            if ans[i][j] == -1:
                return False
    for i in range(N):
        if not check_row(ans, i):
            return False
    for i in range(N):
        if not check_col(ans, i):
            return False
    return True


def check_row(check_mat, r: int):
    vis = [0] * (N + 1)
    for i in range(N):
        if check_mat[r][i] == -1:
            continue
        if vis[check_mat[r][i]]:
            return False
        vis[check_mat[r][i]] = 1
    return True


def check_col(check_mat, c: int):
    vis = [0] * (N + 1)
    for i in range(N):
        if check_mat[i][c] == -1:
            continue
        if vis[check_mat[i][c]]:
            return False
        vis[check_mat[i][c]] = 1
    return True


def get_pos(r: int, c: int, x0: int, y0: int, width: int) -> Tuple:
    """
    获取方格中心坐标 x, y
    :param r: 从上往下第r行 0...r
    :param c: 从左往右第c列 0...c
    :param x0: 左上角x坐标
    :param y0: 左上角y坐标
    :param width: 方格边长
    :return:
    """
    return c * width + width // 2 + x0, r * width + width // 2 + y0


def get_row_col(x, y) -> Tuple:
    r = (y - Y0) // GRID_WIDTH
    c = (x - X0) // GRID_WIDTH
    if r < 0 or r > 3 or c < 0 or c > 3:
        return -1, -1
    return r, c


def draw_grid(screen):
    line_color = (0, 255, 0)
    for y in range(100, 501, 100):
        pygame.draw.line(screen, line_color, [100, y], [500, y])
    for x in range(100, 501, 100):
        pygame.draw.line(screen, line_color, [x, 100], [x, 500])


def draw_select_grid(screen):
    line_color = (255, 255, 255)
    r, c = choose_pos
    x0 = X0 + GRID_WIDTH * c
    y0 = Y0 + GRID_WIDTH * r
    x1, y1 = x0 + GRID_WIDTH, y0 + GRID_WIDTH
    OFFSET = 5
    x0, y0 = x0 + OFFSET, y0 + OFFSET
    x1, y1 = x1 - OFFSET, y1 - OFFSET
    pygame.draw.line(screen, line_color, [x0, y0], [x1, y0])
    pygame.draw.line(screen, line_color, [x0, y0], [x0, y1])
    pygame.draw.line(screen, line_color, [x1, y0], [x1, y1])
    pygame.draw.line(screen, line_color, [x0, y1], [x1, y1])


def draw_mat(screen):
    global ans, raw_mat, row_error, col_error
    font = pygame.font.SysFont(sys_font, 75)
    font_color = (0, 255, 255)
    qm_color = (255, 255, 0)
    error_color = (220, 20, 60)
    black_color = (0, 0, 0)
    right_color = (0, 255, 127)
    for i in range(4):
        for j in range(4):
            a = ans[i][j]
            if a == -1:
                s = '?'
                color = qm_color
            else:
                s = str(a)
                color = font_color
            if row_error[i] == ans[i][j] or col_error[j] == ans[i][j]:
                color = error_color
            else:
                if raw_mat[i][j] == -1:
                    color = right_color
            global image_on
            if image_on and i == choose_pos[0] and j == choose_pos[1] and raw_mat[i][j] == -1:
                color = black_color
            text = font.render(s, True, color)
            x, y = get_pos(i, j, 100, 100, 100)
            screen.blit(text, (x - 15, y - 20))


def draw_text(screen):
    global hint
    fontObj = pygame.font.Font(sys_font, 32)
    # render方法返回Surface对象
    font_color = (222, 49, 99)
    BLACK = (0, 0, 0)
    textSurfaceObj = fontObj.render(hint, True, font_color, BLACK)
    # get_rect()方法返回rect对象
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (300, 570)
    screen.blit(textSurfaceObj, textRectObj)


def init_ans():
    global ans, raw_mat, choose_pos
    gene_soduko()
    raw_mat = copy.deepcopy(mat)
    ans = copy.deepcopy(mat)
    choose_pos = 0, 0
    # 开始时选取的位置在0,0


def choose_digit(press: str):
    """
    :param press: 按下去的字符
    :return:
    """
    r, c = choose_pos
    if raw_mat[r][c] != -1:
        return
    try:
        ip = int(press)
    except ValueError:
        ip = -1
    if 1 <= ip <= 4:
        ans[r][c] = ip
        if not check_row(ans, r):
            row_error[r] = ip
        else:
            row_error[r] = 0
        if not check_col(ans, r):
            col_error[r] = ip
        else:
            col_error[r] = 0
    elif ip == -1:
        ans[r][c] = ip


def proc_mouse(pos: Tuple):
    global choose_pos, time_index
    x, y = pos
    r, c = get_row_col(x, y)
    if r != -1:
        choose_pos = r, c
        time_index = 0


def move_chosen_grid(press: str):
    global choose_pos
    dr, dc = direction[press]
    r, c = choose_pos
    next_r, next_c = r + dr, c + dc
    if 0 <= next_r < N and 0 <= next_c < N:
        choose_pos = (next_r, next_c)


def proc_keyboard(press: str):
    # logger.info(press)
    if press.isdigit():
        # 在有问号的格子里面按数字
        choose_digit(press)
        if check_ans():
            global success, hint
            success = True
            hint = "恭喜布猫！"
    elif press in direction:
        # 上下左右移动格子
        move_chosen_grid(press)
    elif press == "backspace":
        choose_digit(press)


def draw_cat(screen):
    # if success:
    image = cat_images[time_index // 10 % 10]
    screen.blit(image, (X0, Y0))


def main():
    init_ans()
    pygame.init()
    global cat_images
    for i in range(1, 11):
        cat = pygame.image.load("./img/cat/gif_{0}.png".format(i))
        cat = pygame.transform.scale(cat, (300, 300))
        cat_images.append(cat)

    screen = pygame.display.set_mode((600, 640))
    pygame.display.set_caption("数独游戏")

    global choose_pos, mat, row_error, col_error, image_on

    # 控制时间循环
    clock = pygame.time.Clock()
    FPS = 60
    global time_index
    FIN = 45

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                # 处理关闭
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # 处理鼠标选中格子
                pos = pygame.mouse.get_pos()
                proc_mouse(pos)
            if event.type == KEYDOWN:
                # 处理键盘
                press = pygame.key.name(event.key)
                proc_keyboard(press)

        clock.tick(FPS)
        if choose_pos[0] != -1:
            time_index += 1
            if time_index == FIN:
                image_on = not image_on
                time_index = 0

        screen.fill((0, 0, 0))
        draw_grid(screen)
        draw_select_grid(screen)
        draw_mat(screen)
        draw_text(screen)
        draw_cat(screen)
        pygame.display.update()


if __name__ == "__main__":
    logger.add("./log/soduko.log", level="INFO", rotation="10 MB")
    main()
