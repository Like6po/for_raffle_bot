# загрузка официального образа
FROM python:3.10.4
# установка рабочей директории
WORKDIR /app
# установка переменных окржуений
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# установка зависимостей пайтона
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# добавление в контейнер приложения
COPY . .
