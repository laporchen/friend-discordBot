from datetime import datetime, date, timedelta, timezone, tzinfo
from PIL import Image, ImageFont, ImageDraw
timeDiff = 8
tz = timezone(timedelta(hours=timeDiff))


def getDiff():
    currentTime = datetime.now(tz)
    xmasTime = datetime(currentTime.year, 12, 25, 0, 0, 0, tzinfo=tz)
    if(currentTime > xmasTime):
        xmasTime = datetime(currentTime.year+1, 12, 25, 0, 0, 0, tzinfo=tz)
    diff = (xmasTime - currentTime)
    print(diff)
    return diff


def drawOnImg(daysDiff):
    text = f'Next xmas : {daysDiff.days} days, {daysDiff.seconds//3600} hours, {(daysDiff.seconds//60)%60} minutes {daysDiff.seconds%60} seconds'
    img = Image.open("./img/padoru.jpg")
    drawing = ImageDraw.Draw(img)
    font = ImageFont.truetype(
        font="./font/serif.ttf", size=40)
    drawing.text((100, 600), text, (255, 255, 255), font=font)
    img.save('./img/xmas.jpg')
    return "xmas.jpg"


def padoru():
    return drawOnImg(getDiff())
