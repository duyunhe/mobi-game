# -*- coding: utf-8 -*-
# @time     : 2024/6/11 8:31
# @author   : yhdu@tongwoo.cn
# @desc     :    
# @file     : gene_mat.py
# @software : PyCharm

from perm_random import rand_per, next_permutation


class MatGene:
    def __init__(self, n):
        self.dfs_fin = 0

        self.N = n
        self.mat = [[-1] * n for _ in range(n)]
        self.vis = [[0] * (n + 1) for _ in range(n)]

    def check_col(self, check_mat, cur_row: int, cur_col: int):
        val = check_mat[cur_row][cur_col]
        if self.vis[cur_col][val] > 1:
            return False
        return True

    def dfs(self, r):
        if r == self.N:
            self.dfs_fin = 1
            return
        if self.dfs_fin:
            return
        t = rand_per(self.N)
        while True:
            ok = 1
            bi = 0
            for i in range(self.N):
                val = t[i]
                self.mat[r][i] = val
                self.vis[i][val] += 1

                if not self.check_col(self.mat, r, i):
                    ok = 0
                    bi = i + 1
                    break
            else:
                bi = self.N

            if ok:
                self.dfs(r + 1)
            if self.dfs_fin:
                return

            for i in range(bi):
                val = t[i]
                self.mat[r][i] = -1
                self.vis[i][val] -= 1

            t = next_permutation(t)

    def gene(self):
        self.dfs(0)
        return self.mat


def test():
    mg = MatGene(6)
    print(mg.gene())


if __name__ == "__main__":
    test()
