# import os
# os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'

# import torch

# from diffusers import (
#     StableDiffusionPipeline,
#     StableDiffusionImg2ImgPipeline,
#     StableDiffusionInpaintPipeline,
# )

# device="cuda"
# model_id = "IDEA-CCNL/Taiyi-Stable-Diffusion-1B-Chinese-v0.1"

# pipe_text2img = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to(device)
# pipe_img2img = StableDiffusionImg2ImgPipeline(**pipe_text2img.components).to(device)


# # guide = gr.Slider(2, 15, value = 7, label = '文本引导强度(guidance scale)')
# # steps = gr.Slider(10, 30, value = 20, step = 1, label = '迭代次数(inference steps)')
# # width = gr.Slider(512, 512, value = 512, step = 64, label = '宽度(width)')
# # height = gr.Slider(512, 512, value = 512, step = 64, label = '高度(height)')
# # strength = gr.Slider(0, 1.0, value = 0.8, step = 0.05, label = '参考图改变程度(strength)')

# # res=infer_text2img(prompt,image_in=im)

# def infer_text2img(prompt, guide=10, steps=30, width=512, height=512, image_in=None, strength=1):
#     if image_in is not None:
#         init_image = image_in.convert("RGB").resize((width, height))
#         output = pipe_img2img(prompt, init_image=init_image, strength=strength, width=width, height=height, guidance_scale=guide, num_inference_steps=steps)
#     else:
#         output = pipe_text2img(prompt, width=width, height=height, guidance_scale=guide, num_inference_steps=steps,)
#     image = output.images[0]
#     return image


import time,json

pre_count=0
pre_text='input_text'
    
USER_COUNT_PATH='sd/user.json'

def write_json(a,file_path):
    b = json.dumps(a)
    f2 = open(file_path, 'w')
    f2.write(b)
    f2.close()
    return


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

while True:
    write_user_feedback(["1"])
    time.sleep(2)
    write_user_feedback(["1","1","1"])
    time.sleep(2)
    write_user_feedback(["1","1","1"])
    time.sleep(2)
    write_user_feedback(["1","1","1"])