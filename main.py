import gradio as gr


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

global ocr
global sd_zh_pipe
global pipe_text2img
global pipe_img2img

# 百度的ocr
# import ppppocr
def init_ocr():
    global ocr
    ocr = ppppocr.ppppOcr(model='server')


# huggingface的sd库
from diffusers import StableDiffusionPipeline
import torch

device="cuda"
model_id = "IDEA-CCNL/Taiyi-Stable-Diffusion-1B-Chinese-EN-v0.1"

def init_sd():
    global pipe_text2img
    global pipe_img2img
    
    # 是否过滤黄暴图 ,safety_checker=None
    # torch.backends.cudnn.benchmark = True
    # global sd_zh_pipe
    # sd_zh_pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to(device)
    # sd_zh_pipe = StableDiffusionPipeline.from_pretrained("IDEA-CCNL/Taiyi-Stable-Diffusion-1B-Chinese-EN-v0.1").to("cuda")
    pipe_text2img = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to(device)
    pipe_img2img = StableDiffusionImg2ImgPipeline(**pipe_text2img.components).to(device)


#上一次用户输入
pre_text='1'

#记录上一次用户投票
pre_count=0


def load_json():
    f = open(JSON_PATH, 'r')
    content = f.read()
    a = json.loads(content)
    f.close()
    return a


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

global screen_area
screen_area=[620,380, 900,960]

def shotscreen():
    global screen_area
    img = ImageGrab.grab(bbox=(screen_area[0],screen_area[1], screen_area[2],screen_area[3])) #四个数字分别是要截屏的四个角
    img.save(SCREE_PATH) #保存图片
    return img

def shotscreen_setup(t):
    global screen_area
    screen_area= [int(i) for i in t.split(",")]
    img=shotscreen()
    return img



def md5(t):
    return hashlib.md5(t.encode(encoding='UTF-8')).hexdigest()


def create_image(text):
    global sd_zh_pipe
    images=sd_zh_pipe(text+random_prompt_style(), guidance_scale=10.0,num_images_per_prompt=1).images
    name='result_'+text+'_'+str(int(time.time()))
    name=md5(name)+'.png'
    images[0].save('sd/'+name)
    return name,images[0]


def readtext():
    global ocr
    image_path = SCREE_PATH
    dt_boxes, rec_res = ocr.ocr(image_path)
    return rec_res


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
    im=shotscreen()
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
    return texts,im 


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
    texts,im=get_user_input()

    #记录用户的投票
    #write_user_feedback(texts)
    
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
        img_file_name,im=create_image(input_text)
        result_images['images'].append(img_file_name)
        save_json(result_images)
        pre_text=input_text

        return im,result_images

def create_more():
    global pre_text
    tid=md5(pre_text)
    result_images={
            "id":tid,
            "input":pre_text,
            "images":[]
        }
    # 第n张图
    img_file_name,im=create_image(pre_text)
    result_images['images'].append(img_file_name)
    save_json(result_images)
    return im,result_images

def count_user_feedback(keyword):
    texts,im =get_user_input()
    print('count_user_feedback::',keyword,texts)
    return texts


def infer_text2img(prompt, guide, steps, width, height, image_in, strength):
    if image_in is not None:
        init_image = image_in.convert("RGB").resize((width, height))
        output = pipe_img2img(prompt, init_image=init_image, strength=strength, width=width, height=height, guidance_scale=guide, num_inference_steps=steps)
    else:
        output = pipe_text2img(prompt, width=width, height=height, guidance_scale=guide, num_inference_steps=steps,)
    image = output.images[0]
    return image

def infer_inpaint(prompt, guide, steps, width, height, image_in): 
    init_image = image_in["image"].convert("RGB").resize((width, height))
    mask = image_in["mask"].convert("RGB").resize((width, height))

    output = pipe_inpaint(prompt, \
                        init_image=init_image, mask_image=mask, \
                        width=width, height=height, \
                        guidance_scale=7.5, num_inference_steps=20)
    image = output.images[0]
    return image

