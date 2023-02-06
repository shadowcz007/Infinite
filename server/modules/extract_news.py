from paddlenlp import Taskflow
 

try:
    from . import utils
except:
    import utils

try:
    from . import translate
except:
    import translate

FILE_PATH='../data'

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
# ie_en = Taskflow('information_extraction', schema=schema_en, model='uie-base-en')
# similarity = Taskflow("text_similarity")
# question_generator = Taskflow("question_generation")



def create_html(data):
    html='''<div score="'''+str(data['score'])+'''" class="score" style="display: flex;
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

 

def start(filepath='./data',today=0):
    global FILE_PATH
    if filepath:
        FILE_PATH=filepath

    items={}
    jsons=utils.read_dir_json_byday(FILE_PATH,today)

   

    #翻译
    for jsons_data in jsons:
        data=jsons_data['data']
        if isinstance(data, dict):
            for item in data['data']:
                if isinstance(item, dict) and not 'is_zh' in item:
                    item['text']=(",".join([item['title'],item['snippet'],item['keyword']])).lower()
                    is_zh=utils.is_contain_zh(item['text'])
                    #翻译
                    if is_zh==False:
                        try:
                            item['text']=translate.start(item['text'])
                            item['title']=translate.start(item['title'])
                            is_zh=True
                        except:
                            print(is_zh,'translate:',item['title'])
                    item['is_zh']=is_zh
            utils.write_json(data,jsons_data['filepath'])

 
    for jsons_data in jsons:
        data=jsons_data['data']
        # print(data)
        if isinstance(data, dict):

            for item in data['data']:
                if isinstance(item, dict) and not 'event' in item:

                    #item['text']=(",".join([item['title'],item['snippet'],item['keyword']])).lower()
                    is_zh=item['is_zh']

                    # print('is_zh:',is_zh,item['text'])
                    if is_zh==True:
                        item['event'],mkey=extract(item['title'],item['text'],'zh')
                    
                    if 'event' in item and item['event'] and mkey:
                        # 如果有提取出信息才能进一步
                        item['score']+=len(item['event'].keys())+1
                        
                        item['event']['url']=item['url']
                    
                        print(item['score'],item['title'])

                        item['html']=create_html(item)

                        items[utils.get_id(item['url'])]=item
            
            # for item in data['data']:
            #     print(item['event'])
            # print(jsons_data['filepath'])
            utils.write_json(data,jsons_data['filepath'])
                

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
        # if e['event'] and not key in e['event']:
        #     key='人物'
        # if e['event'] and not key in e['event']:
        #     key='公司/组织/机构'

        if e['event'] and key in e['event']:
            if not e['event'][key] in organizations:
                organizations[e['event'][key]]=[]
            organizations[e['event'][key]].append(e)
        
        # else:
        #     print(e['score'],e['title'])



    # 公司信息排序
    rank_res=[]
    for k,vs in organizations.items():
        data=utils.rank(vs,'score')
        qs=[{
            "question":d['event']['问题'],
            "url":d['event']['url']
        } for d in data if '问题' in d['event']]
        # print(qs)
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

<style>
    .for_ai {
        font-size: 18px;
        font-weight: 800;
        color: cornflowerblue;
        margin: 32px 0;
    }
    
    details {
        background: #ededed;
    }
</style>
<script>
let companies = {};

let cards = [...document.querySelectorAll('card')]
    let n = 10 + eval(Array.from(document.querySelectorAll('.score'), s => ~~s.getAttribute('score')).join('+')) / document.querySelectorAll('.score').length;
    console.log(n)

    if (localStorage.getItem(document.title)) {
        n = parseInt(localStorage.getItem(document.title))
    };
    localStorage.setItem(document.title, n);
    let inputN = document.createElement('input');
    inputN.type = 'number';
    inputN.value = n;
    inputN.addEventListener('change', e => {
        localStorage.setItem(document.title, parseInt(inputN.value));
        window.location.reload();
    });

    document.body.insertAdjacentElement('afterbegin', inputN);


    for (let card of cards) {
        Array.from(card.querySelectorAll('.score'), d => {
            if (d.getAttribute('score') <= n) d.parentElement.remove()
        });

        if (card.querySelectorAll('details').length == 0) card.remove()
    }
    cards = [...document.querySelectorAll('card')];
    console.log(cards.length)

    let cardsNum = document.createElement('div');
    cardsNum.innerText = cards.length;
    document.body.insertAdjacentElement('afterbegin', cardsNum);


    for (let card of cards) {
        card.querySelector('.for_ai').innerText = card.querySelector('.for_ai').innerHTML.split('<br>')[0]
         // 提取公司
        Array.from(card.querySelectorAll('details'), details => Array.from(details.innerHTML.split('<br>'), d => {
                if (d.match('#公司/组织/机构')) {
                    if (!companies[d.split('#公司/组织/机构:')[1]]) companies[d.split('#公司/组织/机构:')[1]] = 0;
                    return companies[d.split('#公司/组织/机构:')[1]]++;
                }
            }))
            // console.log(Object.keys(companies))
       
            // console.log(card.querySelector('.for_ai').innerHTML.split('<br>'))
        Array.from(card.children, (c, i) => {
            if (i > 0) {

                c.querySelector('summary').children[0].setAttribute('title', c.querySelector('summary').children[0].children[0].innerText)
                c.querySelector('a').href = c.querySelector('a').href + '?knowledgeTags=' + card.querySelector('.for_ai').innerText + '&knowledgeReply=' + c.querySelector('summary').children[0].children[0].innerText;
            
                c.querySelector('summary').children[0].children[0].innerHTML = `
                <div contenteditable>${c.querySelector('summary').children[0].children[0].innerText} </div>
                <button class='run' style="cursor: pointer;">AIGC</button> `;
                
                let btn = document.createElement('button');
                    btn.innerText = 'delete'
                    btn.addEventListener('click', e => {
                        c.remove()
                    });
                c.querySelector('summary').children[0].children[0].appendChild(btn);

                c.querySelector('.run').addEventListener('click', e => {
                    console.log(e.target.parentElement.parentElement.getAttribute('title'), e.target.previousElementSibling.innerText)
                    createImage(div, e.target.previousElementSibling.innerText, e.target.parentElement.parentElement.getAttribute('title'), c.querySelector('a').href);
                })
                
            }
        })

        let btn = document.createElement('button');
            btn.innerText = 'delete'
            btn.addEventListener('click', e => {
                card.remove()
            });
        card.appendChild(btn);

    };

     // 提取公司
    companies = Array.from(Array.from(Object.keys(companies), key => {
        return {
            count: companies[key],
            key: key
        }
    }).sort((a, b) => b.count - a.count), ks => ks.key)
    document.body.insertAdjacentHTML('afterbegin', `<div style="margin:14px">公司:<br>${companies.join('<br>')}<br></div>`)
    
    
    let div = document.createElement('div');
    // div.setAttribute('contenteditable', true)
    div.style = `position: fixed;
    top: 0;outline:1px solid gray;
    right: 0; display: flex;flex-wrap: wrap;max-height: 100vh;
    overflow: scroll; width:40%;`
    document.body.appendChild(div);

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

        // 导流到微信公众号 mixlab http://weixin.qq.com/r/Skzbw9PEv47ArZeg9xlY
        // shadow实验室 http://weixin.qq.com/r/IUNpcWnE2zSkrS0S9xYz
        qrcode.makeCode('http://weixin.qq.com/r/IUNpcWnE2zSkrS0S9xYz');

        const c = (i, imgUrl, title, qrUrl) => `<div><section style="border: 1px solid #dedede;background:#eee" id="s${i}"><div style="width:300px;margin: 24px;" >
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
        for (let index = 0; index < 20; index++) {
            let r1 = (await create(questions)).data[0];
            div.innerHTML += c(index, r1, title, im.children[1].src);
        }

    }
    window.results = {};
    try {
        window.results = JSON.parse(localStorage.getItem('_res')) || {}
    } catch (error) {
        window.results = {};
    }

    function getImage(id) {
        let t = div.querySelector('#' + id).querySelector('.commit').innerText
        div.querySelector('#' + id).querySelector('.commit').innerHTML = t;
        window.results[t] = t;
        localStorage.setItem('_res', JSON.stringify(window.results))

        html2canvas(div.querySelector('#' + id), {
            backgroundColor: '#ffffff',
            scale: window.devicePixelRatio * 2
        }).then(function(canvas) {
            div.innerHTML = ''
            div.appendChild(canvas);
        });
    }

    let b = document.createElement('button')
    b.style = `top: 0px;
    right: 0px;
    position: fixed;
    z-index: 999;
    width: 44px;
    height: 44px;
    background: red;`
    b.innerText = '导出'
    document.body.appendChild(b)

    b.addEventListener('click', e => {
        let cards = document.querySelectorAll('card');
        let res = '';
        for (const card of cards) {
            let tag = card.querySelector('h4').innerText,
                texts = Array.from(card.children, c => {
                    if (c.querySelector('summary')) {

                        let title = c.querySelector('summary').children[0].title;
                        let url = c.querySelector('a').href;
                        return `· [${title}](${url})`
                    }

                }).filter(f => f).join(' \\n\\n ');
            res += '`' + tag + '` \\n\\n ' + texts + '\\n\\n';
        }

        copyToClickBoard(res)
    })

    function copyToClickBoard(content) {

        navigator.clipboard.writeText(content)
            .then(() => {
                console.log("Text copied to clipboard...")
                b.style.display = 'flex';
                Array.from(document.querySelectorAll('button'), r => r.style.display = 'inline-block');
            })
            .catch(err => {
                console.log('Something went wrong', err);
                b.style.display = 'flex';
                Array.from(document.querySelectorAll('button'), r => r.style.display = 'inline-block');
            })

    }

    let b2 = document.createElement('button')
    b2.style = `top:88px;
    right: 0px;
    position: fixed;
    z-index: 999;
    width: 44px;
    height: 44px;
    background: red;`
    b2.innerText = '洞察'
    document.body.appendChild(b2)

    b2.addEventListener('click', e => {
        copyRes()
    })

    function copyRes() {
        navigator.clipboard.writeText(Object.keys(window.results).join('\\n'))
            .then(() => {
                console.log("Text copied to clipboard...")

            })
            .catch(err => {
                console.log('Something went wrong', err);

            })
    }
</script>
<script src="https://cdn.bootcdn.net/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
<script src="https://cdn.bootcdn.net/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

</html>'''

    
    utils.write_file(result,FILE_PATH+"/"+d+"_extract.html")
    update_index()
    utils.print_info('完成',FILE_PATH+"/"+d+"_extract.html")

     

    
#抽取人物、公司、事件、观点
#同时去除，信息量不足的资讯
def extract(title,text,lang='zh'):
    items=[]
    if lang=='zh':
        items=ie(text)
    # else:
    #     items=ie_en(text)

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

def update_index():
    global FILE_PATH
    #html
    htmls=[]
    for i in range(-7,1):
        try:
            e_html=utils.read_dir_extract_html_byday(FILE_PATH,i)
            if e_html:
                htmls.append('data/'+e_html['filename'])
        except:
            print(i)
    utils.write_json(htmls,FILE_PATH+'/index_extract_html.json')

def parse_args():
    import argparse
    description = "爬取每日资讯..."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-f", "--filepath", type=str, default='../data', help="传入地址")
    
    return parser.parse_args()
  

if __name__ == "__main__":
    
    args = parse_args()
    
    start(args.filepath)
