from fastapi import Request, HTTPException, Depends
import secrets


async def verify_client_key(request: Request) -> str:
    """
    Verify client key from request header using timing-safe comparison.
    If no header is provided, fall back to backend env key for local app usage.
    """
    from backend.app.config import settings
    
    key = request.headers.get("X-IntelliSearch-Client-Key")
    
    if key is None:
        # Frontend does not need to send a key; backend uses env-configured key.
        return settings.CLIENT_KEY
    
    if not secrets.compare_digest(key, settings.CLIENT_KEY):
        raise HTTPException(status_code=403, detail="Invalid client key")
    
    return key
