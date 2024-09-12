import streamlit as st
import requests
from langchain.schema import ChatMessage

st.set_page_config(page_title="X6 Bot", page_icon="🔍")

# Отправление запроса на FastAPI сервер
def send_request(prompt):
  try:
    response = requests.get(f"http://95.182.121.46:8080/query?query={prompt}")
    # response = requests.get(url, json=data)
    if response.status_code == 200:
      answer = response.json()["response"]
      if answer == "поддержка":
        return "Прошу прощения, вы обошли искусственный интеллект 🥺. Перевожу вас на оператора"
      else:
        return f"Вот что я нашел по вашему запросу:  \n{answer}"
      # return " ".join(map(str, answer))
    else:
      st.markdown(
      f"Нет ответа от FastAPI сервера ({url}). Код статуса: {response.status_code}"
              )
  except Exception as e:
    st.markdown(f"Произошла ошибка: {e}")

st.subheader("Техническая поддержка X5", divider="green")

# Вводное сообщение от чатбота
if "messages" not in st.session_state:
  st.session_state["messages"] = [ChatMessage(role="assistant", content="Привет!✌️ Я X6, ваш личный ассистент, который знает (почти) все о внутрикорпоративных тонкостях. Подскажите, чем я могу быть полезен?")]

# Выведение истории чата 
for message in st.session_state.messages:
  if message.role == "user":
    with st.chat_message(message.role, avatar="🦖"):
      st.markdown(message.content)
  else:
    with st.chat_message(message.role, avatar="🖥️"):
      st.markdown(message.content)

# Инициализация окна ввода информации для пользователя
if prompt := st.chat_input("Напишите ваш вопрос"):
  message = ChatMessage(role="user", content=prompt)
  st.session_state["messages"].append(message)

  with st.chat_message("user", avatar="🦖"):
    st.markdown(message.content)

# Генерация ответа ассистента и получение ответа с FastAPI сервера
  with st.chat_message("assistant", avatar="🖥️"):
    with st.spinner("Обрабатываю ваш запрос..."):
      server_answer = send_request(prompt)
      assistant_answer = f"{server_answer}"
      message = ChatMessage(role="assistant", content=assistant_answer)
      st.session_state["messages"].append(message)
      st.markdown(message.content)
      # message_placeholder = st.empty()
      # message_placeholder.markdown(assistant_answer)
