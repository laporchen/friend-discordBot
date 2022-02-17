from datetime import datetime, date
from inspect import getfile
from PIL import Image, ImageFont, ImageDraw


def getDiff():
    currentTime = date.today()
    xmasTime = date(currentTime.year, 12, 25)
    if(currentTime > xmasTime):
        xmasTime = date(currentTime.year+1, 12, 25)
    daysDiff = (xmasTime - currentTime).days
    print()
    return daysDiff


def drawOnImg(daysDiff):
    text = f'Time until next xmas is {daysDiff} days'
    img = Image.open("./img/padoru.jpg")
    drawing = ImageDraw.Draw(img)
    font = ImageFont.truetype(
        font="./font/serif.ttf", size=40)
    drawing.text((100, 600), text, (255, 255, 255), font=font)
    img.save('./img/xmas.jpg')
    return "xmas.jpg"


def padoru():
    return drawOnImg(getDiff())
