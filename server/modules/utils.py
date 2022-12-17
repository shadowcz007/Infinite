from datetime import datetime
import hashlib,json,os
from itertools import permutations

# list 按某个key排序，从高到低
def rank(items,key='score',reverse=True):
    def my_func(e):
        return e[key]
    items.sort(reverse=reverse, key=my_func)
    return items

# 保存到本地
def write_file(text,filepath):
    f = open(filepath, "w")
    f.write(text)
    f.close()

def write_json(j,filepath):
    jsonString = json.dumps(j, ensure_ascii=False)
    jsonFile = open(filepath, "w")
    jsonFile.write(jsonString)
    jsonFile.close()


def mkdir(filepath):
    try:
        os.mkdir(filepath)
    except:
        print('---mkdir---')
    return filepath


def get_date_str():
    d = datetime.today()
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