import json
import logging

from fastapi import APIRouter, HTTPException, Depends
from models.pokeRequest import PokeRequest
from utils.database import execute_query_json
from utils.aQueue import aQueue
from utils.ABlob import ABlob

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

    
async def update_poke_request(poke_request: PokeRequest):

    
    try:
        query = """CALL pokemonqueue.update_poke_request(%s, %s, %s);"""
        
        if not poke_request.url:
            poke_request.url = ""
        
        params = (poke_request.id, poke_request.status, poke_request.url)
        result = await execute_query_json(query, params, True)
        
        if not result:
            raise HTTPException(status_code=404, detail="Request not found")
            
        result_dict = json.loads(result)
        return result_dict

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        raise HTTPException(status_code=500, detail="Invalid response from database")
    except Exception as e:
        logger.error(f"Error updating poke request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def select_poke_request(id: int):
    try:

        query = "select * from pokemonqueue.requests where id = %s"

        params = (id,)
        result = await execute_query_json(query, params, True)
        result_dict = json.loads(result)

        return result_dict
        

    except Exception as e:
        logger.error(f"Error actualizando poke request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def get_all_request() -> dict:
    try:

        query = """select 
        r.id as ReporteId ,
         s.description as Status,
          r.type as PokemonType,
           r.url,
            r.created,
             r.updated
              from pokemonqueue.requests r
              inner join pokemonqueue.status s
              on r.id_status = s.id"""

        result = await execute_query_json(query, None, True)
        result_dict = json.loads(result)
        blob = ABlob()
        for record in result_dict:
            id = record["reporteid"]
            record["url"] = f"{record['url']}{blob.generate_sas_token(id)}"
        
        return result_dict
        

    except Exception as e:
        logger.error(f"Error obteniendo todas las poke requests: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")