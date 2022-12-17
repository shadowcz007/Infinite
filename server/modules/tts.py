
import paddlehub as hub
import argparse
try:
    from . import utils
except:
    import utils
import os

tts_model=None



def init(output_dir=None,speaker_audio=None):
    global tts_model
    if output_dir==None:
        output_dir=os.path.join(utils.get_current_dir(__file__),'../data')
    if speaker_audio==None:
        speaker_audio=os.path.join(utils.get_current_dir(__file__),'../data/shadow.wav')

    tts_model = hub.Module(name='ge2e_fastspeech2_pwgan', output_dir=output_dir, speaker_audio=speaker_audio) 

    return 


def start(text,output_dir=None,speaker_audio=None):
    global tts_model
    if tts_model==None:
        init(output_dir,speaker_audio)
    wav_files =  tts_model.generate([text],use_gpu='gpu')
    print(wav_files)
    return wav_files[0]



def parse_args():
    description = "语音生成tts..."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-t", "--text", type=str, default='', help="文本")
    parser.add_argument("-o", "--output_dir", type=str, help="导出地址")
    parser.add_argument("-s", "--speaker_audio", type=str, help="克隆声音的地址wav格式")
    return parser.parse_args()


if __name__ == "__main__":
    
    args = parse_args()

    if args.text!="":
        res=start(args.text,args.output_dir,args.speaker_audio)
        print(res)

    