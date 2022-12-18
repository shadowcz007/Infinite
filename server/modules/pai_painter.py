from paddlenlp import Taskflow

text_to_image =None

def init():
    global text_to_image
    if text_to_image==None:
        text_to_image= Taskflow("text_to_image")

def start(t):
    init()
    image_list = text_to_image(t)
    return image_list[0]