# while True:
#     try:
#         write_result()
#     except:
#         print('error')
#     time.sleep(2)



with gr.Blocks(css="main.css") as demo:
    examples = [[x] for x in STYLE_PROMPTS]
    # 截图
    with gr.Row(scale=1,):
        with gr.Column(scale=1, ):
            screen_area = gr.Textbox(label = '截图区域',value="620,380, 900,960")
            shotscreen_btn=gr.Button("截图")
            shotscreen_and_ocr_btn=gr.Button("截图&OCR")
            get_user_input_and_createImage_btn=gr.Button("根据用户输入生成")
            create_more_btn=gr.Button("根据用户输入生成更多")
            keyword = gr.Textbox(label = 'prompt-用户输入')
            shotscreen_and_ocr_and_match_keyword_btn=gr.Button("计算投票")
        with gr.Column(scale=1, ):
            screen_image=gr.Image(label = '结果',elem_id="screen_image")
            json_res=gr.JSON(label='结果')
    with gr.Row():
        
        with gr.Column(scale=1, ):
            image_out = gr.Image(label = '输出(output)')
        with gr.Column(scale=1, ):
            image_in = gr.Image(source='upload', elem_id="image_upload", type="pil", label="参考图（非必须）(ref)")
            prompt = gr.Textbox(label = '提示词(prompt)')
            submit_btn = gr.Button("生成图像(Generate)")
            with gr.Row(scale=0.5 ):
                guide = gr.Slider(2, 15, value = 7, label = '文本引导强度(guidance scale)')
                steps = gr.Slider(10, 60, value = 30, step = 1, label = '迭代次数(inference steps)')
                width = gr.Slider(384, 768, value = 512, step = 64, label = '宽度(width)')
                height = gr.Slider(384, 768, value = 512, step = 64, label = '高度(height)')
                strength = gr.Slider(0, 1.0, value = 0.8, step = 0.05, label = '参考图改变程度(strength)')
                ex = gr.Examples(examples, fn=infer_text2img, inputs=[prompt, guide, steps, width, height], outputs=image_out)

        # with gr.Column(scale=1, ):
        #     image_in = gr.Image(source='upload', tool='sketch', elem_id="image_upload", type="pil", label="Upload")
        #     inpaint_prompt = gr.Textbox(label = '提示词(prompt)')
        #     inpaint_btn = gr.Button("图像编辑(Inpaint)")
            # img2img_prompt = gr.Textbox(label = '提示词(prompt)')
            # img2img_btn = gr.Button("图像编辑(Inpaint)")
        submit_btn.click(fn = infer_text2img, inputs = [prompt, guide, steps, width, height, image_in, strength], outputs = image_out)
        shotscreen_btn.click(fn=shotscreen_setup,inputs =[screen_area],
        outputs=screen_image,
        api_name="shotscreen")
        shotscreen_and_ocr_btn.click(fn=get_user_input,
        outputs=[json_res,screen_image],
        api_name="shotscreen")
        get_user_input_and_createImage_btn.click(fn=write_result,
        outputs=[screen_image,json_res],
        api_name="get_user_input_and_createImage")
        create_more_btn.click(fn=create_more,
        outputs=[screen_image,json_res],
        api_name="create_more")

        shotscreen_and_ocr_and_match_keyword_btn.click(fn=count_user_feedback,
        inputs =[keyword],
        outputs=json_res,
        api_name="count_user_feedback")
        # inpaint_btn.click(fn = infer_inpaint, inputs = [inpaint_prompt, width, height, image_in], outputs = image_out)
        # img2img_btn.click(fn = infer_img2img, inputs = [img2img_prompt, width, height, image_in], outputs = image_out)
demo.queue(concurrency_count=1, max_size=8).launch(share=True)