import requests
import json

#функция, отправляющая запрос на сервер и получающая ответ
def get_predited_tag(msg):
    #адрес сервера
    url = "http://158.160.110.56:5000/classify"
    headers = {'Content-Type': 'application/json'}
    #переменная msg - это сообщение пользователя
    data = {"text": msg}
    #получаем ответ
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        response_data = response.json()
        #извлечение значения тега 'predicted_tag'
        predicted_tag = response_data.get('predicted_tag')
        return predicted_tag
    else:
        #на случай ошибок
        return response.status_code, response.text

#использование функции
msg = "купить молоко"
predicted_tag = get_predited_tag(msg)
print(predicted_tag)
