import os
import requests
import json

def image_generate(content: str):
    url = "http://166.111.80.169:8080/v1/images/generations"
    headers = {"Content-Type": "application/json"}
    params = {
        "prompt":content,
        "size":"256x256"
    }
    response = requests.post(url, headers=headers, data=json.dumps(params))
    dict = json.loads(response.text)
    return dict['data'][0]['url']

if __name__ == "__main__":
    image_generate('A cute baby sea otter')
