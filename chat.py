import json
import os
import openai
import requests
def chat(messages):
    #print(messages)
    
    openai.api_key = "1111"
    openai.api_base="http://localhost:8080"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature= 0.7,
        stream=True
    )
    for word in response:
        # print(word['choices'][0]['delta']['content'])
        # print("*")
        yield word['choices'][0]['delta']['content']
    #return response['choices'][0]['message']['content']
    
    # url = "http://localhost:8080/v1/chat/completions"
    # messages = {"model": "gpt-3.5-turbo","messages": messages,"temperature": 0.7}
    # json_msg = json.dumps(messages)
    # headers = {'Content-Type': 'application/json'}
    # response = requests.post(url,data=json_msg,headers=headers)
    # dict = json.loads(response.text)
    # return dict['choices'][0]['text']

    pass

if __name__ == "__main__":
    # chat([{"role": "user", "content": "Say this is a test!"}])
    chat_generator=chat([{"role": "user", "content": "Say this is a test!"}])
    for word in chat_generator:
        print(word)
    
# curl http://localhost:8080/v1/chat/completions -H "Content-Type: application/json" -d '{
#   "model": "ggml-koala-7b-model-q4_0-r2.bin",
#   "messages": [{"role": "user", "content": "Say this is a test!"}],
#   "temperature": 0.7
# }'