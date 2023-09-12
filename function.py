import os
import requests
from typing import List, Dict
import json
import openai
# curl -L -X GET --compressed 'https://geoapi.qweather.com/v2/city/lookup?location=beij&key=8888c47d5b624f0fa1974570dd31efc8'

todo_list = ""
def lookup_location_id(location: str):
    url = 'https://geoapi.qweather.com/v2/city/lookup'
    params = {
        'location': location,
        'key': '8888c47d5b624f0fa1974570dd31efc8'
    }
    response = requests.get(url,params=params)
    dict = json.loads(response.text)
    #print(dict['location'][0]['id'])
    return dict['location'][0]['id']

def get_current_weather(location: str):
    id = lookup_location_id(location)
    url = 'https://devapi.qweather.com/v7/weather/now'
    params = {
        'location': id,
        'key': '8888c47d5b624f0fa1974570dd31efc8'
    }
    response = requests.get(url,params=params)
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
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                },
                "required": ["location"],
            },
        },
        {
            "name": "add_todo",
            "description": "Add something on a TODO-list",
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
    openai.api_base="http://localhost:8080"
    response = openai.ChatCompletion.create(
        model="ggml-openllama.bin",
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    func = response["choices"][0]["message"]["function_call"]
    #print(func)
    if func["function"] == "add_todo":
        arg = json.loads(func["arguments"])
        return add_todo(arg["todo"])
    elif func["function"] == "get_current_weather":
        arg = json.loads(func["arguments"])
        return get_current_weather(arg["location"])
    else:
        return None

if __name__ == "__main__":
    messages = [{"role": "user", "content": "What's the weather like in Beijing?"}]
    response = function_calling(messages)
    print(response)

    messages = [{"role": "user", "content": "Add a todo: walk"}]
    response = function_calling(messages)
    print(response)