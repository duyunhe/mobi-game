# -*- coding: utf-8 -*-
# @time     : 2024/6/12 15:10
# @author   : yhdu@tongwoo.cn
# @desc     :    
# @file     : draw.py
# @software : PyCharm

import pygame
from model.game import GameModel
from typing import Tuple

X0 = 100        # 左上角 (X0, Y0)
Y0 = 100
ALL_WIDTH = 400     # 棋盘总边长
BEGIN_OFFSET = 100
END_OFFSET = BEGIN_OFFSET + ALL_WIDTH


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


class DrawCtrl:
    def __init__(self, N):
        """
        将pygame的screen传入，负责绘制
        :param N
        """
        self.cat_images = []
        self.screen = None
        self.GRID_WIDTH = ALL_WIDTH // N
        self.choose_pos = (-1, -1)
        self.N = N

        self.hint = "喵>_^ 你好，杜楚予"

        for i in range(1, 11):
            cat = pygame.image.load("./img/cat/gif_{0}.png".format(i))
            cat = pygame.transform.scale(cat, (300, 300))
            self.cat_images.append(cat)

    def set_screen(self, screen):
        self.screen = screen

    def set_choose(self, choose_pos):
        self.choose_pos = choose_pos

    def get_choose(self):
        return self.choose_pos

    def get_row_col(self, x, y) -> Tuple:
        r = (y - Y0) // self.GRID_WIDTH
        c = (x - X0) // self.GRID_WIDTH
        if r < 0 or r >= self.N or c < 0 or c >= self.N:
            return -1, -1
        return r, c

    def draw_board(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        self.draw_select_grid()

    def draw_grid(self):
        line_color = (0, 255, 0)
        for y in range(BEGIN_OFFSET, END_OFFSET + 1, self.GRID_WIDTH):
            pygame.draw.line(self.screen, line_color, [BEGIN_OFFSET, y], [END_OFFSET, y])
        for x in range(BEGIN_OFFSET, END_OFFSET + 1, self.GRID_WIDTH):
            pygame.draw.line(self.screen, line_color, [x, BEGIN_OFFSET], [x, END_OFFSET])

    def draw_select_grid(self):
        line_color = (255, 255, 255)
        r, c = self.choose_pos
        if r == -1:
            return
        x0 = X0 + self.GRID_WIDTH * c
        y0 = Y0 + self.GRID_WIDTH * r
        x1, y1 = x0 + self.GRID_WIDTH, y0 + self.GRID_WIDTH
        OFFSET = 5
        x0, y0 = x0 + OFFSET, y0 + OFFSET
        x1, y1 = x1 - OFFSET, y1 - OFFSET
        pygame.draw.line(self.screen, line_color, [x0, y0], [x1, y0])
        pygame.draw.line(self.screen, line_color, [x0, y0], [x0, y1])
        pygame.draw.line(self.screen, line_color, [x1, y0], [x1, y1])
        pygame.draw.line(self.screen, line_color, [x0, y1], [x1, y1])

    def draw_cat(self, time_index):
        image = self.cat_images[time_index // 10 % 10]
        self.screen.blit(image, (X0, Y0))

    def draw_mat(self, gm: GameModel, image_on, choose_pos):
        sys_font = "C:\\Windows\\Fonts\\msyh.ttc"
        font = pygame.font.SysFont(sys_font, 75)
        font_color = (0, 255, 255)
        qm_color = (255, 255, 0)
        error_color = (220, 20, 60)
        black_color = (0, 0, 0)
        right_color = (0, 255, 127)
        ans, raw, row_error, col_error = gm.ans, gm.raw, gm.row_error, gm.col_error
        for i in range(self.N):
            for j in range(self.N):
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
                    if raw[i][j] == -1:
                        color = right_color
                if image_on and i == choose_pos[0] and j == choose_pos[1] and raw[i][j] == -1:
                    color = black_color
                text = font.render(s, True, color)
                x, y = get_pos(i, j, BEGIN_OFFSET, BEGIN_OFFSET, self.GRID_WIDTH)
                self.screen.blit(text, (x - 15, y - 20))

    def draw_text(self):
        sys_font = "C:\\Windows\\Fonts\\msyh.ttc"
        fontObj = pygame.font.Font(sys_font, 32)
        # render方法返回Surface对象
        font_color = (222, 49, 99)
        BLACK = (0, 0, 0)
        textSurfaceObj = fontObj.render(self.hint, True, font_color, BLACK)
        # get_rect()方法返回rect对象
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (300, 570)
        self.screen.blit(textSurfaceObj, textRectObj)

    def set_hint(self, hint):
        self.hint = hint


def main():
    pass


if __name__ == "__main__":
    main()
