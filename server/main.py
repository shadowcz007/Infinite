import random
import hashlib
import time
import json,os,io,base64

from PIL import ImageGrab,Image
import gradio as gr


DEVICE="cuda"
# MODEL_ID = "IDEA-CCNL/Taiyi-Stable-Diffusion-1B-Chinese-EN-v0.1"
MODEL_ID="IDEA-CCNL/Taiyi-Stable-Diffusion-1B-Chinese-v0.1"

# 内置的物体名词
KEYWORDS=[k.strip() for k in 
''' 
蜘蛛侠
钢铁侠
超人
银河护卫队
'''.split("\n") if len(k.strip())>0]

# 内置风格模版
STYLE_PROMPTS=[k.strip() for k in 
''' 
，在外太空，拿着足球，脚踢足球，足球，足球!!!!!!,人物，肖像画，高细节表现力，blender渲染的概念艺术图，超清，写实照片，超现实主义，梦幻唯美，高清的图像,8k detail，脸部刻画清晰，锐化
，长城上，看足球比赛，脚踢足球，足球，足球!!!!!!,人物，肖像画，高细节表现力，blender渲染的概念艺术图，超清，超现实主义，高清的图像,8k detail，脸部刻画清晰，锐化,写实摄影作品

'''.split("\n") if len(k.strip())>0]


SCREE_PATH='jieping.png'
JSON_PATH='sd/images.json'
 

ocr=None
pipe_text2img=None
pipe_img2img=None

# httpserver
http_server=None

#上一次用户输入
pre_text='1'

#记录上一次用户投票
pre_count=0

#截屏位置
screen_area=[620,380, 900,960]



# 百度的ocr
def init_ocr():
    import ppppocr
    global ocr
    ocr = ppppocr.ppppOcr(model='server')

def init_sd():
    # huggingface的sd库
    from diffusers import StableDiffusionPipeline,StableDiffusionImg2ImgPipeline
    import torch

    global pipe_text2img
    global pipe_img2img
    
    # 是否过滤黄暴图 ,safety_checker=None
    # torch.backends.cudnn.benchmark = True
    # global sd_zh_pipe
    # sd_zh_pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to(device)
    # sd_zh_pipe = StableDiffusionPipeline.from_pretrained("IDEA-CCNL/Taiyi-Stable-Diffusion-1B-Chinese-EN-v0.1").to("cuda")
    pipe_text2img = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16,safety_checker=None).to(DEVICE)
    pipe_img2img = StableDiffusionImg2ImgPipeline(**pipe_text2img.components).to(DEVICE)

 
def random_prompt_style():
    i=random.randint(0,len(STYLE_PROMPTS)-1)
    return ''+STYLE_PROMPTS[i]

def random_keyword():
    i=random.randint(0,len(KEYWORDS)-1)
    return KEYWORDS[i]

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

def image_to_base64(image):
    base64_str=None
    if image:
        # 输入为PIL读取的图片，输出为base64格式
        byte_data = io.BytesIO()# 创建一个字节流管道
        image.save(byte_data, format="JPEG")# 将图片数据存入字节流管道
        byte_data = byte_data.getvalue()# 从字节流管道中获取二进制
        base64_str = base64.b64encode(byte_data).decode("ascii")# 二进制转base64
    return base64_str

def base64_to_image(base64_str):
    image=None
    if base64_str:
        # 输入为base64格式字符串，输出为PIL格式图片
        byte_data = base64.b64decode(base64_str) # base64转二进制
        image = Image.open(io.BytesIO(byte_data)) # 将二进制转为PIL格式图片
    return image
    


def create_http_server(style_prompt,guide, steps, width, height, image_in, strength):
    global http_server
    if http_server==None:
        http_server=os.popen('python3 -m http.server')
        os.popen('start http://localhost:8000/magic-card.html')
    return update_pipe_opts(style_prompt,guide, steps, width, height, image_in, strength)

def stop_http_server():
    global http_server
    if http_server:
        http_server.close()

def shotscreen():
    global screen_area
    img = ImageGrab.grab(bbox=(screen_area[0],screen_area[1], screen_area[2],screen_area[3])) #四个数字分别是要截屏的四个角
    img.save(SCREE_PATH) #保存图片
    return img

