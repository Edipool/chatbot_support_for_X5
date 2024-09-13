import requests
import streamlit as st
from langchain.schema import ChatMessage
import pandas as pd
import uuid
import time

st.set_page_config(page_title="X6 Bot", page_icon="🔍")

# Инициализация состояния для хранения чатов
if "chats" not in st.session_state:
    st.session_state["chats"] = {}  # Словарь для хранения активных чатов
    st.session_state["archived_chats"] = {}  # Словарь для хранения архивированных чатов
    st.session_state["current_chat_id"] = None  # Идентификатор текущего чата


# Создание нового чата
def create_new_chat():
    chat_id = str(uuid.uuid4())  # Генерация уникального идентификатора чата
    st.session_state["chats"][chat_id] = {
        "messages": [
            ChatMessage(
                role="assistant",
                content="Привет!✌️ Я X6, ваш личный ассистент, который знает (почти) все о внутрикорпоративных тонкостях. Подскажите, чем я могу быть полезен?"
            )
        ],
        "feedback_df": pd.DataFrame(columns=["user_query", "server_response", "rating"])
    }
    st.session_state["current_chat_id"] = chat_id


# Отправление запроса на FastAPI сервер
def send_request(prompt):
    try:
        response = requests.get(f"http://95.182.121.46:8080/query?query={prompt}")
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Нет ответа от FastAPI сервера. Код статуса: {response.status_code}"
    except Exception as e:
        return f"Произошла ошибка: {e}"


# Функция для обработки оценки
def handle_feedback(chat_id, user_query, server_response, rating):
    feedback_data = pd.DataFrame({"user_query": [user_query], "server_response": [server_response], "rating": [rating]})
    st.session_state["chats"][chat_id]["feedback_df"] = pd.concat(
        [st.session_state["chats"][chat_id]["feedback_df"], feedback_data], ignore_index=True)


# Интерфейс для выбора и создания чатов
st.sidebar.header("Чаты")

# Выход из приложения
if st.sidebar.button("Выйти из чата"):
    st.stop()  # Завершение работы Streamlit приложения

# Создание нового чата
if st.sidebar.button("Новый чат"):
    create_new_chat()

# Вывод активных чатов
st.sidebar.markdown("### Активные чаты", unsafe_allow_html=True)
active_chats = list(st.session_state["chats"].keys())
if active_chats:
    for chat_id in active_chats:
        chat_name = chat_id[:8]  # Отображение первых 8 символов ID для краткости
        chat_title = f"**{chat_name}**"
        col1, col2 = st.sidebar.columns([2, 1])  # Расширяем ширину первого столбца для чатов
        with col1:
            if st.button(chat_title, key=f"active_chat_{chat_id}", use_container_width=True):
                st.session_state["current_chat_id"] = chat_id
        with col2:
            if st.button("Закрыть чат", key=f"close_chat_{chat_id}", use_container_width=True):
                st.session_state["archived_chats"][chat_id] = st.session_state["chats"].pop(chat_id)
                st.session_state["current_chat_id"] = None
                st.experimental_rerun()  # Обновление интерфейса после закрытия чата

# Добавляем несколько пустых строк между активными и архивными чатами
st.sidebar.markdown("<br>" * 3, unsafe_allow_html=True)

# Вывод архивных чатов
st.sidebar.markdown("### Архивные чаты", unsafe_allow_html=True)
archived_chats = list(st.session_state["archived_chats"].keys())
if archived_chats:
    for chat_id in archived_chats:
        chat_name = chat_id[:8]  # Отображение первых 8 символов ID для краткости
        chat_title = f"**{chat_name}**"
        if st.sidebar.button(chat_title, key=f"archived_chat_{chat_id}", use_container_width=True):
            st.session_state["current_chat_id"] = chat_id

# Приветственное сообщение
if not st.session_state.get("current_chat_id"):
    st.markdown(
        "<h1 style='text-align: center; font-size: 36px;'>Добро пожаловать в службу поддержки, Новый пользователь!</h1>",
        unsafe_allow_html=True
    )

