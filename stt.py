
import openai

    
def audio2text(file):
    openai.api_key = "1111"
    openai.api_base="http://166.111.80.169:8080/v1"

    # 使用 OpenAI 的语音转文字 API
    audio_file = open(file, "rb")
    response = openai.Audio.transcribe("whisper-1", audio_file)
    # 获取转录文本
    transcription = response["segments"][0]["text"]
    return transcription

   

if __name__ == "__main__":
    print(audio2text("./sun-wukong.wav"))