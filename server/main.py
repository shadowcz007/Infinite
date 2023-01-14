import random

import json,os,io,base64

from PIL import Image
import gradio as gr

import modules.utils as utils
import modules.http_server as http_server

import modules.ocr as ocr
import modules.lip_sync as lip_sync
import modules.tts as tts
import modules.chatbot as chatbot
import modules.fom as fom 

import modules.taiyi_sd as taiyi_sd
import modules.pai_painter as pai_painter

import modules.get_news as get_news

# 保存数据的路径
data_file_path=utils.get_data_file_path()

#上一次用户输入
pre_text='1'

#记录上一次用户投票
pre_count=0

fom_res=None


def create_http_server(style_prompt,guide, steps, width, height, image_in, strength):
    http_server.start()
    return taiyi_sd.update_pipe_opts(style_prompt,guide, steps, width, height, image_in, strength)



#获取用户输入
def get_user_input():
    #截屏
    im,result = ocr.start()

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


def tts_init(wav_file_input):
    wav_file=utils.write_wav(wav_file_input[1],wav_file_input[0],'./data/wav_file.wav')
    tts.init(None,wav_file)
    wav_file = tts.start('你好呀，初次见面，请多多指教啊')
    return wav_file

def tts_sync(question,wav_file_input,radio_input):
    # print(question)
    if radio_input== "asr-chatbot":
        # speech_recognize(wav_file_input)
        print('speech_recognize')
    elif radio_input== "text-chatbot":
        #
        text=chatbot.start(question)
        wav_file = tts.start(text)
        # print(text)
    elif radio_input=="tts":
        wav_file = tts.start(question)
        text=question
        # print(wav_file)
    else:
        wav_file=utils.write_wav(wav_file_input[1],wav_file_input[0],'./data/wav_file.wav')
        text=question
    #TODO 改造成 接受录音，返回答案
    # asr - > chatbot ->tts
    
    #wav_file=write_wav(wav_file_input[1],wav_file_input[0])
    frames=lip_sync.start(wav_file)
 
    frames['question']=question
    frames['text']=text
    return wav_file,frames

def fom_run(video_input,face_input):
    global fom_res
    if video_input and face_input:
        fom_res=fom.FOM(utils.image_to_byte_data(face_input),video_input)
    return fom_res

def wav2lip_run(text,face_input):
    global fom_res
    wav_file = tts.start(text)

    if fom_res:
        face_input=fom_res
    
    res=fom.wav2lip(wav_file,face_input)
    
    return res



def pai_painter_start(t):
    ims=pai_painter.start(t)
    im=utils.random_text(ims)
    return im.argument,im


def get_news_run():
    get_news.start(data_file_path)
    return {
        "data":"正在爬取"
    }



