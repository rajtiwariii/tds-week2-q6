import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import redis

app = FastAPI()

def get_redis_client():
    redis_host = os.getenv("REDIS_HOST", "redis")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    return redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.post("/hit/{key}")
async def hit_counter(key: str):
    try:
        r = get_redis_client()
        count = r.incr(key)
        return {"key": key, "count": int(count)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/count/{key}")
async def get_counter(key: str):
    try:
        r = get_redis_client()
        val = r.get(key)
        count = int(val) if val is not None else 0
        return {"key": key, "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/healthz")
async def health_check():
    try:
        r = get_redis_client()
        pong = r.ping()
        if pong:
            return {"status": "ok", "redis": "up"}
    except Exception:
        pass
    return JSONResponse(status_code=500, content={"status": "error", "redis": "down"})