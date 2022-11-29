import random
from PIL import ImageGrab
import hashlib
import time

STYLE_PROMPTS=[
    #',by Cyril Rolando,high detailed drawing,art station, concept art,illustration, 4k detailed post processing, fairy cgsociety,8k,highly detailed',
      '，在外太空，拿着足球，脚踢足球，足球，足球!!!!!!,人物，肖像画，高细节表现力，blender渲染的概念艺术图，超清，写实照片，超现实主义，梦幻唯美，高清的图像,8k detail，脸部刻画清晰，锐化',
    # ', lights, lens flares effects, swirly bokeh, brush effect, In style of Yoji Shinkawa, Jackson Pollock, wojtek fus, by Makoto Shinkai, concept art, celestial, amazing, astonishing, wonderful, beautiful, highly detailed, centered',
    # ', hyper realistic, 8k, epic composition, cinematic, octane render, artstation landscape vista photography by Carr Clifton & Galen Rowell, 16K resolution, Landscape veduta photo by Dustin Lefevre & tdraw, 8k resolution, detailed landscape painting by Ivan Shishkin, DeviantArt, Flickr, rendered in Enscape, Miyazaki, Nausicaa Ghibli, Breath of The Wild, 4k detailed post processing, artstation, rendering by octane, unreal engine',
    # ', art station, landscape, concept art, illustration, highly detailed artwork cinematic, hyper realistic painting'
    ]

SCREE_PATH='jieping.png'



import ppppocr
ocr = ppppocr.ppppOcr(model='server')

from diffusers import StableDiffusionPipeline
import torch

# ,safety_checker=None
torch.backends.cudnn.benchmark = True
sd_zh_pipe = StableDiffusionPipeline.from_pretrained("IDEA-CCNL/Taiyi-Stable-Diffusion-1B-Chinese-EN-v0.1", torch_dtype=torch.float16)
sd_zh_pipe.to('cuda')
# sd_zh_pipe = StableDiffusionPipeline.from_pretrained("IDEA-CCNL/Taiyi-Stable-Diffusion-1B-Chinese-EN-v0.1").to("cuda")



pre_text='1'
loading=False


def random_prompt_style():
    i=random.randint(0,len(STYLE_PROMPTS))
    return ''+STYLE_PROMPTS[i]

#截屏
 #安装Pillow包就可以
# img = ImageGrab.grab(bbox=(620,380, 900,960)) #四个数字分别是要截屏的四个角
# img.save('jieping.png') #保存图片

def shotscreen():
    img = ImageGrab.grab(bbox=(620,380, 900,960)) #四个数字分别是要截屏的四个角
    img.save(SCREE_PATH) #保存图片


def md5(t):
    return hashlib.md5(t.encode(encoding='UTF-8')).hexdigest()


def create_image(text):
    images=sd_zh_pipe(text+random_prompt_style(), guidance_scale=10.0,num_images_per_prompt=1).images
    name='result_'+text+'_'+str(int(time.time()))
    name=md5(name)+'.png'
    images[0].save('sd/'+name)
    return name

 
def readtext():
    image_path = SCREE_PATH
    dt_boxes, rec_res = ocr.ocr(image_path)
    return rec_res


def write_result():
    global pre_text
    global loading
    
    if(loading==True):
        return

    loading=True

    shotscreen()
    result = readtext()

    res=[]
    for t in result:
        text=t[0].replace(':','：')
        texts=text.split('：')
        
        if(len(texts)==1):
            # print(texts)
            if(len(res)>0):
                res[-1]+=texts[0]
            else:
                res.append(texts[0])
        if(len(texts)==2):
            # print(texts)
            res.append(texts[0]+'[talk]'+texts[1])

    texts=[]
    for r in res:
        if(len(r.split('[talk]'))==2):
            texts.append(r.split('[talk]')[1])
            #print(r.split('[talk]'))
    
    # print('==========',texts)
    if(len(texts)>0 and texts[-1].strip()!="" and texts[-1]!=pre_text):
        img_file_name=create_image(texts[-1])
        with open('sd/text.txt','w',encoding='utf-8') as f:
            f.write(texts[-1]+'[image]'+img_file_name)
            pre_text=texts[-1]
            loading=False
    else:
        loading=False


while True:
    try:
        write_result()
    except:
        loading=False
    loading=False
    time.sleep(1)
