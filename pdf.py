import os
import re
import requests
import json

def generate_text(prompt):
    #print(prompt)
    url = "http://localhost:8080/v1/completions"
    messages = {"model": "gpt-3.5-turbo","prompt": prompt,"temperature": 0.7}
    json_msg = json.dumps(messages)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url,data=json_msg,headers=headers)
    dict = json.loads(response.text)
    return dict['choices'][0]['text']

def generate_answer(current_file_text: str, content: str):
    prompt = f"I am reading the passage:\n{current_file_text}.According to the passage, the answer of '{content}' is"
    return prompt

def generate_summary(current_file_text: str):
    prompt = f"I am reading the passage:\n{current_file_text}\nTo summarize it in less than three sentence,"
    return prompt

if __name__ == "__main__":
    prompt = generate_answer("Tang Sanzang is a Buddhist monk who is a reincarnation of Golden Cicada, a disciple of the Buddha.Sun Wukong is a monkey born from a stone who acquires supernatural powers through Taoist practices.Jenny is a math teacher", "Who is Jenny?")
    #prompt = generate_summary("Tang Sanzang is a Buddhist monk who is a reincarnation of Golden Cicada, a disciple of the Buddha.Sun Wukong is a monkey born from a stone who acquires supernatural powers through Taoist practices.")
    print(generate_text(prompt))