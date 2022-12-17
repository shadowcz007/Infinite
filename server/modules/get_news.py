from playwright.sync_api import Playwright, sync_playwright, expect


from . import utils

FILE_PATH='../data'

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
人工智能
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
新闻首页
Bing 词典
搜索 图片
_哔哩哔哩
行业情报
搜索 视频
搜索 图片
量子位
金财互联
Access Denied
Search Images
Search Videos'''

bad_case=[k.strip() for k in bad_case.split('\n') if k.strip()!='']


#前一天 已经爬取的数据
pre_datas={}

jsons=utils.read_dir_json_byday(FILE_PATH,-1)
for jsons_data in jsons:
    data=jsons_data['data']['data']
    for d in data:
        pre_datas[utils.get_id(d['url'])]=1

print('前一天 已经爬取的数据',len(pre_datas.keys()))


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
            uid=utils.get_id(h['url'])
            h['keyword']=keyword
            h['score']=1 if keyword.lower() in h['title'].lower() else 0
            # 评分
            h['score']+=1 if len(h['imgurl'])>0 else 0
            #不错的网站
            h['score']+=len([site for site in good_sites if site in h['url']])
            #一些不好的词
            h['score']-=len([bc for bc in bad_case if bc in h['title']])
        
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
    browser = playwright.chromium.launch(**browserLaunchOptionDict)
    context = browser.new_context()
    page = context.new_page()

    d=utils.get_date_str()

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
    html+="".join([h['html'] for h in utils.rank(htmls_data)])

    html='''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>'''+(d.split(' ')[0])+'''</title>
</head><body>'''+html +'''</body></html>'''
    

    utils.write_file(html,FILE_PATH+"/"+(d.split(' ')[0])+"_"+str(len(count_keywords))+".html")
   
    # # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
