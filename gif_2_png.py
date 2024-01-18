# -*- coding: utf-8 -*-
# @time     : 2024/1/18 17:31
# @author   : yhdu@tongwoo.cn
# @desc     :    
# @file     : gif_2_png.py
# @software : PyCharm

from PIL import Image, ImageSequence


def main():
    img = Image.open("./img/1.webp")
    idx = 1
    for frame in ImageSequence.all_frames(img):
        frame.save("./img/cat/gif_{0}.png".format(idx), quality=100)
        idx += 1


if __name__ == "__main__":
    main()
