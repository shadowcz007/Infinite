from paddlenlp import Taskflow

import os

from . import utils

schema={
"人物": "Person",
"公司/组织/机构": "Company/Organization",
"地点": "Location",
"事件": "Event",
"产品": "Product",
"服务": "Service",
"政策": "Policy",
"技术": "Technology",
"数据": "Data",
"专利": "Patent",
"法律": "Law",
"文化": "Culture",
"时间": "Time",
"历史": "History"
}

schema_zh = [x for x in schema.keys()]
schema_en=[x for x in schema.values()]
print(schema_zh,'_',schema_en)
ie = Taskflow('information_extraction', schema=schema_zh)
ie_en = Taskflow('information_extraction', schema=schema_en, model='uie-base-en')
# similarity = Taskflow("text_similarity")



def start(filepath='./data',today=0):
    
    items={}

    jsons=utils.read_dir_json_byday(filepath,today)
 
    for jsons_data in jsons:
        data=jsons_data['data']
        for item in data['data']:
            if isinstance(item, dict):
                # print(item.keys())
                item['text']=(",".join([item['title'],item['snippet'],item['keyword']])).lower()

                #print('* ',item['title'])
                item['event']=extract(item['title'],item['text'],'zh' if utils.is_contain_zh(item['text']) else 'en')
                
                if item['event'] and len(item['imgurl'])>0:
                    # 如果有提取出信息才能进一步  && 有封面图的

                    item['score']+=len(item['event'].keys())+1
                    # print(len(item['imgurl']),item['event'])
                    # print('___________________________________________')
                # else:
                #     print(len(item['imgurl']),item['title'])


                items[utils.get_id(item['url'])]=item

    # 重复的事件去除
    events={}
    for item in items.values():
        if item['event'] and '事件' in item['event']:
            p='<p style="background: yellow;display: block;width: fit-content;margin: 0;margin-top: 12px;font-size: 12px;">' +item['keyword']+'</p>'

            #显示抽取的信息
            item['html']="<br>".join(['#'+k+':'+v for k,v in item['event'].items()])+item['html']

            item['html']='<details><summary><div style="display: inline-flex;align-items: baseline;"><p>'+item['title']+p+'</p></div></summary>'+ item['html']+ '</details>'
            
            events[item['event']['事件']]=item
    
    # 按照公司\产品\人物\技术  来整理信息
    organizations={}
    for e in events.values():

        key='公司/组织/机构'
        if e['event'] and not key in e['event']:
            key='技术'
        if e['event'] and not key in e['event']:
            key='产品'
        if e['event'] and not key in e['event']:
            key='人物'

        if e['event'] and key in e['event']:
            if not e['event'][key] in organizations:
                organizations[e['event'][key]]=[]
            organizations[e['event'][key]].append(e)

    # 公司信息排序
    rank_res=[]
    for k,vs in organizations.items():
        data=utils.rank(vs,'score')
        html="<card><h4>"+k+"</h4>"+"".join([d['html'] for d in data])+"</card>"
        rank_res.append({
            "data":data,
            "html":html,
            "organization":k,
            "score":len(vs)
        })

    result=utils.rank(rank_res,'score')

    d = utils.get_date_str(today).split(" ")[0]

    result='''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>'''+d+'''</title>
</head>
<body>'''+"".join([r['html'] for r in result])+'''</body>

<script> 
let cards=[...document.querySelectorAll('card')]
    
for(let card of cards){
card.style='display:none'
let t=card.querySelector('h4').innerText;  
    card.querySelector('h4').remove();
    card.innerHTML=`<details><summary><h4></h4><p style="font-size: 12px;
    background: #ffffcd;
    display: block;
    width: fit-content;
    padding: 4px;">${t}</p></summary>${card.innerHTML}</details>`
    
Array.from(card.querySelectorAll('img'),im=>{
  let title= im.parentElement.innerText.split('\\n')[0];
    if(!card.querySelector('summary h4').innerText)card.querySelector('summary h4').innerText=title
    let i=new Image();i.src=im.src;
    i.style='width: fit-content;'
    card.querySelector('summary').appendChild(i)
    card.style=`display: flex;
    flex-direction: column;
    background-color: #eee;
    padding: 18px;margin: 12px 0;`
})
}</script>
</html>'''

    
    utils.write_file(result,filepath+"/"+d+"_extract.html")      
     

    
#抽取人物、公司、事件、观点
#同时去除，信息量不足的资讯
def extract(title,text,lang='zh'):

    if lang=='zh':
        items=ie(text)
    else:
        items=ie_en(text)

    result={}

    for item in items:
        for key,values in item.items():
            if lang=='en':
                key=[k for k,v in schema.items() if v==key][0]
            
            vals={}
            for val in values:
                vals[val['text']]=val['probability']

            # 保留最长的
            vals=[{
                "value":v,
                "score":len(v)
            } for v in vals.keys()]
            vals=utils.rank(vals)
            #print('- ',vals)
            #print()
            result[key]=vals[0]['value']
            print(key,result[key])
        print('_________________________')
    #if '事件' in result and len(result.keys())>1:
    #事件没有，可以用title兜底
    if len([x for x in result.keys() if x == '事件'])==0:
        result['事件']=title

    if len(result.keys())>1:
        return result

    
    
start('../data')
# start('./data,-1)