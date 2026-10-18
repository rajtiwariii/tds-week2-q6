import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import redis

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
except Exception:
    r = None

@app.post("/hit/{key}")
async def hit_counter(key: str):
    try:
        count = r.incr(key)
        return {"key": key, "count": int(count)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/count/{key}")
async def get_counter(key: str):
    try:
        val = r.get(key)
        count = int(val) if val is not None else 0
        return {"key": key, "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/healthz")
async def health_check():
    try:
        pong = r.ping()
        if pong:
            return {"status": "ok", "redis": "up"}
    except Exception:
        pass
    return JSONResponse(status_code=500, content={"status": "error", "redis": "down"})