
import requests, json,datetime
import utils

token = 'secret_8X2Ryn7H8qsmTQ4c1gEQeP6A6Mw4QZgErwh7SwKKewO'
database_id = '9146862723b4461888c56a00182d4a53'

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}



def read_database(database_id, headers):
    read_url = f"https://api.notion.com/v1/databases/{database_id}/query"

    res = requests.request("POST", read_url, headers=headers)
    data = res.json()
    # print(res.status_code)
    # print(res.text)
    json_data=[]
    for r in data['results']:
        d=r['properties']
        tags=[n['name'] for n in d['Tag']['multi_select']]
        url=d['URL']['url']
        description=[t['plain_text'] for t in d['Description']['rich_text']]
        name=[t['plain_text'] for t in d['Name']['title']]
        json_data.append({
            "name":name,"description":description,"url":url,"tags":tags
        })
            
    with open('./aigc_tool_data.json', 'w', encoding='utf8') as f:
        json.dump(json_data, f, ensure_ascii=False)


def date_iso(t):
    print('date_iso',t)
    # import datetime
    return datetime.datetime.fromtimestamp(t/1000).isoformat()


# 'summarizer', 'summarizer_zh', 'title', 'text', 'url', 'host_name', 'keyword', 'time', 'title_zh', 'question'
def create_page(database_id, headers,data):

    create_url = 'https://api.notion.com/v1/pages'
   
    tags=[{"name":x} for x in data['tag'].split(",")]
    #print( data['tag'],tags)
    
    new_page_data = {
        "parent": { "database_id": database_id },
        "properties": {
            "Name": {
                "title": [
                {
                    "type": "text",
                    "text": {
                    "content": data['title'],
                    #"link":data['url']
                    }
                }
                ]
            },
            "Description": {
                "rich_text": [
                {
                    "type": "text",
                    "text": {
                    "content": data['description']
                    }
                }
                ]
            },
           "Tag": {
                "multi_select": tags
            },
            
            "URL": {
                "url": data['url']
            }
 
        }
    }
    
    
    data = json.dumps(new_page_data)
    # print(new_page_data)

    res = requests.request("POST", create_url, headers=headers, data=data)

    print(res.status_code)
    print(res.text)


read_database(database_id, headers)

# json_data=utils.load_json('./data.json')
# for data in json_data:
#     create_page(database_id, headers,data)