from subprocess import PIPE, Popen
import json,os,base64
import gradio as gr
import soundfile as sf
import librosa
import numpy as np
import paddlehub as hub



 
# asr_model = hub.Module(
#     name='deepspeech2_aishell',
#     version='1.0.0')
 

# tts_model = hub.Module(
#     name='fastspeech2_baker',
#     version='1.0.0',output_dir="./data")

chatbot_model = hub.Module(name='plato-mini')
tts_model = hub.Module(name='ge2e_fastspeech2_pwgan', output_dir='./data', speaker_audio='./data/shadow.wav') 


def re_wav_16k(name,samplerate=16000):
    src_sig,sr = sf.read(name) 
    dst_sig = librosa.resample(src_sig,sr,samplerate)
    return write_wav(dst_sig,samplerate)


def write_wav(data, samplerate):
    wav_file='./data/new_file.wav'
    # data, samplerate = sf.read('existing_file.wav')
    sf.write(wav_file, data, samplerate)
    return wav_file


def speech_recognize(wav_file):
    # # 采样率为16k，格式为wav的中文语音音频
# wav_file = '/PATH/TO/AUDIO'
    text = asr_model.speech_recognize(wav_file,device='gpu')
    return text

def speech_generate(text):
    wav_files =  tts_model.generate([text],use_gpu='gpu')
    return wav_files[0]

def chatbot(text):
    data = [[text]]
    result = chatbot_model.predict(data,use_gpu=True) 
    return result[0]

def get_platform():
    import platform
    sys_platform = platform.platform().lower()
    pf=""
    if "windows" in sys_platform:
        #print("Windows")
        pf="windows"
    elif "macos" in sys_platform:
        #print("Mac os")
        pf="macos"
    elif "linux" in sys_platform:
        #print("Linux")
        pf="linux"
    # else:
    #     print("其他系统")
    return pf






rhu="./Rhubarb-Lip-Sync-1.13.0-macOS/rhubarb" if get_platform()=='macos' else "./Rhubarb-Lip-Sync-1.13.0-Windows/rhubarb.exe"

def alphabetic_to_viseme(name,weight=1):
    # keys={
    #     "A":"MBP",
    #     "B":"etc","C":"E",
    #     "D":"AI",
    #     "E":"O",
    #     "F":"U",
    #     "G":"FV",
    #     "H":"L",
    #     "X":"rest"
    # }
    keys={
        "A":"viseme_PP",
        "B":"viseme_SS",
        "C":"viseme_E",
        "D":"viseme_I",
        "E":"viseme_O",
        "F":"viseme_U",
        "G":"viseme_FF",
        "H":"viseme_kk",
        "X":"rest"
    }

    visemes={
        "viseme_PP":0,
        "viseme_SS":0,
         "viseme_E":0,
         "viseme_I":0,
         "viseme_O":0,
         "viseme_U":0,
         "viseme_FF":0,
         "viseme_kk":0
    }

    result={}
    for k,v in visemes.items():
        result[k]= weight if k==keys[name] and name!='X' else 0
    return result

def lip_sync(audiopath):
    file = open(audiopath, "rb").read()   # 读取本地语音文件   
    text = base64.b64encode(file).decode("utf-8")   # 对读取的文件进行base64编码

    #open a cmd instance of Rhubarb
    cmd = Popen([rhu,"-r","phonetic", "-f", "json",audiopath], stdout=PIPE)
    result = cmd.communicate()
    res=json.loads(result[0])
    res['base64']='data:audio/wav;base64,'+text
    # print(result)
    return res

def create_weight_data(size=3):
    data=np.random.normal(loc=1, scale=1, size=size)
    _range=np.max(data)-np.min(data)
    if _range==0:
        _range=1
    return (data-np.min(data))/_range

#24fps 
def mouth_shapes_to_frames(duration,mouth_cues):
    fps=18
    # print(duration)
    frames=[x for x in range(0,int(24*duration))]
    # print(len(frames),duration)
    for m in mouth_cues:
        start_index=int(24*m["start"])
        end_index=int(24*m["end"])
        # print('start_index',start_index)

        # print('-------')
        # 按照正态分布生成嘴型变化
        weights=create_weight_data(1+end_index-start_index)

        for index in range(start_index,end_index+1):
            weight=weights[index-start_index]*0.9
            # 优化张嘴的幅度
            # print(weight,index,start_index,end_index,len(frames))
            index=min(index,len(frames)-1)
            frames[index]={
                "name":m['value'],
                "viseme":alphabetic_to_viseme(m['value'],weight)
            }
    return {
        "duration":duration,
        "fps":fps,
        "frames":frames
    }



def start(question,wav_file_input,radio_input):

    if radio_input== "asr-chatbot":
        speech_recognize(wav_file_input)
    elif radio_input== "text-chatbot":
        #
        text=chatbot(question)
        wav_file = speech_generate(text)
        # print(text)
    elif radio_input=="tts":
        wav_file = speech_generate(question)
        text=question
        # print(wav_file)
    else:
        wav_file=write_wav(wav_file_input[1],wav_file_input[0])
    #TODO 改造成 接受录音，返回答案
    # asr - > chatbot ->tts
    
    #wav_file=write_wav(wav_file_input[1],wav_file_input[0])
    data=lip_sync(wav_file)
    frames=mouth_shapes_to_frames(data["metadata"]["duration"],data["mouthCues"])
    frames['base64']=data['base64']
    frames['question']=question
    frames['text']=text
    return wav_file,frames


with gr.Blocks() as demo:
    with gr.Row(scale=1,):
        input_text = gr.Textbox(label = '输入文字')
        audio_upload = gr.Audio(label="录音",type="numpy")
        # chatbot 文字输入，聊天机器人回复，返回语音
        # asr 语音输入，聊天机器人回复，返回语音
        # tts 文字输入，返回语音
        radio=gr.Radio(["asr-chatbot", "text-chatbot","tts","lip"])
        submit_btn = gr.Button(label="生成")
    with gr.Row(scale=1,):
        json_out=gr.JSON(label='结果')   
         

    submit_btn.click(fn=start,
        inputs =[input_text,audio_upload,radio],
        outputs=[audio_upload,json_out],
        api_name="audio_lip")


if __name__ == "__main__":
    demo.queue(concurrency_count=4, max_size=8).launch(share=False,server_name="0.0.0.0")