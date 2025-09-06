from fastapi import HTTPException, Header
from config import SECRET_KEY


def auth_required(api_key: str = Header(alias="x-api-key")):
    if not SECRET_KEY:
        raise HTTPException(status_code=500, detail="Server configuration error")
    
    if not api_key or api_key != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return True