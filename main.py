import uvicorn
import fastapi

app = fastapi.FastAPI()

@app.get("/version")
async def version():
    return {"version": "0.0.0"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

