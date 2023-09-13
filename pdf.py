import os
import re
import requests
import json
import openai

def generate_text(prompt):
    openai.api_key = "1111"
    openai.api_base="http://localhost:8080"
    
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        temperature= 0.7,
        stream=True
    )
    for word in response:
        #print(word)
        if "text" in word['choices'][0]:
            yield word['choices'][0]['text']


def generate_answer(current_file_text: str, content: str):
    prompt = f"I am reading the passage:\n{current_file_text}.According to the passage, the answer of '{content}' is"
    return prompt

def generate_summary(current_file_text: str):
    prompt = f"I am reading the passage:\n{current_file_text}\nTo summarize it in less than three sentence,"
    return prompt

if __name__ == "__main__":
    prompt = generate_answer("Tang Sanzang is a Buddhist monk who is a reincarnation of Golden Cicada, a disciple of the Buddha.Sun Wukong is a monkey born from a stone who acquires supernatural powers through Taoist practices.Jenny is a math teacher", "Who is Tang Sanzang?")
    #prompt = generate_summary("Tang Sanzang is a Buddhist monk who is a reincarnation of Golden Cicada, a disciple of the Buddha.Sun Wukong is a monkey born from a stone who acquires supernatural powers through Taoist practices.")
    chat_generator=generate_text(prompt)
    for word in chat_generator:
        print(word)