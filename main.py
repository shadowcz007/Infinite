STYLE_PROMPT=',by Cyril Rolando,high detailed drawing,fairy cgsociety'

#截屏
from PIL import ImageGrab #安装Pillow包就可以
img = ImageGrab.grab(bbox=(620,380, 900,960)) #四个数字分别是要截屏的四个角
img.save('jieping.png') #保存图片

def shotscreen():
    img = ImageGrab.grab(bbox=(620,380, 900,960)) #四个数字分别是要截屏的四个角
    img.save('jieping.png') #保存图片

import hashlib
def md5(t):
    return hashlib.md5(t.encode(encoding='UTF-8')).hexdigest()

from diffusers import StableDiffusionPipeline
import torch
# ,safety_checker=None
torch.backends.cudnn.benchmark = True
sd_zh_pipe = StableDiffusionPipeline.from_pretrained("IDEA-CCNL/Taiyi-Stable-Diffusion-1B-Chinese-EN-v0.1", torch_dtype=torch.float16)
sd_zh_pipe.to('cuda')
# sd_zh_pipe = StableDiffusionPipeline.from_pretrained("IDEA-CCNL/Taiyi-Stable-Diffusion-1B-Chinese-EN-v0.1").to("cuda")
def create_image(text):
    global STYLE_PROMPT
    images=sd_zh_pipe(text+STYLE_PROMPT, guidance_scale=10.0,num_images_per_prompt=1).images
    name='result_'+text+'_'+str(int(time.time()))
    name=md5(name)+'.png'
    images[0].save('sd/'+name)
    return name

import easyocr
reader = easyocr.Reader(['ch_sim','en'],gpu=False) # this needs to run only once to load the model into memory
result = reader.readtext('jieping.png')

pre_text='1'
loading=False
def write_result():
    global pre_text
    global loading
    
    if(loading==True):
        return

    loading=True

    shotscreen()
    result = reader.readtext('jieping.png')
    res=[]
    #print(result)
    badwords=['OOUUC']
    for t in result:
        text=t[1].replace(';',':')
        #print(text)
        texts=text.split(':')
        if(len(texts)==1):
            if(len(res)>0):
                res[-1]+=texts[0]
            else:
                res.append(texts[0])
        if(len(texts)==2):
            res.append(texts[1])
    #print(2,len(res)>0, pre_text)
    if(len(res)>0 and res[-1].strip()!="" and res[-1]!=pre_text):
        #print(2)
        img_file_name=create_image(res[-1])
        with open('sd/text.txt','w',encoding='utf-8') as f:
            f.write(res[-1]+'[image]'+img_file_name)
            pre_text=res[-1]
            loading=False
    else:
        loading=False



import time
while True:
    try:
        write_result()
    except:
        loading=False
    time.sleep(1)