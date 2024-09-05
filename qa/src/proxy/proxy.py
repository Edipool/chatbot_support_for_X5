from fastapi import FastAPI
import requests
import uvicorn

app = FastAPI()

@app.get("/query")
async def proxy_query(query: str):
    response = requests.get(f"http://127.0.0.1:8081/query?query={query}")
    return {"response": response.json()}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
