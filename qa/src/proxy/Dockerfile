# Используем базовый образ Python 3.9 slim
FROM python:3.9-slim

# Устанавливаем git для клонирования репозитория и другие зависимости
RUN apt-get update && apt-get install -y git

# Используем секрет для передачи токена и клонируем репозиторий
RUN --mount=type=secret,id=git_token \
    bash -c 'GIT_TOKEN=$(cat /run/secrets/git_token) && git clone https://$GIT_TOKEN:x-oauth-basic@github.com/Edipool/chatbot_support_for_X5.git'

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /chatbot_support_for_X5/qa

RUN git checkout qa_baseline

# Копируем зависимости из requirements.txt и устанавливаем их
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем рабочую директорию для запуска скрипта
WORKDIR /chatbot_support_for_X5/qa/src/baseline

# Expose port 8080 to the outside world
EXPOSE 8080

CMD ["uvicorn", "baseline:app", "--host", "0.0.0.0", "--port", "8080"]
