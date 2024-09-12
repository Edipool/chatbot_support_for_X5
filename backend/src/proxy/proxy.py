import requests
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/query")
async def proxy_query(query: str):
    """
    Функция для обработки запроса пользователя

    Аргументы:
    query - строка, содержащая запрос пользователя

    Возвращаемое значение:
    response - строка, содержащая ответ на запрос пользователя
    """
    response = requests.get(f"http://95.182.121.46:8081/query?query={query}")
    return {"response": response.json()}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
