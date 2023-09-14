import requests
import os


def text2audio(content: str):
    # 使用API将文本转换为音频
    api_url = "http://166.111.80.169:8080/tts"
    data = {"input": content, "model": " en-us-blizzard_lessac-medium.onnx"}
    headers = {"Content-Type": "multipart/form-data"}
    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            audio_data = response.content
            return audio_data  # 返回音频数据
        else:
            print(f"Failed to generate audio: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        return None


if __name__ == "__main__":
    text2audio(
        "Sun Wukong (also known as the Great Sage of Qi Tian, Sun Xing Shi, and Dou Sheng Fu) is one of the main characters in the classical Chinese novel Journey to the West"
    )
