import uvicorn
import fastapi
import logging

from fastapi.middleware.cors import CORSMiddleware
from utils.database import execute_query_json
from controller.pokeRequestController import insert_poke_request, update_poke_request, select_poke_request, get_all_request, delete_report
from models.pokeRequest import PokeRequest


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
    return {"version": "0.4.1"}

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
    logger.info("param received: %s", poke_request)
    print(f"Received poke_request: {poke_request}")
    return await update_poke_request(poke_request)

@app.delete("/api/pokemon/request/{report_id}")
async def delete_poke_request(report_id: int):
    return await delete_report(report_id)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


