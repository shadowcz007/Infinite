from playwright.sync_api import Playwright, sync_playwright, expect
import json,hashlib
from datetime import datetime

PROXY_HTTP = "http://127.0.0.1"
# PROXY_SOCKS5 = "socks5://127.0.0.1:51837"

browserLaunchOptionDict = {
    "headless": True,
    # "proxy": {
    #     "server": PROXY_HTTP,
    # }
}

keywords='''
元宇宙
metaverse
DAO
AIGC
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
VR 
AR
XR
增强现实 
虚拟现实 
WebXR 
Artificial intelligence 
脑机接口 
AI大模型 
游戏引擎'''

keywords=[k.strip() for k in keywords.split('\n') if k.strip()!='']


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
www.qbitai.com
www.jiqizhixin.com
www.36kr.com
www.mittrchina.com
www.leiphone.com
www.vrtuoluo.cn
news.nweon.com
hub.baai.ac.cn
zhidx.com
        '''
good_sites=[k.strip() for k in good_sites.split('\n') if k.strip()!='']

bad_case='''直播
活动
直播预约
报名
大会
研讨会
开幕
大赛
竞赛
工作动态
weekly report
今日更多新鲜事
项目报道
周报
Bing 词典
搜索 图片
_哔哩哔哩
搜索 视频
搜索 图片
Access Denied
Search Images
Search Videos'''

bad_case=[k.strip() for k in bad_case.split('\n') if k.strip()!='']


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
                color: black;">  原文链接 </a></p></div>'''.replace('\n','')
    return html


def rank(items):
    def my_func(e):
        return e['score']

    items.sort(reverse=True, key=my_func)
    return items


def get_keyword(keyword='web3',page=None):
    page.goto('https://global.bing.com/search?q=%s&setmkt=en-US&setlang=en')
    page.wait_for_timeout(1000)
    page.goto("https://global.bing.com/news/search?q="+keyword+"&qft=interval%3d%227%22&form=PTFTNR")
    page.wait_for_load_state('domcontentloaded')
    
    items={}

    for i in range(10):
        page.wait_for_timeout(800)
        page.mouse.wheel(0, 1000)
        page.wait_for_timeout(1200)
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
            uid=hashlib.new('md5', h['url'].encode('utf-8')).hexdigest()
            h['keyword']=keyword
            h['score']=1 if keyword.lower() in h['title'].lower() else 0
            # 评分
            h['score']+=1 if len(h['imgurl'])>0 else 0
            #不错的网站
            h['score']+=len([site for site in good_sites if site in h['url']])
            #一些不好的词
            h['score']-=len([bc for bc in bad_case if bc in h['title']])
        
            h['html']=create_html(h)
            items[uid]=h
    
    count=len(items.keys())
    print(keyword,'__',count)

    d = datetime.today()
    d = datetime.strftime(d,'%Y-%m-%d %H:%M:%S')

    res={
        "keyword":keyword,
        "count":count,
        "datetime":d,
        "html":"<h4>"+keyword+"_"+str(count)+"条</h4>",
        "htmls":[]
    }

    res["data"]=rank([x for x in items.values()])

    for r in res['data']:
        res['html']+=r['html']
        res["htmls"].append({
            "score":r['score'],
            "html":r['html']
        })
   
    jsonString = json.dumps(res, ensure_ascii=False)
    jsonFile = open("./data/data_"+keyword+"_"+str(res["count"])+"_"+(d.split(' ')[0])+".json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()
    return res['htmls']

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(**browserLaunchOptionDict)
    context = browser.new_context()
    page = context.new_page()

    d = datetime.today()
    d = datetime.strftime(d,'%Y-%m-%d %H:%M:%S')

    count_keywords=[]

    htmls_data=[]
    for k in keywords:
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
    html+="".join([h['html'] for h in rank(htmls_data)])

    html='''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>'''+(d.split(' ')[0])+'''</title>
</head><body>'''+html +'''</body></html>'''

    f = open("./data/"+(d.split(' ')[0])+"_"+str(len(count_keywords))+".html", "w")
    f.write(html)
    f.close()

    # # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
