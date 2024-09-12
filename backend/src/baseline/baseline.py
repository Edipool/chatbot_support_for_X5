import pandas as pd
import uvicorn
from fastapi import FastAPI
from sklearn.preprocessing import LabelEncoder
from src.baseline.model import ChatbotModel

chatbot = None

app = FastAPI()


@app.get("/query")
async def handle_query(query: str):
    """
    Функция для обработки запроса пользователя

    Аргументы:
    query - строка, содержащая запрос пользователя

    Возвращаемое значение:
    answer - строка, содержащая ответ на запрос пользователя
    """
    global chatbot
    answer = chatbot.predict(query)[0]
    print(f"query: {query}, answer: {answer}")
    return answer


if __name__ == "__main__":
    df = pd.read_excel("../../data/LK_modified.xlsx", sheet_name=1)
    category_counts = df["content"].value_counts()
    small_categories = category_counts[category_counts < 7].index
    df["content"] = df["content"].replace(small_categories, "поддержка")
    label_encoder = LabelEncoder().fit(df["content"])
    chatbot = ChatbotModel(df, label_encoder)
    uvicorn.run(app, host="0.0.0.0", port=8081)
