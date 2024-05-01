#официальный образ Python
FROM python:3.10-slim

#рабочая директория
WORKDIR /app

#копируем файл зависимостей
COPY requirements.txt .
#устанавливаем библиотеки
RUN pip install --no-cache-dir -r requirements.txt

#копируем отальные файлы
COPY . /app

#указываем порт который будет прослушиваться
EXPOSE 5000

#запускаем приложение
CMD ["python", "app.py"]