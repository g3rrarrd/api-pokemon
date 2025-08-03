import uvicorn
import fastapi
from utils.database import execute_query_json
from controller.pokeRequestController import insert_poke_request, update_poke_request, select_poke_request
from models.pokeRequest import PokeRequest

app = fastapi.FastAPI()

@app.get("/version")
async def version():
    return {"version": "0.2.0"}

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
    
@app.post("/api/pokemon/request")
async def create_poke_request(poke_request: PokeRequest):
    return await insert_poke_request(poke_request)

@app.put("/api/pokemon/request")
async def modify_poke_request(poke_request: PokeRequest):
    return await update_poke_request(poke_request)

@app.get("/api/pokemon/request/{id}")
async def get_poke_request(id: int):
    return await select_poke_request(id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


