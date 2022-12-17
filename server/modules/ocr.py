from PIL import ImageGrab,Image
import argparse,time
SCREEN_PATH='./data/jieping.png'
ocr=None
#截屏位置
screen_area=[620,380, 900,960]

def shotscreen():
    global screen_area
    img = ImageGrab.grab(bbox=(screen_area[0],screen_area[1], screen_area[2],screen_area[3])) #四个数字分别是要截屏的四个角
    img.save(SCREEN_PATH) #保存图片
    # print(screen_area,SCREEN_PATH)
    return img


#手动配置截屏区域
def shotscreen_setup(x,y,w,h):
    global screen_area
    screen_area= [x,y,w,h]
    img=shotscreen()
    return img

# 百度的ocr
def init_ocr():
    import ppppocr
    global ocr
    ocr = ppppocr.ppppOcr(model='server')
    return ocr

def readtext():
    global ocr
    if ocr==None:
        init_ocr()
    image_path = SCREEN_PATH
    dt_boxes, rec_res = ocr.ocr(image_path)
    print(rec_res)
    rec_res=[[r[0],r[1]] for r in rec_res]
    return rec_res

def start():
    im=shotscreen()
    # time.sleep(0.5)
    result = readtext()
    return im,result


def parse_args():
    description = "百度的ocr..."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-f", "--image_path", type=str, default='', help="传入地址")

    return parser.parse_args()


if __name__ == "__main__":
    
    args = parse_args()
    res=start()
    print(res)