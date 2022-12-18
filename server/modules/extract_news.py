from paddlenlp import Taskflow


try:
    from . import utils
except:
    import utils

try:
    from . import translate
except:
    import translate

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
question_generator = Taskflow("question_generation")


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
                is_zh=utils.is_contain_zh(item['text'])

                item['event'],mkey=extract(item['title'],item['text'],'zh' if is_zh else 'en')
                

                if item['event'] and len(item['imgurl'])>0:
                    # 如果有提取出信息才能进一步  && 有封面图的

                    item['score']+=len(item['event'].keys())+1
                    
                    #翻译
                    if is_zh==False:
                        item['text']=translate.start(item['text'])

                    #问题生成
                    if mkey:
                        r=question_generator([{
                        "context":item['text'],
                        "answer":item['event'][mkey]
                        }])
                        item['event']['问题']=r[0]
                        item['event']['答案']=mkey+'_'+item['event'][mkey]
                        item['event']['url']=item['url']
                        # print(r)
                        # print({
                        #     "context":item['text'],
                        #     "answer":mkey+'_'+item['event'][mkey]
                        # })
                        # print('________________')


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
        key='技术'
        if e['event'] and not key in e['event']:
            key='产品'
        if e['event'] and not key in e['event']:
            key='人物'
        if e['event'] and not key in e['event']:
            key='公司/组织/机构'

        if e['event'] and key in e['event']:
            if not e['event'][key] in organizations:
                organizations[e['event'][key]]=[]
            organizations[e['event'][key]].append(e)

    # 公司信息排序
    rank_res=[]
    for k,vs in organizations.items():
        data=utils.rank(vs,'score')
        qs=[{
            "question":d['event']['问题'],
            "url":d['event']['url']
        } for d in data if '问题' in d['event']]
        print(qs)
        html="<card><h4 class='for_ai' urls='"+",".join([q['url'] for q in qs])+"' questions='"+",".join([q['question'] for q in qs])+"' title='"+k+"'>"+k+"<br>"+",".join([q['question'] for q in qs])+"</h4>"+"".join([d['html'] for d in data])+"</card>"
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
    let cards = [...document.querySelectorAll('card')]
    let div = document.createElement('div');
    // div.setAttribute('contenteditable', true)
    div.style = `position: fixed;
    top: 0;
    right: 0; display: flex;flex-wrap: wrap;height: 100vh;
    overflow: scroll;
    background-color: #eee;width:60%;`
    document.body.appendChild(div);
    for (let card of cards) {
        card.style = 'display:none'
        let t = card.querySelector('h4').innerText;
        let urls = card.querySelector('h4').getAttribute('urls'),
            title = card.querySelector('h4').getAttribute('title'),
            questions = card.querySelector('h4').getAttribute('questions');
        card.querySelector('h4').remove();
        card.innerHTML = `<details><summary><h4></h4><p style="font-size: 12px;
    background: #ffffcd;
    display: block;
    width: fit-content;
    padding: 4px;
    cursor: pointer;">${t}</p></summary>${card.innerHTML}</details>`;

        card.querySelector('summary p').addEventListener('click', e => {
            createImage(div, '' + questions, card.querySelector('summary h4').innerText, urls.split(',')[0]);
        })


        Array.from(card.querySelectorAll('img'), im => {
            let title = im.parentElement.innerText.split('\\n')[0];
            if (!card.querySelector('summary h4').innerText) card.querySelector('summary h4').innerText = title
            let i = new Image();
            i.src = im.src;
            i.style = 'width: fit-content;'
            card.querySelector('summary').appendChild(i)
            card.style = `display: flex;
    flex-direction: column;
    background-color: #eee;
    padding: 18px;margin: 12px 0;`
        })
    };


    function create(t) {
        return fetch("http://127.0.0.1:7860/run/infer_text2img_for_auto", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    data: [
                        t,
                    ]
                })
            })
            .then(r => r.json())
    }
    async function createImage(div, questions, title, urls) {
        let im = document.createElement('div')
        let qrcode = new QRCode(im);
        qrcode.clear();
        // 导流到微信公众号
        qrcode.makeCode('http://weixin.qq.com/r/Skzbw9PEv47ArZeg9xlY');

        const c = (i, imgUrl, title, qrUrl) => `<div><section style="border: 1px solid #dedede;" id="s${i}"><div style="width:300px;margin: 24px;" >
            <img src="${imgUrl}" style="width:300px"/>
            <p style="display: flex;
    height: 56px;font-size: 15px;
    font-weight: 800;
    justify-content: space-around;" contenteditable >${title}<br> <img src="${qrUrl}" /></p><p style="font-size: 12px;
    padding-top: 6px;" contenteditable class="commit">评论：</p>
    <p style="font-size: 12px;font-weight:300" contenteditable>${urls}</p>
            </div></section> <button onclick='getImage("s${i}")'>OK</button></div>`

        r = (await create(questions)).data[0];
        div.innerHTML = c(0, r, title, im.children[1].src);
        r1 = (await create(questions)).data[0];
        div.innerHTML += c(1, r1, title, im.children[1].src);
        r2 = (await create(questions)).data[0];
        div.innerHTML += c(2, r2, title, im.children[1].src);
        r3 = (await create(questions)).data[0];
        div.innerHTML += c(3, r3, title, im.children[1].src);
        r4 = (await create(questions)).data[0];
        div.innerHTML += c(4, r4, title, im.children[1].src);
        r5 = (await create(questions)).data[0];
        div.innerHTML += c(5, r5, title, im.children[1].src);
        r6 = (await create(questions)).data[0];
        div.innerHTML += c(6, r6, title, im.children[1].src);

    }

    function getImage(id) {
        div.querySelector('#' + id).querySelector('.commit').innerHTML = div.querySelector('#' + id).querySelector('.commit').innerText;
        html2canvas(div.querySelector('#' + id), {
            backgroundColor: '#ffffff',
            scale: window.devicePixelRatio * 2
        }).then(function(canvas) {
            div.innerHTML = ''
            div.appendChild(canvas);
        });
    }
</script>
<script src="https://cdn.bootcdn.net/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
<script src="https://cdn.bootcdn.net/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

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
            #print(key,result[key])
        #print('_________________________')
    #if '事件' in result and len(result.keys())>1:
    #事件没有，可以用title兜底
    if len([x for x in result.keys() if x == '事件'])==0:
        result['事件']=title

    # 优先显示的，用来分类
    mkey='技术'
    for key,v in result.items():
        if not mkey in result:
            mkey='产品'
        if not mkey in result:
            mkey='人物'
        if not mkey in result:
            mkey='公司/组织/机构'
        if not mkey in result:
            mkey=None
        

    if len(result.keys())>1:
        return result,mkey
    else:
        return None,None

    
    
start('../data')
# start('./data,-1)