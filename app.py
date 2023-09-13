import gradio as gr
import os
import time
import requests
import json
import pdf
import function
import fetch
import chat
import search
# Chatbot demo with multimodal input (text, markdown, LaTeX, code blocks, image, audio, & video). Plus shows support for streaming text.
# message:[{"role": "user", "content": "Who won the world series in 2020?"},{"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},{"role": "user", "content": "Where was it played?"}] 
messages = []
current_file_text = None

def add_text(history, text):# 对话框
    #print(history,text)
    history = history + [(text, None)]
    
    return history, gr.update(value="", interactive=False)


def add_file(history, file):# 上传文件  
    history = history + [((file.name,), None)]
    return history


def bot(history):# 回复
    global current_file_text
    last_msg = history[-1][0]
    response = ""
    #print(last_msg)
    if isinstance(last_msg, tuple):# 上传了一个文件
        last_msg = last_msg[0]
        #print(last_msg)
        extension = os.path.splitext(last_msg)[1].lower() 
        #print(extension)
        if extension == ".txt":# 文件聊天
            with open(last_msg,"r") as txt:
                current_file_text = txt.read()
                prompt = pdf.generate_summary(current_file_text)
                messages.append({"role": "user", "content": prompt})
                chat_generator = pdf.generate_text(prompt)
                history[-1][1] = ""
                for word in chat_generator:
                    history[-1][1]=history[-1][1]+word
                    yield history
                messages.append({"role": "assistant", "content": history[-1][1]})     
        else:
            history[-1][1] = "other file"
            messages.append({"role": "assistant", "content": history[-1][1]})
            return history
    elif last_msg[0] == '/': # 使用命令
        cmd = last_msg.split(" ")[0] #获取命令
        content = last_msg[len(cmd)+1:] #获取命令后面的内容
        if cmd == "/file": # 文件聊天
            prompt = pdf.generate_answer(current_file_text,content)
            messages.append({"role": "user", "content": prompt})
            chat_generator = pdf.generate_text(prompt)
            history[-1][1] = ""
            for word in chat_generator:
                history[-1][1]=history[-1][1]+word
                yield history
            messages.append({"role": "assistant", "content": history[-1][1]})
            return history
        elif cmd == "/function":# 函数调用
            messages.append({"role":"user","content":content})
            response = function.function_calling(messages)
            history[-1][1] = response
            messages.append({"role": "assistant", "content": response})
            return history
        elif cmd == "/fetch": # 网页总结
            prompt = fetch.fetch(content)
            messages.append({"role":"user","content":prompt})
            chat_generator=chat.chat(messages)
            history[-1][1] = ""
            for word in chat_generator:
                history[-1][1]=history[-1][1]+word
                yield history
            messages.append({"role": "assistant", "content": history[-1][1]})
        elif cmd== "/search":#网络搜索
            prompt = search.search(content)
            #print(prompt)
            messages.append({"role":"user","content":prompt})
            # print(prompt)
            chat_generator=chat.chat(messages)
            history[-1][1] = ""
            for word in chat_generator:
                history[-1][1]=history[-1][1]+word
                yield history
            # print(history)
            messages.append({"role": "assistant", "content": history[-1][1]})
        else:
            response = "other command"
            history[-1][1] = response
            messages.append({"role": "assistant", "content": response})
            return history
    else:
        #print(type(last_msg))
        messages.append({"role":"user","content":last_msg})
        history[-1][1]=""
        chat_generator=chat.chat(messages)
        for word in chat_generator:
            history[-1][1]=history[-1][1]+word
            yield history
            # print(history)
        messages.append({"role": "assistant", "content": history[-1][1]})
    #print(messages)
    
    

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        clear_btn = gr.Button('Clear')
        btn = gr.UploadButton("📁", file_types=["file"])

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot
    )
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear_btn.click(lambda: messages.clear(), None, chatbot, queue=False)

demo.queue()
demo.launch()
