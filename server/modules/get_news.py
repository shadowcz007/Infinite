from playwright.sync_api import Playwright, sync_playwright

import argparse

try:
    from . import utils
except:
    import utils

FILE_PATH='../data'

IS_RUN=False

KEYWORDS=[]

good_sites='''
 medium.com
 technologyreview.com
 futurism.com
 techcrunch.com        
techmeme.com
theverge.com
thenextweb.com
wired.com
mashable.com
engadget.com
firstpost.com
producthunt.com
digitaltrends.com
a16z.com
vrscout.com
arxiv.org
the-decoder.com
mixed-news.com
tech.sina.com.cn
qbitai.com
jiqizhixin.com
36kr.com
mittrchina.com
leiphone.com
vrtuoluo.cn
news.nweon.com
hub.baai.ac.cn
zhidx.com
about.fb.com
geekpark.net
        '''
good_sites=[k.strip() for k in good_sites.split('\n') if k.strip()!='']

bad_sites='''
msn.com
'''
bad_sites=[k.strip() for k in bad_sites.split('\n') if k.strip()!='']

bad_case='''直播
活动
直播预约
报名
大会
研讨会
开幕
大赛
竞赛
合作论坛
生态论坛
工作动态
创意大赛
weekly report
今日更多新鲜事
项目报道
周报
新动态
完美落幕
培训活动
日报
今日更多大新闻
新闻首页
每日要闻
招生官网
Bing 词典
搜索 图片
_哔哩哔哩
行业情报
搜索 视频
搜索 图片
量子位
展览现场
金财互联
路演
通知
周末利好消息
精彩盘点
本科招生简章
招生专业计划发布
招生信息汇总
赠票
指北播报
风雨看盘
看点回顾
涨停分析
专场回顾
现场直击
全年征订中
习近平
Access Denied
Search Images
Search Videos'''

bad_case=[k.strip() for k in bad_case.split('\n') if k.strip()!='']

def do_keywords(text=''):
    return [k.strip() for k in text.split('\n') if k.strip()!='']


#前一天 已经爬取的数据
pre_datas={}

def get_old_data(file_path=None):
    global FILE_PATH
    if file_path!=None:
        FILE_PATH=file_path
    global pre_datas
    try:
        for i in range(-7,0):
            jsons=utils.read_dir_json_byday(FILE_PATH,i)
            for jsons_data in jsons:
                if isinstance(jsons_data['data'], dict):
                    data=jsons_data['data']['data']
                    #print(jsons_data['filename'])
                    for d in data:
                        pre_datas[utils.get_id(d['url'])]=1
                else:
                    print(jsons_data['filename'])
    except:
        print('目录无数据')

    print('目录地址：',FILE_PATH)
    print('前7天 已经爬取的数据',len(pre_datas.keys()))


def create_html(data):
    html='''<div score="'''+str(data['score'])+'''" style="display: flex;
                flex-direction: column;
                outline: 1px solid gray;
                margin: 12px;
                padding: 24px;
                font-size: 18px;
                font-weight: 800;
                color: black;">'''+data['title']+''' <br>
                '''+( '''<img src="'''+data['imgurl']+'''" style="width: 140px;height: fit-content;"/>''' if data['imgurl'] else '')+'''
                <p style="background: yellow;
                display: block;
                width: fit-content;
                margin: 0;
                margin-top: 12px;
                font-size: 12px;">'''+data['keyword']+' '+data['author']+'''</p> <p style="background: #dedede;
                display: block;
                width: fit-content;
                font-size: 12px;
                font-weight: 300;">'''+data['date']+'''</p> <p style="display: block;
                width: fit-content;
                margin: 6px;
                font-size: 14px;
                font-weight: 300;
                line-height: 24px;">'''+data['snippet']+''' <a href="'''+data['url']+'''" style="
                font-size: 15px;
                font-weight: 800;
                color: black;" target="_blank">  原文链接 </a></p></div>'''.replace('\n','')
    return html





