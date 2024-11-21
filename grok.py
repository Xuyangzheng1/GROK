import requests

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

# 使用示例
prompt = "你觉得比特币以后还会涨嘛"
result = call_xai_api(prompt)
print(result)