# Chatbot_support_for_X5
---
# О чем это проект?
Этот проект призван решить проблему поиска ответа на вопрос. За время работы X5 накопилась огромная база знания с парами "вопрос-ответ". Руководство компании решило выставить на первую линию общения чат-бота вместо обращения к операторам. Если пользовать удовлетворен ответом на свой вопрос от чат-бота - он не идет дальше на вторую линию к операторам, что, в свою очередь, снижает нагрузку и смещает акцент реагирования только на те вопросы, которых нет в базе знаний.

---
# Что под капотом?
Данная версия bassline-решения работает на основе tf-idf и word2vec алгоритмов поиска и модели на базе данных с парами "вопрос-ответ". Данное решение не требует серьёзнаых вычислительных мощностье, финансовых затрат и представляет собой быстрое решение в условиях ограниченного времени и ресурсов.

---
# Как пользоваться чат-ботом?
У вас есть на выбор два способа пользоваться чат-ботом:
1. Пользовательский интерфейс чат-бота написанного на Streamlit. Пользовательский интерфейс чат-бота доступен по адресу https://x6-bot.streamlit.app/.
2. API к чат-боту написанному на FastAPI. Для использования API необходимо сделать запрос.
**Пример запроса для Curl:**
    ```
    curl -G "http://95.182.121.46:8080/query" --data-urlencode "query=Я сменил автомобить, на учет еще не поставил, могу ли я заправляться по топливной карте?"
    ```
**Пример запроса для Postman:**
1. Открыть *Postman*
2. Добавить новый *GET-запрос*
3. В URL ввести ```http://95.182.121.46:8080/query?query=Я сменил автомобить, на учет еще не поставил, могу ли я заправляться по топливной карте?```

---
# Документация
Нами был написанн ML System Design Doc для bassline-решение, в котором описана вся методология ML-решения. Ознакомиться ML System Design Doc в можете в директории docs.

---
# Организация проекта
.
├── backend  <-- Backend проекта
│   ├── data  <-- Данные для работы с базой данных
│   │   └── LK_modified.xlsx  <-- База данных с парами "вопрос-ответ"
│   ├── requirements.txt  <-- Требуемые пакеты для работы с бэкендом
│   └── src  <-- Исходные коды для работы с бэкендом
│       ├── baseline  <-- Базовый алгоритм поиска ответа на вопрос
│       │   ├── baseline.py  -  Базовый алгоритм поиска ответа на вопрос
│       │   ├── Dockerfile  <-- Dockerfile для базового алгоритма поиска ответа на вопрос
│       │   ├── model.py  <-- Модель на базе данных с парами "вопрос-ответ"
│       │   └── requirements.txt  <-- Требуемые пакеты для работы с базовым алгоритмом поиска ответа на вопрос
│       └── proxy  <-- Прокси для работы с бэкендом
│           ├── Dockerfile  <-- Dockerfile для прокси для работы с бэкендом
│           └── proxy.py  <-- Прокси для работы с бэкендом
├── docker-compose.yml  <-- Докер-компоуз для работы с бэкендом
├── docs  <-- Документация по работе с бэкендом
│   └── ML System Design Doc - Chat-bot for X5.md  <-- Документация по работе с бэкендом
├── notebooks  <-- PоC
│   └── PoC_Chat_bot_for_X5.ipynb
├── README.md
└── ui  <-- UI проекта
    ├── requirements.txt  <-- Требуемые пакеты для работы с пользовательским интерфейсом
    └── streamlit_app.py  <-- Пользовательский интерфейс

---
# Инструменты проекта
![MLOps](https://img.shields.io/badge/-MLOps-090909?style=for-the-badge&logo=MLOps) ![ML System Design Document](https://img.shields.io/badge/-ML_System_Design-090909?style=for-the-badge&logo=ML_System_Design) ![Streamlit](https://img.shields.io/badge/-Streamlit-090909?style=for-the-badge&logo=Streamlit) ![Fastapi](https://img.shields.io/badge/-Fastapi-090909?style=for-the-badge&logo=Fastapi) ![Docker](https://img.shields.io/badge/-Docker-090909?style=for-the-badge&logo=Docker) ![Docker Compose](https://img.shields.io/badge/-docker_compose-090909?style=for-the-badge&logo=docker_compose) ![Scikit_learn](https://img.shields.io/badge/-Scikit_learn-090909?style=for-the-badge&logo=Scikit_learn) ![TF-IDF](https://img.shields.io/badge/-TF_IDF-090909?style=for-the-badge&logo=TF_IDF) ![Word2Vec](https://img.shields.io/badge/-Word2Vec-090909?style=for-the-badge&logo=Word2Vec)