def get_keyword(keyword='web3',page=None):
    global FILE_PATH
    page.goto('https://global.bing.com/search?q=%s&setmkt=en-US&setlang=en')
    page.wait_for_timeout(1000)
    page.goto("https://global.bing.com/news/search?q="+keyword+"&qft=interval%3d%227%22&form=PTFTNR")
    page.wait_for_load_state('domcontentloaded')
    
    items={}

    for i in range(2):
        page.wait_for_timeout(800)
        page.mouse.wheel(0, 1000)
        page.wait_for_timeout(990)
        html = page.evaluate('''var cards=document.querySelectorAll('.news-card');
        cards=Array.from(cards,c=>{
               
                let im=c.querySelector('.rms_img');
                imgurl=im?im.src:"";
                author=c.querySelector('.title').getAttribute('data-author');
                title=c.querySelector('.title').innerText;
                url=c.querySelector('.title').href;
                snippet=c.querySelector('.snippet').title;
                date=Array.from(c.querySelectorAll('.source span'),d=>d.innerText).filter(f=>f)[0];
                
                    return {title,imgurl,author,url,snippet,date}
                
                }).filter(f=>f);
            cards
        ''')
        for h in html:
            uid=utils.get_id(h['url'])
            h['keyword']=keyword
            h['score']=10 if keyword.lower() in h['title'].lower() else 0
            # 评分
            h['score']+=6 if len(h['imgurl'])>0 else 0
            #不错的网站
            h['score']+=len([site for site in good_sites if site in h['url']])*20
            #一些不好的词
            h['score']-=len([bc for bc in bad_case if bc in h['title']])*2
            #不好的网站
            h['score']-=len([site for site in bad_sites if site in h['url']])*10
        
            h['html']=create_html(h)
            
            if not uid in pre_datas:
                items[uid]=h
            else:
                print('已经有了:',h['title'])
    
    count=len(items.keys())
    print(keyword,'__',count)

    d = utils.get_date_str()

    res={
        "keyword":keyword,
        "count":count,
        "datetime":d,
        "html":"<h4>"+keyword+"_"+str(count)+"条</h4>",
        "htmls":[]
    }

    res["data"]=utils.rank([x for x in items.values()])

    for r in res['data']:
        res['html']+=r['html']
        res["htmls"].append({
            "score":r['score'],
            "html":r['html']
        })
    
    utils.write_json(res,FILE_PATH+"/data_"+keyword+"_"+str(res["count"])+"_"+(d.split(' ')[0])+".json")
  
    return res['htmls']


def run(playwright: Playwright) -> None:
    global IS_RUN
    global FILE_PATH
    global KEYWORDS
    browserLaunchOptionDict = {
        "headless": True
    }
    browser = playwright.chromium.launch(**browserLaunchOptionDict)
    context = browser.new_context()
    page = context.new_page()

    d=utils.get_date_str()

    count_keywords=[]

    htmls_data=[]
    for k in KEYWORDS:
        try:
            htmls=get_keyword(k,page)
            for h in htmls:
                htmls_data.append(h)
            if len(htmls)>0:
                count_keywords.append(k)
        except:
            print('#####error:',k)
        page.wait_for_timeout(1500)

    html="<p>"+(d.split(' ')[0])+"_"+str(len(htmls_data))+"条 <br>"+",".join(count_keywords)+"</p>"
    html+="".join([h['html'] for h in utils.rank(htmls_data)])

    html='''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>'''+(d.split(' ')[0])+'''</title>
</head><body>'''+html +'''</body></html>'''
    

    utils.write_file(html,FILE_PATH+"/"+(d.split(' ')[0])+"_"+str(len(count_keywords))+".html")
   
    # # ---------------------
    context.close()
    browser.close()
    utils.print_info('完成','本次共获得'+str(len(count_keywords))+'条')
    IS_RUN=False


def start(file_path=None,keywords=''):
    global IS_RUN
    global KEYWORDS
    if IS_RUN==False:
        # keywords
        KEYWORDS=do_keywords(keywords)
        print('目标关键词',KEYWORDS)
        # file_path
        get_old_data(file_path)
        IS_RUN=True
        with sync_playwright() as playwright:
            run(playwright)


def parse_args():
    description = "爬取每日资讯..."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-f", "--filepath", type=str, default=None, help="传入地址")
    parser.add_argument("-k", "--keywords", type=str, default='''
        元宇宙
metaverse
DAO
AIGC
chatGPT
数字艺术
crypto art
Virtual Spaces
digital human
meta-human
数字人
虚拟人
web3
nft
Stable Diffusion
EleutherAI 
Extended Reality
Virtual Reality
Augmented Reality
增强现实
虚拟现实
虚拟世界
开发者社区
AI大模型
WebXR
Artificial intelligence
人工智能
脑机接口
游戏引擎
数字资产
深度学习
机器学习
自然语言处理
计算机视觉
游戏开发
数字化
可视化
可交互式
元宇宙服装
Product-led Growth
产品设计
AI
AI写作工具
AI艺术家
AR
Accomplice.ai
AltspaceVR
Artbreeder
CHATGPT
CHATGPT应用指南
DALL·E
Dall-E 2
DreamBooth
GFPGAN
GPT-3
GPT3
Getty Images
InstructPix2Pix
OPENAI
PhotoRoom
Plai Labs
QuickNode
Roblox
Stability AI
StyleGAN-T
TPS Motion
TTS
Unstable Diffusion
VR
Voldex
XR
a16z
action
haiper3d
nanoGPT
producthunt
stable diffusion
talking face
whisper
人工智能艺术
创新公司
增强现实应用程序
开源
开源社区
微软
提示工程
搜索引擎
智能产品
混合现实耳机
游戏
知识引擎
硬件
社交平台
设计工具
语音识别
谷歌
面部识别
        ''', help="传入关键词")
    return parser.parse_args()



if __name__ == "__main__":
    
    args = parse_args()
    start(args.filepath,args.keywords)
