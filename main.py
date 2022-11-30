import random
from PIL import ImageGrab
import hashlib
import time
import json

STYLE_PROMPTS=[
    #',by Cyril Rolando,high detailed drawing,art station, concept art,illustration, 4k detailed post processing, fairy cgsociety,8k,highly detailed',
    '，在外太空，拿着足球，脚踢足球，足球，足球!!!!!!,人物，肖像画，高细节表现力，blender渲染的概念艺术图，超清，写实照片，超现实主义，梦幻唯美，高清的图像,8k detail，脸部刻画清晰，锐化',
    '，长城上，看足球比赛，脚踢足球，足球，足球!!!!!!,人物，肖像画，高细节表现力，blender渲染的概念艺术图，超清，超现实主义，高清的图像,8k detail，脸部刻画清晰，锐化,写实摄影作品',
    # ', hyper realistic, 8k, epic composition, cinematic, octane render, artstation landscape vista photography by Carr Clifton & Galen Rowell, 16K resolution, Landscape veduta photo by Dustin Lefevre & tdraw, 8k resolution, detailed landscape painting by Ivan Shishkin, DeviantArt, Flickr, rendered in Enscape, Miyazaki, Nausicaa Ghibli, Breath of The Wild, 4k detailed post processing, artstation, rendering by octane, unreal engine',
    # ', art station, landscape, concept art, illustration, highly detailed artwork cinematic, hyper realistic painting'
    ]

SCREE_PATH='jieping.png'

JSON_PATH='sd/images.json'

USER_COUNT_PATH='sd/user.json'

# 百度的ocr
import ppppocr
ocr = ppppocr.ppppOcr(model='server')

# huggingface的sd库
from diffusers import StableDiffusionPipeline
import torch

# 是否过滤黄暴图 ,safety_checker=None
torch.backends.cudnn.benchmark = True
sd_zh_pipe = StableDiffusionPipeline.from_pretrained("IDEA-CCNL/Taiyi-Stable-Diffusion-1B-Chinese-EN-v0.1", torch_dtype=torch.float16)
sd_zh_pipe.to('cuda')
# sd_zh_pipe = StableDiffusionPipeline.from_pretrained("IDEA-CCNL/Taiyi-Stable-Diffusion-1B-Chinese-EN-v0.1").to("cuda")


#上一次用户输入
pre_text='1'

#记录上一次用户投票
pre_count=0


# 本地缓存的图片集合
result_images=load_json()


def init_keywords(keywords):
    keywords=keywords.split("\n")
    keywords_new=[]
    for i in range(len(keywords)):
        t=keywords[i].strip()
        if len(t)>0:
            keywords_new.append(t)
    return keywords_new

# 内置的物体名词
keywords=''' 
蜘蛛侠
钢铁侠
超人
银河护卫队
'''

keywords=init_keywords(keywords)
# print(keywords)


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

def load_json():
    f = open(JSON_PATH, 'r')
    content = f.read()
    a = json.loads(content)
    f.close()
    return a

def save_json(a):
    return write_json(a,JSON_PATH)

def write_json(a,file_path):
    b = json.dumps(a)
    f2 = open(file_path, 'w')
    f2.write(b)
    f2.close()
    return


def get_user_input():
    #截屏
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
    return texts 


def write_user_feedback(texts):
    global pre_count
    global pre_text
    count=0
    for t in texts:
        if t=='1':
            print('#####用户反馈---1')
            count+=1
    if count>pre_count:
        write_json({
            "count":count,
            "input":pre_text
        },USER_COUNT_PATH)
        pre_count=count
    else:
        write_json({
            "count":0,
            "input":pre_text
        },USER_COUNT_PATH)

        


def write_result():
    global pre_text
    #用户输入
    texts=get_user_input()

    #记录用户的投票
    write_user_feedback(texts)
    
    # 避免 1 作为prompt
    # print('==========',texts)
    if(len(texts)>0 and texts[-1].strip()!="" and texts[-1].strip()!="1" and texts[-1]!=pre_text):
        input_text=texts[-1].strip()
        tid=md5(input_text)
        result_images={
            "id":tid,
            "input":input_text,
            "images":[]
        }

        # 第一张图
        img_file_name=create_image(input_text)
        result_images['images'].append(img_file_name)
        save_json(result_images)
        pre_text=input_text

        # 第2张图
        img_file_name=create_image(input_text)
        result_images['images'].append(img_file_name)
        save_json(result_images)

        # 第3张图
        img_file_name=create_image(input_text)
        result_images['images'].append(img_file_name)
        save_json(result_images)

        # 第4张图
        img_file_name=create_image(input_text)
        result_images['images'].append(img_file_name)
        save_json(result_images)




while True:
    try:
        write_result()
    except:
        print('error')
    time.sleep(2)
