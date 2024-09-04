import requests

def get(l,w,url='http://localhost:70/fish'):
    headers = {
        'accept': 'application/json',
    }

    params = {
        'length': '100',
        'weight': '50',
    }

    response = requests.get(url, params=params, headers=headers).text
    json = eval(response)

    print(json)

    return json["prediction"]
