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
from typing import Tuple

ans = []
mat = [[1, 2, 3, 4], [4, 3, -1, 1], [3, 1, -1, -1], [-1, -1, -1, -1]]
choose_pos = (0, 0)
image_on = True


def get_pos(r: int, c: int, x0: int, y0: int, width: int) -> Tuple:
    """
    获取方格中心坐标 x, y
    :param r: 从上往下第r行 1...r
    :param c: 从左往右第c列 1...c
    :param x0: 左上角x坐标
    :param y0: 左上角y坐标
    :param width: 方格边长
    :return:
    """
    return (c - 1) * width + width // 2 + x0, (r - 1) * width + width // 2 + y0


def get_row_col(x, y, x0, y0, width) -> Tuple:
    r = (y - y0) // width + 1
    c = (x - x0) // width + 1
    if r < 1 or r > 4 or c < 1 or c > 4:
        return -1, -1
    return r, c


def draw_grid(screen):
    line_color = (0, 255, 0)
    for y in range(100, 501, 100):
        pygame.draw.line(screen, line_color, [100, y], [500, y])
    for x in range(100, 501, 100):
        pygame.draw.line(screen, line_color, [x, 100], [x, 500])


def draw_mat(screen):
    global ans
    font = pygame.font.SysFont("arial.ttf", 75)
    font_color = (0, 255, 255)
    qm_color = (255, 255, 0)
    black_color = (0, 0, 0)
    for i in range(1, 5):
        for j in range(1, 5):
            a = ans[i - 1][j - 1]
            if a == -1:
                s = '?'
                color = qm_color
            else:
                s = str(a)
                color = font_color
            global image_on
            if image_on and i == choose_pos[0] and j == choose_pos[1]:
                color = black_color
            text = font.render(s, True, color)
            x, y = get_pos(i, j, 100, 100, 100)
            screen.blit(text, (x - 15, y - 20))


def init_ans():
    global ans
    ans = copy.deepcopy(mat)


def main():
    init_ans()
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption("数独游戏")

    global choose_pos, mat
    clock = pygame.time.Clock()
    FPS = 60
    i = 0
    FIN = 30
    global image_on
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos
                r, c = get_row_col(x, y, 100, 100, 100)
                if r != -1:
                    if mat[r - 1][c - 1] == -1:
                        choose_pos = r, c
                        i = 0
                        print(choose_pos)
                    else:
                        choose_pos = 0, 0
            if event.type == KEYDOWN:
                pass

        clock.tick(FPS)
        if choose_pos[0] != 0:
            i += 1
            if i == FIN:
                image_on = not image_on
                i = 0
        screen.fill((0, 0, 0))
        draw_grid(screen)
        draw_mat(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
