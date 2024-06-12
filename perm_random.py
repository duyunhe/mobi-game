# -*- coding: utf-8 -*-
# @time     : 2024/6/11 9:33
# @author   : yhdu@tongwoo.cn
# @desc     : 随机排列
# @file     : perm_random.py
# @software : PyCharm

import random
from typing import List


def next_permutation(per_list: List[int]):
    n = len(per_list)
    for i in range(n - 2, -1, -1):
        if per_list[i] < per_list[i + 1]:
            bi = i
            break
    else:
        return [i + 1 for i in range(n)]
    for i in range(n - 1, bi, -1):
        if per_list[i] > per_list[bi]:
            per_list[i], per_list[bi] = per_list[bi], per_list[i]
            break
    i, j = bi + 1, n - 1
    while i < j:
        per_list[i], per_list[j] = per_list[j], per_list[i]
        i, j = i + 1, j - 1
    return per_list


def rand_per(n):
    p = [i + 1 for i in range(n)]
    s = set(p)
    ans = []
    for i in range(n):
        l = list(s)
        j = random.randint(0, n - 1 - i)
        val = l[j]
        ans.append(val)
        s.remove(val)
    return ans


def main():
    for i in range(10):
        p = rand_per(9)
        print(p)


if __name__ == "__main__":
    main()
