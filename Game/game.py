import os
import sys
import subprocess
import time
import random
from PIL import Image, ImageDraw
from io import BytesIO


# ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆
VERSION = "0.0.1"
screenshot_way = 2

def check_screenshot():  # 检查获取截图的方式
    global screenshot_way
    if (screenshot_way < 0):
        print('暂不支持当前设备')
        sys.exit()
    binary_screenshot = pull_screenshot()
    try:
        Image.open(BytesIO(binary_screenshot)).load()  # 直接使用内存IO
        print('Capture Method: {}'.format(screenshot_way))
    except Exception:
        screenshot_way -= 1
        check_screenshot()


def pull_screenshot():  # 获取截图
    global screenshot_way
    if screenshot_way in [1, 2]:
        process = subprocess.Popen(
            'adb  shell screencap -p', shell=True, stdout=subprocess.PIPE)
        screenshot = process.stdout.read()
        if screenshot_way == 2:
            binary_screenshot = screenshot.replace(b'\r\n', b'\n')
        else:
            binary_screenshot = screenshot.replace(b'\r\r\n', b'\n')
        return binary_screenshot
    elif screenshot_way == 0:
        os.system('adb shell screencap -p /sdcard/autojump.png')
        os.system('adb pull /sdcard/autojump.png .')

def move(x1,y1,a_x,a_y):
    cmd = "adb shell input swipe {} {} {} {}".format(x1,y1,x1+a_x,y1+a_y)
    os.system(cmd)

def touch(x,y):
    cmd = "adb shell input tap {} {}".format(x,y)
    os.system(cmd)

# ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆


def main():
    check_screenshot()  # 检查截图

    binary_screenshot = pull_screenshot()
    im = Image.open(BytesIO(binary_screenshot))
    w,h = im.size
    move(w//2,h//2,-100,100)


    # 标注截图并显示
    # draw = ImageDraw.Draw(im)
    # draw.line([piece_x, 0, piece_x, h], fill='blue', width=1)  # start
    # draw.line([board_x, 0, board_x, h], fill='red', width=1)  # end
    # draw.ellipse([swipe_x1 - 16, swipe_y1 - 16,
    #               swipe_x1 + 16, swipe_y1 + 16], fill='red')  # click
    im.show()
    pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        os.system('adb kill-server')
        print('bye')
        exit(0)