from PIL import Image, ImageFilter, ImageQt, ImageDraw, ImageFont
import random
from captcha.image import ImageCaptcha
import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


def rndChar():
    return chr(random.randint(65, 90))


def rndColor():
    return tuple([random.randint(32, 127) for _ in range(3)])


def rndBg():
    return tuple([random.randint(64, 255) for _ in range(3)])


def rndLine():
    return tuple([random.randint(32, 72) for _ in range(3)])


def code1():
    blurFlag = True
    enhanceFlag = True
    lineFlag = True
    linecolor = rndLine()
    linenumber = random.randint(5, 10)

    def genLine(draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=linecolor)

    width = 60 * 4
    height = 60

    img = Image.new("RGB", (width, height), (155, 255, 255))
    font = ImageFont.truetype("images_code/FZDHTJW.TTF", 36)
    draw = ImageDraw.Draw(img)

    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndBg())

    for t in range(4):
        draw.text((60 * t + 15, 10), rndChar(), font=font, fill=rndColor())

    if lineFlag:
        for t in range(linenumber):
            genLine(draw, width, height)

    if blurFlag:
        img = img.filter(ImageFilter.BLUR)

    if enhanceFlag:
        img = img.filter(ImageFilter.EDGE_ENHANCE)

    img.show()


def code2():
    im = ImageCaptcha()
    rnd = ''
    for t in range(4):
        rnd = rnd + rndChar()

    im.write(rnd, "code.png")
    ans = ''
    while ans.lower != rnd.lower:
        ans = input("请输入验证码：")
        if ans.lower() == rnd.lower():
            print("验证成功")
            break
        else:
            print("验证失败")


code2()
