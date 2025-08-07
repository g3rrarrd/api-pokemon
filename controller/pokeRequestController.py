import os
import json
import logging

from models.pokeRequest import PokeRequest

from utils.database import execute_query_json
from utils.aQueue import aQueue
from utils.ABlob import ABlob

from fastapi import APIRouter, HTTPException, Depends, status
from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob.aio import BlobServiceClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
    print(f"Received poke_request for update: {poke_request}")

    try:
        query = """CALL pokemonqueue.update_poke_request(%s, %s, %s);"""
           
        if poke_request.url is None:
            poke_request.url = "https://default.url/report.csv"
        
        params = (poke_request.id, poke_request.status, poke_request.url)
        result = await execute_query_json(query, params, True)
        
        if not result:
            raise HTTPException(status_code=404, detail="Request not found")
            
        result_dict = json.loads(result)
        return result_dict
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating report request: {e}")
        logger.error(f"Error updating report request {e}")
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
            record['url'] = f"{record['url']}?{blob.generate_sas(id)}"
        
        return result_dict
        

    except Exception as e:
        logger.error(f"Error obteniendo todas las poke requests: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
async def delete_report(report_id: int):
    try:
        
        select_q = "SELECT id, url FROM pokemonqueue.requests WHERE id = %s"
        select_res = await execute_query_json(select_q, (report_id,), True)

        if not select_res:
        
            raise HTTPException(status_code=404, detail=f"Report with ID {report_id} not found")

        
        if isinstance(select_res, str):
            rows = json.loads(select_res)
        else:
            rows = select_res

        if not rows or len(rows) == 0:
            raise HTTPException(status_code=404, detail=f"Report with ID {report_id} not found")

        row = rows[0]
        blob_url = row.get("url") or ""

        delete_query = "DELETE FROM pokemonqueue.requests WHERE id = %s"
        await execute_query_json(delete_query, (report_id,), needs_commit=True)
        logger.info(f"Report {report_id} deleted from DB")

        
        blob_deleted = False
        if blob_url:
            try:
                blob = ABlob()
        
                await asyncio.to_thread(blob.delete_blob, report_id)
                blob_deleted = True
                logger.info(f"Blob for report {report_id} deleted")
            except Exception as be:
                logger.warning(f"Failed deleting blob for report {report_id}: {be}")
        return {
            "message": "Report deleted successfully",
            "report_id": report_id,
            "blob_deleted": blob_deleted
        }

    except HTTPException:
        # re-lanzar 404
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting report {report_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error while deleting report")

