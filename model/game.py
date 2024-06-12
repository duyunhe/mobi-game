# -*- coding: utf-8 -*-
# @time     : 2024/6/12 15:52
# @author   : yhdu@tongwoo.cn
# @desc     :    
# @file     : game.py
# @software : PyCharm

from gene_mat import MatGene
import random
from copy import deepcopy


class GameModel:
    def __init__(self, N):
        self.ans = None       # 当前的矩阵，用-1代表需要填的数字，在棋盘上用问号显示
        self.raw = None             # 原始矩阵
        self.N = N
        self.row_error = [0] * N
        self.col_error = [0] * N
        self.success = False

    def gene_sudoku(self):
        mg = MatGene(self.N)
        mat = mg.gene()
        for i in range(self.N):
            ri = random.randint(0, self.N - 1)
            mat[i][ri] = -1
            # 再放N个?
        ticket = self.N - 1
        while ticket:
            ri = random.randint(0, self.N * self.N - 1)
            r, c = ri // self.N, ri % self.N
            if mat[r][c] != -1:
                ticket -= 1
                mat[r][c] = -1

        self.raw = deepcopy(mat)
        self.ans = mat

    def set_ans(self, r, c, val):
        if self.raw[r][c] != -1:
            return
        if 1 <= val <= self.N or val == -1:
            self.ans[r][c] = val

            if not self.check_row(r):
                self.row_error[r] = val
            else:
                self.row_error[r] = 0
            if not self.check_col(c):
                self.col_error[c] = val
            else:
                self.col_error[c] = 0
            # 检查是否完成
            self.success = self.check_ans()

    def check_row(self, r: int):
        vis = [0] * (self.N + 1)
        for i in range(self.N):
            val = self.ans[r][i]
            if val == -1:
                continue
            if vis[val]:
                return False
            vis[val] = 1
        return True

    def check_col(self, c: int):
        vis = [0] * (self.N + 1)
        for i in range(self.N):
            val = self.ans[i][c]
            if val == -1:
                continue
            if vis[val]:
                return False
            vis[val] = 1
        return True

    def check_ans(self) -> bool:
        """
        检查是否完成数独
        :return: True 完成  False 未完成
        """
        for i in range(self.N):
            for j in range(self.N):
                if self.ans[i][j] == -1:
                    return False
        for i in range(self.N):
            if not self.check_row(i):
                return False
        for i in range(self.N):
            if not self.check_col(i):
                return False
        return True

    def get_success(self):
        return self.success


def main():
    pass


if __name__ == "__main__":
    main()
