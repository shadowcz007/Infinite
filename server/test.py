global screen_area
screen_area=[620,380, 900,960]
SCREE_PATH='jieping.png'

# 百度的ocr
import ppppocr
def init_ocr():
    global ocr
    ocr = ppppocr.ppppOcr(model='server')
init_ocr()

def shotscreen():
    global screen_area
    img = ImageGrab.grab(bbox=(screen_area[0],screen_area[1], screen_area[2],screen_area[3])) #四个数字分别是要截屏的四个角
    img.save(SCREE_PATH) #保存图片
    return img


def readtext():
    global ocr
    image_path = SCREE_PATH
    dt_boxes, rec_res = ocr.ocr(image_path)
    return rec_res

import time
while True:
    shotscreen()
    readtext()
    time.sleep(6)