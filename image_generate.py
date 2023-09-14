import os
import requests
import json

def image_generate(content: str):
    url = "https://api.openai.com/v1/images/generations"
    headers = "Content-Type: application/json"
    params = {
        "prompt":content,
        "size":"256x256"
    }
    response = requests.get(url, headers=headers, params=params)
    dict = json.loads(response.text)
    return dict['data'][0]['url']

if __name__ == "__main__":
    image_generate('A cute baby sea otter')
