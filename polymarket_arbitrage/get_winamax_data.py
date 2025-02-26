import requests
import json

def wina_data(url):
    headers = {
        'User-Agent': 'Mozilla/6.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
    }
    response = requests.get(url, headers=headers)
    html = response.text
    try:
        split1 = html.split("var PRELOADED_STATE = ")[1]
        split2 = split1.split(";</script>")[0]
        data = json.loads(split2)
        return data
    except:
        print(html)
        exit()
