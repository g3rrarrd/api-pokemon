import json
import logging

from fastapi import APIRouter, HTTPException, Depends
from models.pokeRequest import PokeRequest
from utils.database import execute_query_json
from utils.aQueue import aQueue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def insert_poke_request(poke_request: PokeRequest):
    try:

        query = """CALL pokemonqueue.create_poke_request(%s, NULL);"""
        params = (poke_request.pokemon_type,)
        result = await execute_query_json(query, params, True)
        result_dict = json.loads(result)

        await aQueue().insert_message_on_queue(result)

        return result_dict
        

    except Exception as e:
        logger.error(f"Error insertando poke request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    