import requests


auth_token = 'secret_8X2Ryn7H8qsmTQ4c1gEQeP6A6Mw4QZgErwh7SwKKewO'
parent_page_id = '9146862723b4461888c56a00182d4a53'




url = 'http://example.com'

api_url = 'https://api.notion.com/v3/create_page'

headers = {
    'Authorization': 'Bearer ' + auth_token,
    'Content-Type': 'application/json',
}

data = {
    'parent_page_id': parent_page_id,
    'type': 'url',
    'properties': {
        'url': {
            'title': [
                {
                    'text': {
                        'content': url
                    }
                }
            ]
        }
    }
}

response = requests.post(api_url, headers=headers, json=data)

if response.status_code == 201:
    print('Success')
else:
    print('Failed')