import uvicorn
import fastapi

from fastapi.middleware.cors import CORSMiddleware
from utils.database import execute_query_json
from controller.pokeRequestController import insert_poke_request, update_poke_request, select_poke_request, get_all_request
from models.pokeRequest import PokeRequest

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/version")
async def version():
    return {"version": "0.4.0"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API pokemon!"}

@app.get("/pokemon/messages")
async def get_messages():
    sql_template = "SELECT * FROM pokemonqueue.messages;"
    try:
        results = await execute_query_json(sql_template)
        return {"messages": results}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/api/pokemon/request/{id}")
async def get_poke_request(id: int):
    return await select_poke_request(id)

@app.get("/api/pokemon/request")
async def select_all_request():
    return await get_all_request()
    
@app.post("/api/pokemon/request")
async def create_poke_request(poke_request: PokeRequest):
    return await insert_poke_request(poke_request)

@app.put("/api/pokemon/request")
async def modify_poke_request(poke_request: PokeRequest):
    return await update_poke_request(poke_request)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


