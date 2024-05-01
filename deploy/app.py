from flask import Flask, request, jsonify
import onnxruntime as ort
import numpy as np

from transformers import BertTokenizer

app = Flask(__name__)

#загружаем модель onnx
session = ort.InferenceSession("bert_model.onnx")
input_names = [input.name for input in session.get_inputs()]
output_names = [output.name for output in session.get_outputs()]

#загружаем токенизатор
tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")

@app.route('/classify', methods=['POST'])
def classify():
    #получаем данные из POST-запроса
    data = request.json
    text = data['text']

    #токенизируем текст
    inputs = tokenizer(text, return_tensors="np", truncation=True, max_length=512)
    input_ids = inputs['input_ids'].astype(np.int64)
    attention_mask = inputs['attention_mask'].astype(np.int64)

    #делаем предсказания
    outputs = session.run(output_names, {
    input_names[0]: input_ids,
    input_names[1]: attention_mask
    })

     #применяем Softmax для получения вероятностей
    probabilities = np.exp(outputs[0]) / np.sum(np.exp(outputs[0]), axis=1, keepdims=True)

    threshold = 0.1
    #сравниваем два самых больших результата
    max_idx = np.argmax(probabilities)
    second_max_idx = np.argsort(probabilities)[-1][-2]

    #если разница меньше порога, ставим категорию "другое"
    if probabilities[0][max_idx] - probabilities[0][second_max_idx] < threshold:
        predicted_class_id = 3
        predicted_tag = 'другое'
    else:
        predicted_class_id = max_idx.item()
        if predicted_class_id == 0:
            predicted_tag = 'быт'
        elif predicted_class_id == 1:
            predicted_tag = 'работа/учеба'
        elif predicted_class_id == 2:
            predicted_tag = 'покупки'

    #возвращаем тег как результат
    return jsonify({"predicted_tag": predicted_tag})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    