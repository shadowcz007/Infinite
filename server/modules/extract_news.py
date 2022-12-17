from paddlenlp import Taskflow

import os

import utils

schema={
    '人物':'person',
    '公司':'organization',
    '事件':'event'
}

schema_zh = [x for x in schema.keys()]
schema_en=[x for x in schema.values()]
print(schema_zh,'_',schema_en)
ie = Taskflow('information_extraction', schema=schema_zh)
ie_en = Taskflow('information_extraction', schema=schema_en, model='uie-base-en')
# similarity = Taskflow("text_similarity")



def start(filepath='./data',d=None):
    

    if d==None:
        d = utils.get_date_str().split(" ")[0]

    items={}
    for filename in [x[2] for x in os.walk(filepath)][0]:
        if d+'.json' in filename:
            data=utils.load_json(filepath+'/'+filename)
            for item in data['data']:
                if isinstance(item, dict):
                    # print(item.keys())
                    item['text']=(",".join([item['title'],item['snippet'],item['keyword']])).lower()

                    #print('* ',item['title'])
                    item['event']=extract(item['text'],'zh' if utils.is_contain_zh(item['text']) else 'en')
                    if item['event']:
                        item['score']+=len(item['event'].keys())+1
                       
                        # html=''
                        # for ek,ev in item['event'].items():
                        #     html+='#'+ek+':'+ev+'<br>'
                        # item['html']='<p>'+html+'</p>'+item['html']
                        print(item['event'])
                        print('___________________________________________')

                    items[utils.get_id(item['url'])]=item

    # 重复的事件去除
    events={}
    for item in items.values():
        if item['event'] and '事件' in item['event']:
            p='<p style="background: yellow;display: block;width: fit-content;margin: 0;margin-top: 12px;font-size: 12px;">' +item['keyword']+'</p>'
            item['html']='<details><summary><div style="display: inline-flex;align-items: baseline;"><p>'+item['title']+p+'</p></div></summary>'+ item['html']+ '</details>'
            events[item['event']['事件']]=item
    
    # 按照公司来整理信息
    organizations={}
    for e in events.values():
        if e['event'] and '公司' in e['event']:
            if not e['event']['公司'] in organizations:
                organizations[e['event']['公司']]=[]
            organizations[e['event']['公司']].append(e)

    # 公司信息排序
    rank_res=[]
    for k,vs in organizations.items():
        data=utils.rank(vs,'score')
        html="<h4>"+k+"</h4>"+"".join([d['html'] for d in data])+""
        rank_res.append({
            "data":data,
            "html":html,
            "organization":k,
            "score":len(vs)
        })

    result=utils.rank(rank_res,'score')
    result="".join([r['html'] for r in result])


    utils.write_file(result,filepath+"/"+d+"_extract.html")      
     
                    

    
#抽取人物、公司、事件
#同时去除，信息量不足的资讯
def extract(text,lang='zh'):

    if lang=='zh':
        items=ie(text)
    else:
        items=ie_en(text)

    result={}

    for item in items:
        for key,values in item.items():
            if lang=='en':
                key=[k for k,v in schema.items() if v==key][0]
            #print('#',key)
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
    if '事件' in result and len(result.keys())>1:
        return result

    
    
start('../data')
# start('./data,'2022-12-15')