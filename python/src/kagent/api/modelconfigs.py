from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any

router = APIRouter()

@router.get("/modelconfigs")
async def get_modelconfigs(user_id: str = Query(...)) -> List[Dict[str, Any]]:
    try:
        # Return a list of model configurations
        return [
            {
                "name": "default-model-config",
                "provider": "openai",
                "model": "gpt-4",
                "config": {
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
            }
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/modelconfigs/{name}")
async def get_modelconfig(name: str, user_id: str = Query(...)) -> Dict[str, Any]:
    try:
        # Return a specific model configuration
        return {
            "name": name,
            "provider": "openai",
            "model": "gpt-4",
            "config": {
                "temperature": 0.7,
                "max_tokens": 2000
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
