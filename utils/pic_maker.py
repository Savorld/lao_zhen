# -*- coding:utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import os
from datas import city


# n = 0
for k, v in city.items():
    # if n == 1:
    #     break
    for i in range(8):
        img = Image.open('../static/img/living_pic/m.jpg')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('../static/img/living_pic/simkai.ttf', 30)
        txt = v.decode('utf-8') + u'-中图' + unicode(i)
        draw.text((10, 80), txt, (0, 255, 0), font=font)
        # img.show()
        path = '../static/img/living_pic/m/' + k + '-' + str(i) + '.jpg'
        img.save(path)
    # n += 1


