
import os
try:
    from . import utils
except:
    import utils


from ppgan.apps.wav2lip_predictor import Wav2LipPredictor
from ppgan.apps.first_order_predictor import FirstOrderPredictor

wav2lip_module = None
fom_module=None

driving_video_user=None
 

d,filename = os.path.split(utils.get_current_dir(__file__))
fom_output=d+'/data/FOM_result.mp4'
wav_output=d+'/data/wav2lip_result.mp4'


def init_fom():
    global fom_module
    if fom_module==None:
        output,filename=os.path.split(fom_output)
        fom_module  =FirstOrderPredictor(output = output, 
                                                filename = filename, 
                                                face_enhancement = True, 
                                                ratio = 0.4,
                                                relative = True,
                                                image_size=512,
                                                adapt_scale = True)
def init_wav():
    global wav2lip_module
    if wav2lip_module==None:
        wav2lip_module  = Wav2LipPredictor(
                                face_det_batch_size = 2,
                                 wav2lip_batch_size = 16,
                                 face_enhancement = True)
def init():
    init_fom()
    init_wav()

def FOM(source_image,driving_video):
    init_fom()
    global fom_module
    fom_module.run(source_image, driving_video)
    return fom_output

def wav2lip(audio_input_path,face_input_path):
    init_wav()
    global wav2lip_module
    wav2lip_module.run(
        face_input_path, 
        audio_input_path,wav_output)
    return wav_output

# def run(face_image_input,audio_input_path):
#     global driving_video_user,driving_video_user_res

#     if driving_video_user_res==None:
#         if driving_video_user!=None:
#             fom_res=FOM(face_image_input,driving_video_user)
#             driving_video_user_res=fom_res
    
#     wav2lip(audio_input_path,fom_res)
#     return wav_output
   
