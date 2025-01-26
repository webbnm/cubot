import time

import requests
import secret

def YandexGPT(text):
    folder_id = secret.folder_id
    api_key = secret.api_key
    gpt_model = 'yandexgpt-lite'

    system_prompt = 'Ты автор рассказов, тебе будут даваться темы, а ты должен сгенерировать рассказ. Возвращай ТОЛЬКО сам рассказ'
    user_prompt = text

    body = {
        'modelUri': f'gpt://{folder_id}/{gpt_model}',
        'completionOptions': {'stream': False, 'temperature': 1, 'maxTokens': 2000},
        'messages': [
            {'role': 'system', 'text': system_prompt},
            {'role': 'user', 'text': user_prompt},
        ],
    }
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Api-Key {api_key}'
    }

    response = requests.post(url, headers=headers, json=body)
    operation_id = response.json().get('id')

    url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"
    headers = {"Authorization": f"Api-Key {api_key}"}

    while True:
        response = requests.get(url, headers=headers)
        done = response.json()["done"]
        if done:
            break
        else:
            time.sleep(1)

    data = response.json()
    answer = data['response']['alternatives'][0]['message']['text']

    return answer