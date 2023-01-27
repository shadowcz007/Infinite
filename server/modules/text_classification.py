from paddlenlp import Taskflow

model=None

def init():
    global model
    model = Taskflow("zero_shot_text_classification", 
    schema=["介绍类信息","主观评价类信息", "研究结论类信息","展望未来类信息","需求洞察类信息"])


def start(text):
    global model
    if model==None:
        init()
    res=model(text.split('\n'))
    keywords={}
    texts=[]
    for r in res:
        if len(r['predictions'])>0 and r['predictions'][0]['score']>0.99:
            print(r['predictions'])
            print(r['text_a'])
            texts.append(r['text_a'])
            print('-----------------')
            if not r['predictions'][0]['label'] in keywords:
                keywords[r['predictions'][0]['label']]=0
            keywords[r['predictions'][0]['label']]+=1

    print(keywords)
    print('======')
    print("\n".join(texts))
    return {
        "keywords":keywords,
        "text":"\n".join(texts),
        "res":res
    }




def parse_args():
    import argparse
    description = "提取文章里的核心信息..."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-t", "--text", type=str, default='', help="文章文本")
    
    return parser.parse_args()



if __name__ == "__main__":
    
    args = parse_args()
    start(args.text)
