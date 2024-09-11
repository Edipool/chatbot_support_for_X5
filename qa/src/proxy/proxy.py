from fastapi import FastAPI
import requests
import uvicorn

app = FastAPI()

@app.get("/query")
async def proxy_query(query: str):
    response = requests.get(f"http://95.182.121.46/:8081/query?query={query}")
    return {"response": response.json()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
