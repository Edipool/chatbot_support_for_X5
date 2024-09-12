from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/health")
async def check_health():
    """
    Функция для проверки здоровья микросервиса

    Возвращаемое значение:
    answer - строка, содержащая текущее состояние сервиса
    """

    return "Advanced service is up and running"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)
