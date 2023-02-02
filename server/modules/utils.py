from datetime import datetime,timedelta
import hashlib,json,os,random,io,base64
from itertools import permutations
import soundfile as sf
from PIL import Image
import tkinter.messagebox as msgbox


def print_info(title,text):
    msgbox.showinfo(title,text)

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

# list 按某个key排序，从高到低
def rank(items,key='score',reverse=True):
    def my_func(e):
        return e[key]
    items.sort(reverse=reverse, key=my_func)
    return items

def load_file(filepath):
    with open( filepath, 'r' ) as f:
        return f.read()

# 保存到本地
def write_file(text,filepath):
    f = open(filepath, "w",encoding='utf-8')
    f.write(text)
    f.close()

def write_wav(data, samplerate,wav_file):
    
    # data, samplerate = sf.read('existing_file.wav')
    sf.write(wav_file, data, samplerate)
    return wav_file


def write_json(j,filepath):
    jsonString = json.dumps(j, ensure_ascii=False)
    write_file(jsonString,filepath)

def mkdir(filepath):
    try:
        os.mkdir(filepath)
    except:
        print('---mkdir---')
    return filepath

def get_data_file_path():
    return os.path.join(os.path.split(get_current_dir(__file__))[0],'data')

def get_current_dir(f):
    return os.path.split(os.path.abspath(f))[0]

# 获取目录下的文件
def get_dir_filenames(filepath):
    return [filename for filename in [x[2] for x in os.walk(filepath)][0]]

#按照当前日期获取json文件 2022-12-15.json
def read_dir_json_byday(filepath,day=0):
    res=[]
    filenames=get_dir_filenames(filepath)
    d=get_date_str(day).split(' ')[0]+'.json'
    for filename in filenames:
        if d in filename:
            res.append({
                "filepath":filepath+'/'+filename,
                "filename":filename,
                "data":load_json(filepath+'/'+filename)
            })
    return res

#按照当前日期获取处理好的html文件 2022-12-15_extract.html
def read_dir_extract_html_byday(filepath,day=0):
    res=None
    filenames=get_dir_filenames(filepath)
    d=get_date_str(day).split(' ')[0]+'_extract.html'
    for filename in filenames:
        if d in filename:
            res={
                "filepath":filepath+'/'+filename,
                "filename":filename,
                # "data":load_json(filepath+'/'+filename)
            }
    return res
    

# 获取日期，0 是当天，-1是前天
def get_date_str(today=0):
    d = datetime.today()+timedelta(days=today)
    d = datetime.strftime(d,'%Y-%m-%d %H:%M:%S')
    return d

def get_id(text):
    return hashlib.new('md5', text.encode('utf-8')).hexdigest()


def load_json(filepath):
    with open(filepath,'r') as load_f:
        load_dict = json.load(load_f)
        return load_dict


def is_contain_zh(check_str):
    for ch in check_str: 
        if u'\u4e00' <= ch <= u'\u9fff': 
            return True 
    return False

def random_text(texts):
    i=random.randint(0,len(texts)-1)
    return texts[i]


def image_to_byte_data(image):
    byte_data = io.BytesIO()# 创建一个字节流管道
    if image:
        image.save(byte_data, format="JPEG")# 将图片数据存入字节流管道
        byte_data = byte_data.getvalue()
        
    return byte_data

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
