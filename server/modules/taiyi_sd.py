
try:
    from . import utils
except:
    import utils


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
，使用Blender渲染的超现实主义，8K详细度，锐化，写实摄影作品，3d作品，水墨风格。
，细节清晰，不要有手，使用Blender渲染的超现实主义，8K详细度，锐化，游戏引擎作品，3d作品，三维建模，现实感，画面明亮，水墨风格，水彩的色彩，立体卡通，摄影后期，完整的画面
，细节清晰，宋徽宗的丝网印刷, featured on pixiv, featured on amiami, bong， thick oil painting，8K详细度，锐化，中国油画

'''.split("\n") if len(k.strip())>0]

  
def random_prompt_style():
    return ''+utils.random_text(STYLE_PROMPTS)

def random_keyword():
    return utils.random_text(KEYWORDS)


pipe_text2img=None
pipe_img2img=None
pipe_opts=None

def update_pipe_opts(style_prompt,guide, steps, width, height, image_in, strength):
    global pipe_opts
    # print(image_in)
    pipe_opts={
        "style_prompt":style_prompt,
        "guide":guide,
        "steps":steps,
        "width":width,
        "height":height,
        "image_in":utils.image_to_base64(image_in),
        "strength":strength
    }
    return pipe_opts

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


def infer_text2img_for_auto(prompt):
    global pipe_opts
    im=infer_text2img(prompt,
    pipe_opts["style_prompt"],
    pipe_opts["guide"],
    pipe_opts["steps"],
    pipe_opts["width"],
    pipe_opts["height"],
    utils.base64_to_image(pipe_opts["image_in"]),
    pipe_opts["strength"]
    )
    return im


def infer_inpaint(prompt, guide, steps, width, height, image_in): 
    init_image = image_in["image"].convert("RGB").resize((width, height))
    mask = image_in["mask"].convert("RGB").resize((width, height))

    output = pipe_inpaint(prompt, \
                        init_image=init_image, mask_image=mask, \
                        width=width, height=height, \
                        guidance_scale=7.5, num_inference_steps=20)
    image = output.images[0]
    return image