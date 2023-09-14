import os
import requests
from typing import List, Dict
import json
import openai
# curl -L -X GET --compressed 'https://geoapi.qweather.com/v2/city/lookup?location=Shanghai,China&key=8888c47d5b624f0fa1974570dd31efc8'

todo_list = ""
def lookup_location_id(location: str):
    url = 'https://geoapi.qweather.com/v2/city/lookup'
    params = {
        'location': location,
        'key': '8888c47d5b624f0fa1974570dd31efc8'
    }
    response = requests.get(url,params=params)
    #if response.status_code != 200:
    #    return ""
    dict = json.loads(response.text)
    if dict['code']!= "200":
        #print(dict['code'])
        return ""
    return dict['location'][0]['id']

def get_current_weather(location: str):
    id = lookup_location_id(location)
    if id == "":
        return f"can't find {location}."
    url = 'https://devapi.qweather.com/v7/weather/now'
    params = {
        'location': id,
        'key': '8888c47d5b624f0fa1974570dd31efc8'
    }
    response = requests.get(url,params=params)
    if response.status_code != 200:
        return f"can't get the weather of {location}."
    dict = json.loads(response.text)['now']
    return f"Temperature: {dict['feelsLike']} Description:{dict['text']} Humidity: {dict['humidity']}"

def add_todo(todo: str):
    global todo_list
    todo_list +=f"- {todo}\n"
    return todo_list

def function_calling(messages: List[Dict]):
# ...
# Send the conversation and available functions to GPT
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "A city, province or counrty,or none. e.g. ShangHai, Beijing, China, US. No form of \"Shanghai, China\"",
                    },
                },
                "required": ["location"],
            },
        },
        {
            "name": "add_todo",
            "description": "Add something on a TODO-list. Add a todo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "todo": {
                        "type": "string",
                        "description": "something added to the TODO-list, e.g. walk, swim",
                    }
                },
                "required": ["todo"],
            },
        }
    ]
    openai.api_key="1111"
    openai.api_base="http://166.111.80.169:8080"
    response = openai.ChatCompletion.create(
        model="ggml-openllama.bin",
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    try:   
        func = response["choices"][0]["message"]["function_call"]
        if func["function"] == "add_todo":
            arg = json.loads(func["arguments"])
            return add_todo(arg["todo"])
        elif func["function"] == "get_current_weather":
            arg = json.loads(func["arguments"])
            return get_current_weather(arg["location"])
        else:
            return None
    except:
        return f"no function found!response:{response}"

if __name__ == "__main__":
    messages = [{"role": "user", "content": "What's the weather like in Beijing"}]
    response = function_calling(messages)
    print(response)

    messages = [{"role": "user", "content": "Add a todo: do math homework"}]
    response = function_calling(messages)
    print(response)