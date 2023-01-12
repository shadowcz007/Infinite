 
from diffusers import StableDiffusionPipeline
import torch


# model_name='shadow/duckduck-roast_duck-heywhale'
model_name='IDEA-CCNL/Taiyi-Stable-Diffusion-1B-Chinese-EN-v0.1'

# ,safety_checker=None
torch.backends.cudnn.benchmark = True
sd_zh_pipe = StableDiffusionPipeline.from_pretrained(model_name, torch_dtype=torch.float16,safety_checker=None)
sd_zh_pipe.to('cuda')



from itertools import product

import argparse
try:
    from . import utils
except:
    import utils


def split_text(text,num=2):
    texts=text.split(',')

    result=[];

    #二阶
    if num==2:
        res = list(product(texts,texts))

        for r in res:
            if r[0]!=r[1]:
                result.append(",".join(r))
    elif num==3:
  
        #三阶
        res = list(product(texts,texts,texts))
        for rs in res:
            nr={}
            for r in rs:
                nr[r]=1
            if len(nr.keys())==3:
                result.append(",".join(rs))
    elif num==1:
        return texts

    return result


def mkdir(output,id):
    pn=output+'/'+id
    utils.mkdir(pn)
    return pn


def create_image_and_save(file_path,items=[],seed=1024):
    generator = torch.Generator("cuda").manual_seed(seed)
    for i in items:
        images=sd_zh_pipe(i,num_inference_steps=60, guidance_scale=9.0,num_images_per_prompt=1,generator=generator).images
        name=str(i)+'.png'
        images[0].save(file_path+'/'+name)
        print('###',i)


def start(text,file_path,num=2,seed=1024):
    id=utils.get_id(text)
    output_file_path=mkdir(file_path,id)
    print(output_file_path)
    items =split_text(text,num)
    create_image_and_save(output_file_path,items,seed)



def parse_args():
    description = "提示词研究..."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-t", "--text", type=str, default='', help="传入提示词用英文逗号,分开")
    parser.add_argument("-o", "--output", type=str, default='images', help="输出的文件夹地址")
    parser.add_argument("-n", "--num", type=int, default=2, help="组合的元素数量")
    parser.add_argument("-s", "--seed", type=int, default=1024, help="seed")
    return parser.parse_args()
    


if __name__ == "__main__":
    
    args = parse_args()
    print(args)
    print(type(args))
    print(args.text,args.seed)
    if args.text!="":
        start(args.text,args.output,args.num,args.seed)