#手动配置截屏区域
def shotscreen_setup(x,y,w,h):
    global screen_area
    screen_area= [x,y,w,h]
    img=shotscreen()
    return img

#hash值
def md5(t):
    return hashlib.md5(t.encode(encoding='UTF-8')).hexdigest()


def readtext():
    global ocr
    if ocr==None:
        init_ocr()
    image_path = SCREE_PATH
    dt_boxes, rec_res = ocr.ocr(image_path)
    return rec_res

#获取用户输入
def get_user_input():
    #截屏
    im=shotscreen()
    result = readtext()

    res=[]
    if result!=None:
        for t in result:
            if t!=None:
                text=t[0]
                if text!='主播':
                    text=text.replace(':','：')
                    texts=text.split('：')
                    if len(texts)==1:
                        if(len(res)>0 and isinstance(res[-1],str)):
                            res[-1]+=','+texts[0]
                    elif len(texts)==2:
                        if texts[1]=='':
                            res.append(1)
                        else:
                            num=texts[1]
                            try:
                                num=int(num)
                            except:
                                num=None
                            if num!=None:
                                res.append(num)
                            else:
                                res.append(texts[1])       
    return res,im 




#根据用户输入，新主题 
def get_user_input_and_prompt():
    global pre_text
    #用户输入
    texts,im=get_user_input()

    # 避免 1 作为prompt
    res=[]
    for t in texts:
        try:
            t=int(t)
        except:
            t=t.strip()
        if isinstance(t,str):
            res.append(t)
    print('==========',res)
    if(len(res)>0 and isinstance(res[-1],str) and res[-1].strip()!="" and res[-1].strip()!="1" and res[-1]!=pre_text):
        pre_text=res[-1].strip()
      
    return pre_text,im
   


# 获取用户投票
def count_user_feedback(keyword):
    texts,im =get_user_input()
    # print('count_user_feedback::',keyword,texts)
    is_count=False
    count=0
    for t in texts:
        if is_count and isinstance(t, int):
            count+=t
        if keyword==t:
            is_count=True
    return count

def infer_text2img_for_auto(prompt):
    global pipe_opts
    im=infer_text2img(prompt,
    pipe_opts["style_prompt"],
    pipe_opts["guide"],
    pipe_opts["steps"],
    pipe_opts["width"],
    pipe_opts["height"],
    base64_to_image(pipe_opts["image_in"]),
    pipe_opts["strength"]
    )
    return im

def update_pipe_opts(style_prompt,guide, steps, width, height, image_in, strength):
    global pipe_opts
    # print(image_in)
    pipe_opts={
        "style_prompt":style_prompt,
        "guide":guide,
        "steps":steps,
        "width":width,
        "height":height,
        "image_in":image_to_base64(image_in),
        "strength":strength
    }
    return pipe_opts

def infer_text2img(prompt, style_prompt,guide, steps, width, height, image_in, strength):
    global pipe_text2img
    global pipe_img2img

    if style_prompt!=None:
        prompt=prompt+','+style_prompt
    if pipe_text2img==None:
        init_sd()
    if image_in is not None:
        init_image = image_in.convert("RGB").resize((width, height))
        output = pipe_img2img(prompt, 
                                        init_image=init_image, 
                                        strength=strength, 
                                        width=width, 
                                        height=height, 
                                        guidance_scale=guide, 
                                        num_inference_steps=steps)
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


# init_ocr()
# init_sd()


