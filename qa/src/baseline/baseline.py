from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/query")
async def handle_query(query: str):
    if query == "Как твои дела":
        return {"answer": "нормально"}
    else:
        return {"answer": "turn on to human"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