with gr.Blocks(css="main.css") as demo:
    examples = [[taiyi_sd.random_keyword(),x] for x in taiyi_sd.STYLE_PROMPTS]
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
                model_id_input=gr.Dropdown(label='huggface-模型-id',value=taiyi_sd.get_model_list()[0],choices=taiyi_sd.get_model_list())
                # model_id_input = gr.Textbox(label = '风格-预设模板',value='shadow/duckduck-roast_duck-heywhale')
                update_pipe_opts_btn=gr.Button('更新参数')
                get_news_btn=gr.Button('爬取今天资讯')
            
            with gr.Row(scale=0.5 ):
                guide = gr.Slider(2, 15, value = 7, label = '文本引导强度(guidance scale)')
                steps = gr.Slider(10, 60, value = 30, step = 1, label = '迭代次数(inference steps)')
                width = gr.Slider(384, 768, value = 512, step = 64, label = '宽度(width)')
                height = gr.Slider(384, 768, value = 512, step = 64, label = '高度(height)')
                strength = gr.Slider(0, 1.0, value = 0.8, step = 0.05, label = '参考图改变程度(strength)')
            with gr.Row(scale=0.5 ):
                image_in = gr.Image(source='upload', elem_id="image_upload", type="pil", label="sd参考图（非必须）(ref)，虚拟人的人像照片")

            with gr.Row(scale=0.5):
                wav_file_input = gr.Audio(label="录音",type="numpy")
                tts_radio=gr.Radio(["asr-chatbot", "text-chatbot","tts","lip"])
                tts_lip_btn = gr.Button("语音生成")
                tts_init_btn=gr.Button('克隆声音')

            with gr.Row(scale=0.5):
                video_input = gr.Video()
                fom_btn=gr.Button("fom生成")
                wav2lip_btn=gr.Button("虚拟人播报生成")

            with gr.Row(scale=0.5):
                pai_painter_btn = gr.Button("pai_painter生成")
            
        with gr.Column(scale=1, ):
            
            keyword = gr.Textbox(label = 'prompt-用户输入,tts的文字')

            style_input = gr.Textbox(label = '风格-预设模板')
            
            get_user_input_and_prompt_btn=gr.Button("截屏提取最新回复作为输入")
         
            use_pipe_opts_btn = gr.Button("根据设定的参数生成图像")

            submit_btn = gr.Button("根据prompt和参数生成图像")
            shotscreen_and_ocr_and_match_keyword_btn=gr.Button("截屏计算投票")
            
                
    with gr.Row(scale=0.5):
        video_out=gr.Video(label='结果')
        image_out = gr.Image(label = '输出(output)')
        json_out=gr.JSON(label='结果')    
            
    with gr.Row():     
        ex = gr.Examples(examples, fn=taiyi_sd.infer_text2img, inputs=[keyword,style_input, model_id_input,guide, steps, width, height], outputs=image_out)
        # with gr.Column(scale=1, ):
        #     image_in = gr.Image(source='upload', tool='sketch', elem_id="image_upload", type="pil", label="Upload")
        #     inpaint_prompt = gr.Textbox(label = '提示词(prompt)')
        #     inpaint_btn = gr.Button("图像编辑(Inpaint)")
            # img2img_prompt = gr.Textbox(label = '提示词(prompt)')
            # img2img_btn = gr.Button("图像编辑(Inpaint)")
        use_pipe_opts_btn.click(fn = taiyi_sd.infer_text2img_for_auto, 
        inputs =keyword, 
        outputs = image_out,api_name="infer_text2img_for_auto")

        submit_btn.click(fn = taiyi_sd.infer_text2img, 
        inputs = [keyword, style_input,model_id_input, guide, steps, width, height, image_in, strength], 
        outputs = image_out,api_name="infer_text2img")

        pai_painter_btn.click(fn=pai_painter_start,
        inputs=keyword,
        outputs=[json_out,image_out],
        api_name="pai_painter")

        update_pipe_opts_btn.click(fn = taiyi_sd.update_pipe_opts, 
        inputs = [model_id_input,style_input, guide, steps, width, height, image_in, strength], 
        outputs = json_out)

        shotscreen_btn.click(fn=ocr.shotscreen_setup,inputs =[screen_x,screen_y,screen_width,screen_height],
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

        tts_init_btn.click(fn=tts_init,
        inputs=wav_file_input,
        outputs=wav_file_input,
        )

        tts_lip_btn.click(fn=tts_sync,
        inputs=[keyword,wav_file_input,tts_radio],
        outputs=[wav_file_input,json_out],
        api_name="audio_lip")

        fom_btn.click(fn=fom_run,
        inputs=[video_input,image_in],
        outputs=video_out
        )
        wav2lip_btn.click(fn=wav2lip_run,
        inputs=[keyword,image_in],
        outputs=video_out
        )

        get_news_btn.click(fn=get_news_run,
        inputs=[],
        outputs=[json_out])

        # inpaint_btn.click(fn = infer_inpaint, inputs = [inpaint_prompt, width, height, image_in], outputs = image_out)
        # img2img_btn.click(fn = infer_img2img, inputs = [img2img_prompt, width, height, image_in], outputs = image_out)
demo.queue(concurrency_count=1, max_size=4).launch(share=False)