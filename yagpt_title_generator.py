import requests

#открываем новоть из txt-файла
#потом заменится на сообщение от пользователя
with open('long_text_sample.txt', encoding='utf8') as f:
    msg = f.read()

def get_generated_text(msg, prompt):
    #открываем txt-файл с id каталога на яндекс клауде и api ключом (очень секретный)
    with open('yagpt_login.txt') as f:
        lines = f.readlines()
        cat_id, api_key = lines[0].strip(), lines[1].strip()

    #составляем промпт
    title_prompt = {
        #уточняем модель
        'modelUri': f'gpt://{cat_id}/yandexgpt-lite',
        #стандартные параметры
        'completionOptions': {
            'stream': False,
            'temperature': 0.6,
            'maxTokens': '2000'
        },
        'messages': [
            {
                #определяем контекст диалога, что должна сделать модель
                'role': 'system',
                'text': prompt
            },
            {
                #что пришло от пользователя
                'role': 'user',
                'text': msg
            }
        ]
    }

    #адрес, на который отправляем запрос
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    #вставляем api-key
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Api-Key {api_key}'
    }

    #получаем ответ
    response = requests.post(url, headers=headers, json=title_prompt)

    #извлекаем из ответа нужную часть
    resp_json = response.json()
    result = resp_json['result']['alternatives'][0]['message']['text']
    return result

#определяют, что будем генерировать: название или описание
title_prompt = 'Сформулируй короткое название из нескольких слов для данного текста, передающее его суть'
summary_prompt = 'Напиши краткое саммари данного текста, используй не больше 15 слов'

title = get_generated_text(msg, title_prompt)
summary = get_generated_text(msg, summary_prompt)
print(title, summary)