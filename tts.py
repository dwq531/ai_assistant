import requests
import os
import json


def text2audio(content: str):
    url = "http://166.111.80.169:8080/tts"
    headers = {"Content-Type": "application/json"}
    data = {"model": "en-us-blizzard_lessac-medium.onnx", "input": content}
    data_json = json.dumps(data)
    # 获取已有的音频文件数量
    audio_folder = ".\\audio"
    existing_audio_files = [f for f in os.listdir(audio_folder) if f.startswith("response") and f.endswith(".wav")]
    audio_count = len(existing_audio_files)

    # 生成新的文件名
    audio_file_name = f"response{audio_count + 1}.wav"
    audio_file_path = os.path.join(audio_folder, audio_file_name)
    response = requests.post(url, headers=headers, data=data_json)
    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(response.content)
    #print(response.content)
    #print("音频文件已生成")
    return audio_file_path


if __name__ == "__main__":
    text2audio(
        "I am an AI language model developed by OpenAI. I am designed to assist with language tasks, such as answering questions and generating text. I am programmed to understand natural language and respond appropriately. My purpose is to improve the quality of language on various platforms, including social media and messaging apps."
    )
