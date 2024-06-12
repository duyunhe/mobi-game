# -*- coding: utf-8 -*-
# @time     : 2023/12/8 14:10
# @author   : yhdu@tongwoo.cn
# @desc     :    
# @file     : sudoku.py
# @software : PyCharm

import copy
import random
import sys
from typing import Tuple

import pygame
from loguru import logger
from pygame.locals import *
from ctl.draw import DrawCtrl
from model.game import GameModel

N = 5
model = GameModel(N)
draw_ctl = DrawCtrl(N)
end_hints = ['布猫真聪明！', '喵~布猫棒棒的！', '喵呜~布猫答对啦！', '妙~恭喜布猫！']
image_on = True
time_index = 0
FPS = 60
FIN = 45

direction = {
    "left": [0, -1],
    "right": [0, 1],
    "up": [-1, 0],
    "down": [1, 0]
}


def init_game():
    model.gene_sudoku()
    pygame.init()
    screen = pygame.display.set_mode((600, 640))
    pygame.display.set_caption("数独游戏 Sudoku")
    draw_ctl.set_screen(screen)


def choose_digit(press: str):
    """
    选择字符，并且检查是否有冲突
    :param press: 按下去的字符
    :return:
    """
    r, c = draw_ctl.get_choose()
    try:
        ip = int(press)
    except ValueError:
        ip = -1
    model.set_ans(r, c, ip)


def proc_mouse(pos: Tuple):
    global time_index
    x, y = pos
    r, c = draw_ctl.get_row_col(x, y)
    if r != -1:
        draw_ctl.set_choose((r, c))
        time_index = 0


def move_chosen_grid(press: str):
    dr, dc = direction[press]
    r, c = draw_ctl.get_choose()
    if r == -1:
        next_r, next_c = 0, 0
    else:
        next_r, next_c = r + dr, c + dc
    if 0 <= next_r < N and 0 <= next_c < N:
        draw_ctl.set_choose((next_r, next_c))


def proc_keyboard(press: str):
    # logger.info(press)
    if press.isdigit():
        # 在有问号的格子里面按数字
        choose_digit(press)
        # 完成数独
        if model.get_success():
            hint = random.choice(end_hints)
            draw_ctl.set_hint(hint)
    elif press in direction:
        # 上下左右移动格子
        move_chosen_grid(press)
    elif press == "backspace":
        choose_digit(press)


def main():
    global image_on, time_index
    # time_index 用于控制问号闪烁
    clock = pygame.time.Clock()

    init_game()
    # 控制时间循环
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

        choose_pos = draw_ctl.get_choose()
        if choose_pos[0] != -1:
            time_index += 1
            if time_index == FIN:
                image_on = not image_on
                time_index = 0

        draw_ctl.draw_board()
        draw_ctl.draw_mat(model, image_on, choose_pos)
        draw_ctl.draw_text()
        if model.get_success():
            draw_ctl.draw_cat(time_index)

        pygame.display.update()


if __name__ == "__main__":
    logger.add("./log/soduko.log", level="INFO", rotation="10 MB")
    main()