# Проверка текущего чата
if st.session_state["current_chat_id"]:
    chat = st.session_state["chats"].get(st.session_state["current_chat_id"],
                                         st.session_state["archived_chats"].get(st.session_state["current_chat_id"]))

    st.subheader("Техническая поддержка X5", divider="green")

    # Выведение истории чата
    for idx, message in enumerate(chat["messages"]):
        if message.role == "user":
            with st.chat_message(message.role, avatar="🦖"):
                st.markdown(message.content)
        else:
            with st.chat_message(message.role, avatar="🖥️"):
                st.markdown(message.content)

    # Отображение кнопок для оценки после ответа сервера
    if "current_feedback_state" in st.session_state and st.session_state["current_feedback_state"]:
        col1, col2 = st.columns(2)
        with col1:
            like_button = st.button("👍", key=f"like_feedback_{st.session_state['current_feedback_state']['timestamp']}",
                                    use_container_width=True)
        with col2:
            dislike_button = st.button("👎",
                                       key=f"dislike_feedback_{st.session_state['current_feedback_state']['timestamp']}",
                                       use_container_width=True)

        # Обработка лайков и дизлайков
        if like_button:
            handle_feedback(st.session_state["current_chat_id"],
                            st.session_state["current_feedback_state"]["user_query"],
                            st.session_state["current_feedback_state"]["server_response"], "like")
            st.session_state["current_feedback_state"] = None
            st.experimental_rerun()  # Обновление интерфейса после обработки кнопок

        if dislike_button:
            handle_feedback(st.session_state["current_chat_id"],
                            st.session_state["current_feedback_state"]["user_query"],
                            st.session_state["current_feedback_state"]["server_response"], "dislike")
            st.session_state["current_feedback_state"] = None
            st.experimental_rerun()  # Обновление интерфейса после обработки кнопок

    # Инициализация окна ввода информации для пользователя
    chat_is_archived = st.session_state["current_chat_id"] in st.session_state["archived_chats"]

    # Если чат в архиве, сделать поле ввода недоступным
    input_disabled = chat_is_archived

    if prompt := st.chat_input("Напишите ваш вопрос", disabled=input_disabled):
        message = ChatMessage(role="user", content=prompt)
        chat["messages"].append(message)

        with st.chat_message("user", avatar="🦖"):
            st.markdown(message.content)

        # Генерация ответа ассистента и получение ответа с FastAPI сервера
        with st.chat_message("assistant", avatar="🖥️"):
            # Имитируем потоковую передачу текста
            server_answer = send_request(prompt)
            response_text = server_answer
            output_text = ""
            progress_text = st.empty()

            for char in response_text:
                output_text += char
                progress_text.markdown(f"{output_text} ...")
                time.sleep(0.05)  # Задержка для эффекта печати

            # Обновляем финальный текст после завершения "печатания"
            st.markdown(output_text)

            # Добавляем ответ в историю сообщений
            chat["messages"].append(ChatMessage(role="assistant", content=output_text))
            st.session_state["current_feedback_state"] = {
                "user_query": prompt,
                "server_response": response_text,
                "timestamp": pd.Timestamp.now().timestamp()  # добавляем временную метку для уникальности ключей
            }

            # Обновляем интерфейс после установки состояния
            st.experimental_rerun()  # Обновление интерфейса после получения ответа


    # Сохранение датафрейма при завершении сессии
    def save_feedback():
        for chat_id, chat_data in st.session_state["chats"].items():
            if not chat_data["feedback_df"].empty:
                file_path = f"feedback_{chat_id}.csv"
                chat_data["feedback_df"].to_csv(file_path, index=False, encoding='utf-16')

        for chat_id, chat_data in st.session_state["archived_chats"].items():
            if not chat_data["feedback_df"].empty:
                file_path = f"feedback_{chat_id}.csv"
                chat_data["feedback_df"].to_csv(file_path, index=False, encoding='utf-16')


    # Проверяем, закончилась ли сессия
    if st.session_state.get("current_feedback_state") is None and chat["messages"]:
        save_feedback()
