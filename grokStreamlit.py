import streamlit as st
import requests
import json
from datetime import datetime

def call_xai_api(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer xai-d6n1Go29r7uVNAjhv5zS2RMU7k2waruE2wKrSfFISN4x3NOqjhR7rgpyN75SnkTbhuYTFbnO4CSi5hzs'
    }
    
    data = {
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt}
        ],
        'model': 'grok-beta',
        'stream': False,
        'temperature': 0
    }
    
    response = requests.post('https://api.x.ai/v1/chat/completions', 
                           headers=headers, 
                           json=data)
    return response.json()

def init_session_state():
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    if 'current_chat' not in st.session_state:
        st.session_state['current_chat'] = []

def main():
    st.set_page_config(page_title="Grok Chat", layout="wide")
    
    st.title("🤖 Grok Chat")
    init_session_state()

    # 侧边栏
    with st.sidebar:
        st.header("聊天记录")
        if st.button("新建对话"):
            st.session_state['current_chat'] = []
            st.experimental_rerun()
        
        # 显示历史对话列表
        for idx, chat in enumerate(st.session_state['messages']):
            if st.button(f"对话 {idx + 1} - {chat['time']}", key=f"chat_{idx}"):
                st.session_state['current_chat'] = chat['messages']
                st.experimental_rerun()

    # 主聊天界面
    chat_container = st.container()
    
    # 显示当前对话
    with chat_container:
        for message in st.session_state['current_chat']:
            role = message['role']
            with st.chat_message(role):
                st.write(message['content'])
    
    # 输入框
    prompt = st.chat_input("发送消息...")
    
    if prompt:
        # 显示用户输入
        with st.chat_message("user"):
            st.write(prompt)
            st.session_state['current_chat'].append({
                "role": "user",
                "content": prompt
            })
        
        # 获取API响应
        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                response = call_xai_api(prompt)
                content = response['choices'][0]['message']['content']
                st.write(content)
                st.session_state['current_chat'].append({
                    "role": "assistant",
                    "content": content
                })
        
        # 保存当前对话
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        st.session_state['messages'].append({
            'time': current_time,
            'messages': st.session_state['current_chat']
        })

if __name__ == "__main__":
    main()