from . import utils
import base64,json
from subprocess import PIPE, Popen
import argparse
import numpy as np
import os


ph="mac" if utils.get_platform()=='macos' else "win"

# rhu="./Rhubarb-Lip-Sync-1.13.0-macOS/rhubarb" if utils.get_platform()=='macos' else "./Rhubarb-Lip-Sync-1.13.0-Windows/rhubarb.exe"


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




def rhu_run(audiopath,mac,win):
    
    rhu=mac if ph=='mac' else win
    # print(win,utils.get_current_dir(__file__))
    file = open(audiopath, "rb").read()   # 读取本地语音文件   
    text = base64.b64encode(file).decode("utf-8")   # 对读取的文件进行base64编码

    #open a cmd instance of Rhubarb
    cmd = Popen([rhu,"-r","phonetic", "-f", "json",audiopath], stdout=PIPE)
    result = cmd.communicate()
    res=json.loads(result[0])
    res['base64']='data:audio/wav;base64,'+text
    # print(result)
    return res

def start(audiopath,mac=None,win=None):
    if mac==None:
        mac=utils.get_current_dir(__file__)+'/Rhubarb-Lip-Sync-1.13.0-macOS/rhubarb'
    if win==None:
        win=utils.get_current_dir(__file__)+'/Rhubarb-Lip-Sync-1.13.0-Windows/rhubarb.exe'

    data=rhu_run(audiopath,mac,win)
    frames=mouth_shapes_to_frames(data["metadata"]["duration"],data["mouthCues"])
    frames['base64']=data['base64']
    return frames



def parse_args():
    description = "语音生成lip..."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-a", "--audiopath", type=str, default='', help="传入地址")
    parser.add_argument("-m", "--mac", type=str, default='./Rhubarb-Lip-Sync-1.13.0-macOS/rhubarb', help="Rhubarb-mac地址")
    parser.add_argument("-w", "--win", type=str, default='./Rhubarb-Lip-Sync-1.13.0-Windows/rhubarb.exe', help="Rhubarb-Windows地址")
    
    return parser.parse_args()


if __name__ == "__main__":
    
    args = parse_args()

    if args.audiopath!="":
        res=start(args.audiopath,args.mac,args.win)
        print(res)