with gr.Blocks(css="main.css") as demo:
    examples = [[random_keyword(),x] for x in STYLE_PROMPTS]
    # 截图
    with gr.Row(scale=1,):
        with gr.Column(scale=1, ):
            with gr.Row(scale=0.5 ):
                
                # screen_area = gr.Textbox(label = '截图区域',value="620,380, 900,960")
                screen_x=gr.Slider(0, 1500, value = 620, label = 'x')
                screen_y=gr.Slider(0, 1500, value = 380, label = 'y')
                screen_width=gr.Slider(1, 1024, value = 900, label = 'width')
                screen_height=gr.Slider(1, 1024, value = 960, label = 'height')
            with gr.Row(scale=0.5 ):
                shotscreen_btn=gr.Button("截图区域配置")
                shotscreen_and_ocr_btn=gr.Button("截图&OCR")
                http_server_btn=gr.Button("http服务")
                update_pipe_opts_btn=gr.Button('更新参数')
            
            with gr.Row(scale=0.5 ):
                guide = gr.Slider(2, 15, value = 7, label = '文本引导强度(guidance scale)')
                steps = gr.Slider(10, 60, value = 30, step = 1, label = '迭代次数(inference steps)')
                width = gr.Slider(384, 768, value = 512, step = 64, label = '宽度(width)')
                height = gr.Slider(384, 768, value = 512, step = 64, label = '高度(height)')
                strength = gr.Slider(0, 1.0, value = 0.8, step = 0.05, label = '参考图改变程度(strength)')
            with gr.Row(scale=0.5 ):
                image_in = gr.Image(source='upload', elem_id="image_upload", type="pil", label="参考图（非必须）(ref)")
            
        with gr.Column(scale=1, ):
            
            keyword = gr.Textbox(label = 'prompt-用户输入')

            style_input = gr.Textbox(label = '风格-预设模板')
            
            get_user_input_and_prompt_btn=gr.Button("截屏提取最新回复作为输入")
         
            use_pipe_opts_btn = gr.Button("根据设定的参数生成图像")

            submit_btn = gr.Button("根据prompt和参数生成图像")
            shotscreen_and_ocr_and_match_keyword_btn=gr.Button("截屏计算投票")
            
                
    with gr.Row(scale=0.5):
        image_out = gr.Image(label = '输出(output)')
        json_out=gr.JSON(label='结果')    
            
    with gr.Row():     
        ex = gr.Examples(examples, fn=infer_text2img, inputs=[keyword,style_input, guide, steps, width, height], outputs=image_out)
        # with gr.Column(scale=1, ):
        #     image_in = gr.Image(source='upload', tool='sketch', elem_id="image_upload", type="pil", label="Upload")
        #     inpaint_prompt = gr.Textbox(label = '提示词(prompt)')
        #     inpaint_btn = gr.Button("图像编辑(Inpaint)")
            # img2img_prompt = gr.Textbox(label = '提示词(prompt)')
            # img2img_btn = gr.Button("图像编辑(Inpaint)")
        use_pipe_opts_btn.click(fn = infer_text2img_for_auto, 
        inputs =keyword, 
        outputs = image_out,api_name="infer_text2img_for_auto")

        submit_btn.click(fn = infer_text2img, 
        inputs = [keyword,style_input, guide, steps, width, height, image_in, strength], 
        outputs = image_out,api_name="infer_text2img")

        update_pipe_opts_btn.click(fn = update_pipe_opts, 
        inputs = [style_input, guide, steps, width, height, image_in, strength], 
        outputs = json_out)

        shotscreen_btn.click(fn=shotscreen_setup,inputs =[screen_x,screen_y,screen_width,screen_height],
        outputs=image_out,
        api_name="shotscreen")

        shotscreen_and_ocr_btn.click(fn=get_user_input,
        outputs=[json_out,image_out],
        api_name="shotscreen_ocr")

        http_server_btn.click(fn=create_http_server,
        inputs = [style_input, guide, steps, width, height, image_in, strength], 
        outputs = json_out)

        get_user_input_and_prompt_btn.click(fn=get_user_input_and_prompt,
        outputs=[keyword,image_out],
        api_name="get_user_input_and_prompt")

        shotscreen_and_ocr_and_match_keyword_btn.click(fn=count_user_feedback,
        inputs =[keyword],
        outputs=json_out,
        api_name="count_user_feedback")

        # inpaint_btn.click(fn = infer_inpaint, inputs = [inpaint_prompt, width, height, image_in], outputs = image_out)
        # img2img_btn.click(fn = infer_img2img, inputs = [img2img_prompt, width, height, image_in], outputs = image_out)
demo.queue(concurrency_count=1, max_size=4).launch(share=True)